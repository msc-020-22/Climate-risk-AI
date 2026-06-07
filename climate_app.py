"""
Climate Risk Assessment Web Application
A Streamlit app for assessing and visualizing climate-related risks.

Features:
- CSV file upload and validation
- Risk categorization (High/Medium/Low)
- Interactive visualizations and maps
- Professional report generation
- Data trend analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats
import io
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Climate Risk Assessment",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .high-risk {
        border-left-color: #ef553b;
    }
    .medium-risk {
        border-left-color: #ffa15a;
    }
    .low-risk {
        border-left-color: #00cc96;
    }
    .section-header {
        font-size: 24px;
        font-weight: bold;
        color: #1f77b4;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_csv_columns(df, required_columns=None):
    """
    Validate that CSV has required columns (flexible but expect specific ones).
    
    Args:
        df: DataFrame to validate
        required_columns: List of expected column names
    
    Returns:
        Tuple of (is_valid, message, available_columns)
    """
    if required_columns is None:
        required_columns = ['date', 'location', 'rainfall_mm', 'flood_depth_cm', 'temperature_c']
    
    df_cols_lower = [col.lower().strip() for col in df.columns]
    available_cols = {col.lower().strip(): col for col in df.columns}
    
    # Check which required columns are present
    missing = [col for col in required_columns if col not in df_cols_lower]
    
    if missing:
        return False, f"Missing columns: {', '.join(missing)}", available_cols
    
    return True, "All required columns present", available_cols

def categorize_risk(rainfall_mm, flood_depth_cm):
    """
    Categorize climate risk based on rainfall and flood depth.
    
    Risk Logic:
    - High risk: rainfall > 100mm OR flood_depth > 50cm
    - Medium risk: rainfall 50-100mm OR flood_depth 20-50cm
    - Low risk: rainfall < 50mm AND flood_depth < 20cm
    
    Args:
        rainfall_mm: Rainfall in millimeters
        flood_depth_cm: Flood depth in centimeters
    
    Returns:
        Risk category (str)
    """
    if pd.isna(rainfall_mm) or pd.isna(flood_depth_cm):
        return 'Unknown'
    
    if rainfall_mm > 100 or flood_depth_cm > 50:
        return 'High'
    elif (50 <= rainfall_mm <= 100) or (20 <= flood_depth_cm <= 50):
        return 'Medium'
    elif rainfall_mm < 50 and flood_depth_cm < 20:
        return 'Low'
    else:
        return 'Unknown'

def get_risk_color(risk_level):
    """Return color for risk level."""
    colors = {
        'High': '#ef553b',
        'Medium': '#ffa15a',
        'Low': '#00cc96',
        'Unknown': '#636EFA'
    }
    return colors.get(risk_level, '#636EFA')

def get_risk_recommendations(risk_level):
    """Get recommendations based on risk level."""
    recommendations = {
        'High': [
            '🚨 Install flood barriers and emergency drainage systems',
            '📢 Establish early warning systems',
            '👥 Evacuate vulnerable populations',
            '🏗️ Implement structural reinforcements',
            '📋 Activate emergency response protocols'
        ],
        'Medium': [
            '⚠️ Monitor weather conditions closely',
            '🔧 Maintain drainage infrastructure',
            '📱 Prepare emergency communication channels',
            '🛠️ Conduct regular equipment inspections',
            '📊 Increase monitoring frequency'
        ],
        'Low': [
            '✅ Continue routine monitoring',
            '📈 Track trends over time',
            '🔍 Maintain regular inspections',
            '📚 Keep awareness materials updated',
            '💾 Document baseline conditions'
        ]
    }
    return recommendations.get(risk_level, [])

def generate_lat_lon_for_demo(df):
    """Generate random latitude and longitude if not provided."""
    np.random.seed(42)
    
    if 'lat' not in df.columns and 'latitude' not in df.columns:
        df['lat'] = np.random.uniform(-90, 90, len(df))
    if 'lon' not in df.columns and 'longitude' not in df.columns:
        df['lon'] = np.random.uniform(-180, 180, len(df))
    
    return df

def create_risk_map(df, location_col, lat_col, lon_col, risk_col):
    """
    Create an interactive Folium map with risk markers.
    
    Args:
        df: DataFrame with location and risk data
        location_col: Column name for location names
        lat_col: Column name for latitude
        lon_col: Column name for longitude
        risk_col: Column name for risk level
    
    Returns:
        Folium map object
    """
    # Calculate map center
    center_lat = df[lat_col].mean()
    center_lon = df[lon_col].mean()
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=4,
        tiles="OpenStreetMap"
    )
    
    # Add markers
    for idx, row in df.iterrows():
        location = row[location_col]
        risk = row[risk_col]
        color = get_risk_color(risk)
        
        # Create popup with information
        popup_text = f"""
        <b>{location}</b><br>
        Risk Level: <b>{risk}</b><br>
        Rainfall: {row['rainfall_mm']:.1f}mm<br>
        Flood Depth: {row['flood_depth_cm']:.1f}cm<br>
        Temperature: {row['temperature_c']:.1f}°C
        """
        
        folium.CircleMarker(
            location=[row[lat_col], row[lon_col]],
            radius=10,
            popup=folium.Popup(popup_text, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)
    
    return m

def calculate_trend(df, date_col, value_col):
    """
    Calculate linear trend for a numeric value over time.
    
    Args:
        df: DataFrame with temporal data
        date_col: Column name for dates
        value_col: Column name for values
    
    Returns:
        Tuple of (slope, r_squared, trend_text)
    """
    try:
        df_sorted = df.sort_values(by=date_col).dropna(subset=[value_col])
        if len(df_sorted) < 2:
            return 0, 0, "Insufficient data for trend analysis"
        
        x = np.arange(len(df_sorted))
        y = df_sorted[value_col].values
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        r_squared = r_value ** 2
        
        if slope > 0:
            trend_text = f"📈 INCREASING (slope: {slope:.3f})"
        elif slope < 0:
            trend_text = f"📉 DECREASING (slope: {slope:.3f})"
        else:
            trend_text = "➡️ STABLE (slope: 0)"
        
        return slope, r_squared, trend_text
    
    except Exception as e:
        return 0, 0, f"Error calculating trend: {str(e)}"

def generate_report(df, risk_summary):
    """
    Generate a text report with executive summary and recommendations.
    
    Args:
        df: DataFrame with risk data
        risk_summary: Dictionary with risk counts
    
    Returns:
        String containing formatted report
    """
    report = []
    report.append("=" * 80)
    report.append("CLIMATE RISK ASSESSMENT REPORT")
    report.append("=" * 80)
    report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Executive Summary
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 80)
    report.append(f"Total Locations Analyzed: {len(df)}")
    report.append(f"High Risk Zones: {risk_summary.get('High', 0)} ({risk_summary.get('High', 0)/len(df)*100:.1f}%)")
    report.append(f"Medium Risk Zones: {risk_summary.get('Medium', 0)} ({risk_summary.get('Medium', 0)/len(df)*100:.1f}%)")
    report.append(f"Low Risk Zones: {risk_summary.get('Low', 0)} ({risk_summary.get('Low', 0)/len(df)*100:.1f}%)")
    
    # Key Statistics
    report.append("\n\nKEY STATISTICS")
    report.append("-" * 80)
    report.append(f"Average Rainfall: {df['rainfall_mm'].mean():.2f}mm")
    report.append(f"Maximum Rainfall: {df['rainfall_mm'].max():.2f}mm")
    report.append(f"Average Flood Depth: {df['flood_depth_cm'].mean():.2f}cm")
    report.append(f"Maximum Flood Depth: {df['flood_depth_cm'].max():.2f}cm")
    report.append(f"Average Temperature: {df['temperature_c'].mean():.2f}°C")
    
    # High Risk Locations
    high_risk_df = df[df['risk_level'] == 'High'].sort_values('rainfall_mm', ascending=False)
    if len(high_risk_df) > 0:
        report.append("\n\nHIGH RISK LOCATIONS")
        report.append("-" * 80)
        for idx, row in high_risk_df.iterrows():
            report.append(f"\n  {row['location'].upper()}")
            report.append(f"    Rainfall: {row['rainfall_mm']:.1f}mm | Flood Depth: {row['flood_depth_cm']:.1f}cm")
            report.append(f"    Temperature: {row['temperature_c']:.1f}°C")
    
    # Recommendations by Risk Level
    report.append("\n\nRECOMMENDATIONS")
    report.append("-" * 80)
    
    for risk_level in ['High', 'Medium', 'Low']:
        report.append(f"\n{risk_level.upper()} RISK AREAS:")
        recommendations = get_risk_recommendations(risk_level)
        for rec in recommendations:
            report.append(f"  • {rec}")
    
    # Conclusion
    report.append("\n\nCONCLUSION")
    report.append("-" * 80)
    if risk_summary.get('High', 0) > 0:
        report.append("⚠️ IMMEDIATE ACTION REQUIRED: High-risk zones have been identified.")
        report.append("Implement emergency protocols and activate response teams immediately.")
    elif risk_summary.get('Medium', 0) > 0:
        report.append("⚠️ PRECAUTIONARY MEASURES RECOMMENDED: Medium-risk zones require close monitoring.")
        report.append("Prepare infrastructure and maintain heightened alertness.")
    else:
        report.append("✅ SITUATION STABLE: Current conditions indicate low risk across all monitored areas.")
        report.append("Continue routine monitoring and maintain preventive measures.")
    
    report.append("\n" + "=" * 80)
    
    return "\n".join(report)

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

st.sidebar.title("🌍 Climate Risk Assessment")
st.sidebar.markdown("---")

# File upload
uploaded_file = st.sidebar.file_uploader(
    "📤 Upload CSV File",
    type=['csv'],
    help="Upload a CSV with columns: date, location, rainfall_mm, flood_depth_cm, temperature_c"
)

# Display repository info
st.sidebar.markdown("---")
st.sidebar.info(
    "📍 **Repository**: msc-020-22/Climate-risk-AI\n\n"
    "🚀 This app helps assess climate-related risks and provides actionable recommendations."
)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

st.title("🌍 Climate Risk Assessment Dashboard")
st.markdown("Comprehensive climate risk analysis and visualization platform")

if uploaded_file is None:
    # Welcome Screen
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Welcome to the Climate Risk Assessment Tool
        
        This application helps you:
        - **📊 Analyze** climate data from your location
        - **⚠️ Identify** high-risk zones requiring immediate action
        - **📈 Track** rainfall and flood trends
        - **🗺️ Visualize** risks on an interactive map
        - **📋 Generate** professional risk reports
        
        ### 📋 Required CSV Columns
        Your CSV file should contain:
        - `date`: Date of observation
        - `location`: Name of the location
        - `rainfall_mm`: Rainfall in millimeters
        - `flood_depth_cm`: Flood depth in centimeters
        - `temperature_c`: Temperature in Celsius
        
        Optional columns:
        - `lat`, `longitude`: Latitude (or `latitude`)
        - `lon`: Longitude
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Risk Categories
        
        **🔴 HIGH RISK**
        - Rainfall > 100mm OR Flood depth > 50cm
        - **Action**: Immediate emergency response
        
        **🟡 MEDIUM RISK**
        - Rainfall 50-100mm OR Flood depth 20-50cm
        - **Action**: Enhanced monitoring required
        
        **🟢 LOW RISK**
        - Rainfall < 50mm AND Flood depth < 20cm
        - **Action**: Routine monitoring
        
        ### 📝 Sample Data Format
        ```
        date,location,rainfall_mm,flood_depth_cm,temperature_c
        2024-01-01,Zone A,120.5,65.3,28.5
        2024-01-01,Zone B,45.2,18.9,25.3
        ```
        """)
    
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "<p>👈 Use the sidebar to upload your CSV file and get started</p>"
        "</div>",
        unsafe_allow_html=True
    )

else:
    # File Processing and Analysis
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        
        # Validate columns
        is_valid, validation_msg, available_cols = validate_csv_columns(df)
        
        if not is_valid:
            st.error(f"❌ {validation_msg}")
            st.info("Please ensure your CSV has the required columns: date, location, rainfall_mm, flood_depth_cm, temperature_c")
        else:
            # Normalize column names to lowercase
            df.columns = [col.lower().strip() for col in df.columns]
            
            # Ensure numeric columns are numeric
            numeric_cols = ['rainfall_mm', 'flood_depth_cm', 'temperature_c']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Convert date column
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            
            # Generate lat/lon if not provided
            df = generate_lat_lon_for_demo(df)
            
            # Calculate risk levels
            df['risk_level'] = df.apply(
                lambda row: categorize_risk(row['rainfall_mm'], row['flood_depth_cm']),
                axis=1
            )
            
            # ================================================================
            # SECTION 1: DATA PREVIEW
            # ================================================================
            st.markdown("<div class='section-header'>📊 Data Preview & Summary</div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df), "rows")
            with col2:
                st.metric("Unique Locations", df['location'].nunique(), "locations")
            with col3:
                st.metric("Date Range", f"{df['date'].min().date()} to {df['date'].max().date()}")
            
            # Data preview with expander
            with st.expander("📋 View First 5 Rows", expanded=False):
                st.dataframe(df.head(), use_container_width=True)
            
            # Basic Statistics
            st.markdown("#### Statistical Summary")
            
            stats_cols = st.columns(len(numeric_cols))
            for idx, col_name in enumerate(numeric_cols):
                with stats_cols[idx]:
                    col_data = df[col_name]
                    st.markdown(f"**{col_name.replace('_', ' ').title()}**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"Min: {col_data.min():.2f}")
                    with col2:
                        st.write(f"Mean: {col_data.mean():.2f}")
                    with col3:
                        st.write(f"Max: {col_data.max():.2f}")
            
            # ================================================================
            # SECTION 2: RISK ANALYSIS SUMMARY
            # ================================================================
            st.markdown("<div class='section-header'>⚠️ Risk Summary & Analysis</div>", unsafe_allow_html=True)
            
            # Calculate risk counts
            risk_counts = df['risk_level'].value_counts()
            risk_summary = risk_counts.to_dict()
            
            # Risk metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(
                    f"<div class='metric-card high-risk'>"
                    f"<div style='font-size: 28px; font-weight: bold; color: #ef553b;'>{risk_summary.get('High', 0)}</div>"
                    f"<div style='color: #666; font-size: 14px;'>HIGH RISK</div>"
                    f"<div style='color: #999; font-size: 12px;'>{risk_summary.get('High', 0)/len(df)*100:.1f}% of total</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    f"<div class='metric-card medium-risk'>"
                    f"<div style='font-size: 28px; font-weight: bold; color: #ffa15a;'>{risk_summary.get('Medium', 0)}</div>"
                    f"<div style='color: #666; font-size: 14px;'>MEDIUM RISK</div>"
                    f"<div style='color: #999; font-size: 12px;'>{risk_summary.get('Medium', 0)/len(df)*100:.1f}% of total</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            with col3:
                st.markdown(
                    f"<div class='metric-card low-risk'>"
                    f"<div style='font-size: 28px; font-weight: bold; color: #00cc96;'>{risk_summary.get('Low', 0)}</div>"
                    f"<div style='color: #666; font-size: 14px;'>LOW RISK</div>"
                    f"<div style='color: #999; font-size: 12px;'>{risk_summary.get('Low', 0)/len(df)*100:.1f}% of total</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            with col4:
                st.markdown(
                    f"<div class='metric-card'>"
                    f"<div style='font-size: 28px; font-weight: bold; color: #636EFA;'>{risk_summary.get('Unknown', 0)}</div>"
                    f"<div style='color: #666; font-size: 14px;'>UNKNOWN</div>"
                    f"<div style='color: #999; font-size: 12px;'>{risk_summary.get('Unknown', 0)/len(df)*100:.1f}% of total</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            # Risk distribution pie chart
            risk_distribution = df['risk_level'].value_counts()
            fig_pie = go.Figure(data=[go.Pie(
                labels=risk_distribution.index,
                values=risk_distribution.values,
                marker=dict(colors=['#ef553b', '#ffa15a', '#00cc96', '#636EFA']),
                textposition='inside',
                textinfo='label+percent'
            )])
            fig_pie.update_layout(
                title="Risk Distribution Across Locations",
                height=400,
                showlegend=True
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # ================================================================
            # SECTION 3: TREND ANALYSIS
            # ================================================================
            st.markdown("<div class='section-header'>📈 Trend Analysis</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Rainfall trend
                slope, r_sq, trend_text = calculate_trend(df, 'date', 'rainfall_mm')
                st.markdown(f"**Rainfall Trend**: {trend_text}")
                st.caption(f"R² value: {r_sq:.4f}")
                
                # Create trend visualization
                df_sorted = df.sort_values('date')
                fig_rain = px.scatter(
                    df_sorted,
                    x='date',
                    y='rainfall_mm',
                    color='risk_level',
                    color_discrete_map={'High': '#ef553b', 'Medium': '#ffa15a', 'Low': '#00cc96', 'Unknown': '#636EFA'},
                    title="Rainfall Over Time",
                    labels={'rainfall_mm': 'Rainfall (mm)', 'date': 'Date'}
                )
                
                # Add trend line
                if slope != 0:
                    x_trend = np.arange(len(df_sorted))
                    y_trend = slope * x_trend + (df_sorted['rainfall_mm'].mean() - slope * len(df_sorted) / 2)
                    fig_rain.add_scatter(
                        x=df_sorted['date'],
                        y=y_trend,
                        mode='lines',
                        name='Trend',
                        line=dict(color='red', width=2, dash='dash')
                    )
                
                fig_rain.update_layout(height=400)
                st.plotly_chart(fig_rain, use_container_width=True)
            
            with col2:
                # Flood depth trend
                slope_flood, r_sq_flood, trend_text_flood = calculate_trend(df, 'date', 'flood_depth_cm')
                st.markdown(f"**Flood Depth Trend**: {trend_text_flood}")
                st.caption(f"R² value: {r_sq_flood:.4f}")
                
                # Create flood depth visualization
                fig_flood = px.scatter(
                    df_sorted,
                    x='date',
                    y='flood_depth_cm',
                    color='risk_level',
                    color_discrete_map={'High': '#ef553b', 'Medium': '#ffa15a', 'Low': '#00cc96', 'Unknown': '#636EFA'},
                    title="Flood Depth Over Time",
                    labels={'flood_depth_cm': 'Flood Depth (cm)', 'date': 'Date'}
                )
                
                # Add trend line
                if slope_flood != 0:
                    x_trend = np.arange(len(df_sorted))
                    y_trend = slope_flood * x_trend + (df_sorted['flood_depth_cm'].mean() - slope_flood * len(df_sorted) / 2)
                    fig_flood.add_scatter(
                        x=df_sorted['date'],
                        y=y_trend,
                        mode='lines',
                        name='Trend',
                        line=dict(color='red', width=2, dash='dash')
                    )
                
                fig_flood.update_layout(height=400)
                st.plotly_chart(fig_flood, use_container_width=True)
            
            # ================================================================
            # SECTION 4: HIGH-RISK ZONES
            # ================================================================
            st.markdown("<div class='section-header'>🚨 High-Risk Zones</div>", unsafe_allow_html=True)
            
            high_risk_df = df[df['risk_level'] == 'High'].sort_values('rainfall_mm', ascending=False)
            
            if len(high_risk_df) > 0:
                st.warning(f"⚠️ {len(high_risk_df)} locations flagged as HIGH RISK")
                
                # Display high-risk table
                display_cols = ['location', 'date', 'rainfall_mm', 'flood_depth_cm', 'temperature_c', 'risk_level']
                st.dataframe(high_risk_df[display_cols], use_container_width=True)
                
                # High-risk recommendations
                st.markdown("#### 🎯 Recommended Actions for High-Risk Areas:")
                recommendations = get_risk_recommendations('High')
                for i, rec in enumerate(recommendations, 1):
                    st.markdown(f"{i}. {rec}")
            
            else:
                st.success("✅ No locations currently in HIGH RISK category")
            
            # ================================================================
            # SECTION 5: INTERACTIVE MAP
            # ================================================================
            st.markdown("<div class='section-header'>🗺️ Interactive Risk Map</div>", unsafe_allow_html=True)
            
            st.info("🗺️ Green = Low Risk | Yellow = Medium Risk | Red = High Risk | Blue = Unknown")
            
            try:
                risk_map = create_risk_map(df, 'location', 'lat', 'lon', 'risk_level')
                st_folium(risk_map, width=1200, height=500)
            except Exception as e:
                st.error(f"Error creating map: {str(e)}")
            
            # ================================================================
            # SECTION 6: DETAILED ANALYSIS BY LOCATION
            # ================================================================
            st.markdown("<div class='section-header'>🔍 Detailed Location Analysis</div>", unsafe_allow_html=True)
            
            selected_location = st.selectbox(
                "Select a location for detailed analysis",
                df['location'].unique()
            )
            
            location_data = df[df['location'] == selected_location]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Current Risk Level",
                    location_data.iloc[-1]['risk_level'],
                    delta=None,
                    delta_color="off"
                )
            with col2:
                st.metric(
                    "Latest Rainfall",
                    f"{location_data.iloc[-1]['rainfall_mm']:.1f} mm"
                )
            with col3:
                st.metric(
                    "Latest Flood Depth",
                    f"{location_data.iloc[-1]['flood_depth_cm']:.1f} cm"
                )
            
            # Display location data
            st.markdown(f"#### Historical Data for {selected_location}")
            st.dataframe(location_data, use_container_width=True)
            
            # Location recommendations
            current_risk = location_data.iloc[-1]['risk_level']
            st.markdown(f"#### Recommendations for {current_risk} Risk Level:")
            for rec in get_risk_recommendations(current_risk):
                st.markdown(f"• {rec}")
            
            # ================================================================
            # SECTION 7: REPORT GENERATION
            # ================================================================
            st.markdown("<div class='section-header'>📋 Report Generation</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(
                    "Generate a comprehensive report with executive summary, "
                    "high-risk locations, and actionable recommendations."
                )
            
            with col2:
                if st.button("📄 Generate Report", use_container_width=True):
                    report_text = generate_report(df, risk_summary)
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Report (.txt)",
                        data=report_text,
                        file_name=f"climate_risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Display report preview
                    st.markdown("#### Report Preview:")
                    st.text(report_text)
            
            # ================================================================
            # SECTION 8: EXPORT DATA
            # ================================================================
            st.markdown("<div class='section-header'>📤 Export Data</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Export analyzed data
                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                
                st.download_button(
                    label="📊 Download Analyzed Data (CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"climate_risk_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Export high-risk zones only
                if len(high_risk_df) > 0:
                    csv_high_risk = io.StringIO()
                    high_risk_df.to_csv(csv_high_risk, index=False)
                    
                    st.download_button(
                        label="🚨 Download High-Risk Data (CSV)",
                        data=csv_high_risk.getvalue(),
                        file_name=f"climate_risk_high_risk_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Please ensure your CSV file is properly formatted and contains all required columns.")

# ================================================================
# FOOTER
# ================================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #999; font-size: 12px;'>"
    "<p>Climate Risk Assessment Dashboard | "
    "msc-020-22/Climate-risk-AI | "
    f"{datetime.now().year}</p>"
    "</div>",
    unsafe_allow_html=True
)
