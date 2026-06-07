# Climate Risk Assessment Application

A professional **Streamlit web application** for comprehensive climate risk assessment, analysis, and visualization.

## 🎯 Features

### 📊 Data Management
- **CSV File Upload**: Upload climate data with flexible column naming
- **Data Validation**: Automatic validation and error handling for missing columns
- **Data Preview**: View first 5 rows and comprehensive statistical summaries
- **Automatic Coordinate Generation**: Generate demo coordinates if not provided

### ⚠️ Risk Categorization
- **High Risk**: Rainfall > 100mm OR Flood depth > 50cm
- **Medium Risk**: Rainfall 50-100mm OR Flood depth 20-50cm
- **Low Risk**: Rainfall < 50mm AND Flood depth < 20cm

### 📈 Analysis & Visualization
- **Risk Distribution**: Pie charts showing location breakdown by risk level
- **Trend Analysis**: Linear regression analysis for rainfall and flood depth trends
- **Time Series Charts**: Interactive Plotly visualizations with trend lines
- **Statistical Summary**: Min, max, mean for all numeric columns

### 🗺️ Interactive Mapping
- **Folium Maps**: Color-coded markers (Red=High, Yellow=Medium, Green=Low)
- **Location Popups**: Click markers to see detailed location information
- **Responsive Design**: Works with any geographic data

### 🚨 High-Risk Zone Identification
- **Automatic Detection**: Identifies all locations flagged as high-risk
- **Customized Recommendations**: Specific action items for high-risk areas
- **Data Export**: Download high-risk zones separately

### 📋 Professional Report Generation
- **Executive Summary**: Risk counts and percentages
- **Key Statistics**: Rainfall, flood depth, and temperature statistics
- **High-Risk Details**: Detailed information on critical zones
- **Actionable Recommendations**: Customized by risk level
- **Download Support**: Export reports as .txt files

### 📤 Data Export
- **Analyzed Data Export**: Download full analysis results as CSV
- **High-Risk Export**: Download only high-risk locations
- **Report Export**: Generate and download professional text reports

## 📋 Required CSV Columns

```
date                    # Date of observation (any standard date format)
location               # Name of the location/zone
rainfall_mm            # Rainfall in millimeters
flood_depth_cm         # Flood depth in centimeters
temperature_c          # Temperature in Celsius
```

### Optional Columns
```
lat, latitude          # Latitude coordinate
lon, longitude         # Longitude coordinate
```

If latitude/longitude are not provided, the app generates random demo coordinates.

## 📝 Sample CSV Format

```csv
date,location,rainfall_mm,flood_depth_cm,temperature_c
2024-01-01,Zone A,120.5,65.3,28.5
2024-01-01,Zone B,45.2,18.9,25.3
2024-01-02,Zone A,95.0,42.1,29.2
2024-01-02,Zone B,30.5,12.4,26.1
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/msc-020-22/Climate-risk-AI.git
cd Climate-risk-AI
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🎮 Running the Application

```bash
streamlit run climate_app.py
```

The application will open in your default browser at `http://localhost:8501`

## 📚 Application Structure

### Main Sections

1. **Sidebar** - File upload and repository information
2. **Welcome Screen** - Introduction and instructions (before file upload)
3. **Data Preview** - First 5 rows and statistical summaries
4. **Risk Summary** - Metric cards and distribution pie charts
5. **Trend Analysis** - Time series visualizations with trend lines
6. **High-Risk Zones** - Detailed table and recommendations
7. **Interactive Map** - Folium-based geographic visualization
8. **Detailed Analysis** - Location-specific historical data
9. **Report Generation** - Professional report with download
10. **Data Export** - CSV download options

## 🎨 UI/UX Features

- **Professional Styling**: Custom CSS with color-coded risk levels
- **Expandable Sections**: Use expanders for detailed data without clutter
- **Responsive Layout**: Multi-column layouts that adapt to screen size
- **Color Coding**: 
  - 🔴 Red (#ef553b) = High Risk
  - 🟡 Yellow (#ffa15a) = Medium Risk
  - 🟢 Green (#00cc96) = Low Risk
- **Metric Cards**: Visual indicators for risk counts and percentages
- **Interactive Charts**: Hover, zoom, and interact with Plotly visualizations

## 🔍 Key Functions

### Risk Categorization
```python
def categorize_risk(rainfall_mm, flood_depth_cm)
```
Determines risk level based on rainfall and flood depth thresholds.

### Trend Analysis
```python
def calculate_trend(df, date_col, value_col)
```
Calculates linear regression to identify increasing/decreasing trends.

### Report Generation
```python
def generate_report(df, risk_summary)
```
Creates comprehensive text report with recommendations.

### Interactive Mapping
```python
def create_risk_map(df, location_col, lat_col, lon_col, risk_col)
```
Generates Folium map with color-coded risk markers.

## 📊 Analysis Outputs

### Risk Summary Metrics
- Total locations analyzed
- Count of high/medium/low risk zones
- Percentage distribution

### Trend Information
- Slope of linear regression
- R-squared value
- Trend direction (increasing/decreasing/stable)

### High-Risk Details
- Location names
- Latest sensor readings
- Recommended actions

### Export Formats
- CSV (full analysis, high-risk zones only)
- TXT (professional reports)

## ⚙️ Error Handling

- **Missing Columns**: Clear error message with column requirements
- **Invalid Data Types**: Automatic conversion with error handling
- **Empty DataFrames**: Graceful handling with user guidance
- **Map Errors**: Fallback with error messages
- **File Format**: CSV validation before processing

## 🔧 Customization

### Modify Risk Thresholds
Edit the `categorize_risk()` function:
```python
def categorize_risk(rainfall_mm, flood_depth_cm):
    if rainfall_mm > 100 or flood_depth_cm > 50:
        return 'High'
    # ... etc
```

### Change Colors
Update the `get_risk_color()` function:
```python
colors = {
    'High': '#ef553b',
    'Medium': '#ffa15a',
    'Low': '#00cc96'
}
```

### Update Recommendations
Modify the `get_risk_recommendations()` function to add new action items.

## 📦 Dependencies

- **streamlit**: Web framework
- **streamlit-folium**: Folium integration
- **pandas**: Data processing
- **numpy**: Numerical operations
- **scipy**: Scientific computing (trend analysis)
- **plotly**: Interactive visualizations
- **folium**: Geographic mapping

## 📄 License

MIT License - See LICENSE file for details

## 👤 Author

**msc-020-22 Jonathan zimunya** - Climate Risk Assessment Project

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🗓️ Version History

### v1.0.0 (2024)
- Initial release
- CSV upload and validation
- Risk categorization
- Interactive visualizations
- Report generation
- Data export functionality

---

**Climate Risk Assessment Dashboard** - Making climate data accessible and actionable 🌍
