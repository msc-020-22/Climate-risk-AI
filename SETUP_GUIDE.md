# Climate Risk Assessment - Setup Guide

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/msc-020-22/Climate-risk-AI.git
cd Climate-risk-AI
```

### Step 2: Create Virtual Environment
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
streamlit run climate_app.py
```

The app will open automatically at `http://localhost:8501`

---

## 📊 Using the Application

### 1. Upload Your Data
- Click the file uploader in the sidebar
- Select your CSV file (see **Data Format** section below)

### 2. View Data Preview
- See the first 5 rows of your data
- Check min, max, and mean values for numeric columns

### 3. Analyze Risk Levels
- View risk distribution across locations
- See high, medium, and low risk zone counts

### 4. Explore Trends
- Check if rainfall is increasing or decreasing
- View flood depth trends over time

### 5. Review High-Risk Zones
- See detailed list of high-risk locations
- Get specific recommendations for each zone

### 6. Visualize on Map
- Interactive map with color-coded risk markers
- Click markers to see location details

### 7. Generate Report
- Click "Generate Report" button
- Download professional text report

### 8. Export Data
- Download analyzed data as CSV
- Download high-risk zones separately

---

## 📋 Data Format

### Required Columns
```
date             → Date (any standard format: YYYY-MM-DD, MM/DD/YYYY, etc.)
location         → Location name (string)
rainfall_mm      → Rainfall in millimeters (numeric)
flood_depth_cm   → Flood depth in centimeters (numeric)
temperature_c    → Temperature in Celsius (numeric)
```

### Optional Columns
```
lat, latitude    → Latitude coordinate (numeric)
lon, longitude   → Longitude coordinate (numeric)
```

### Example CSV
```csv
date,location,rainfall_mm,flood_depth_cm,temperature_c
2024-01-01,Zone A,125.5,65.3,28.5
2024-01-01,Zone B,45.2,18.9,25.3
2024-01-02,Zone A,95.0,42.1,29.2
```

A sample file `sample_climate_data.csv` is included for testing.

---

## 🔍 Understanding Risk Levels

### High Risk 🔴
- **Criteria**: Rainfall > 100mm OR Flood depth > 50cm
- **Actions**:
  - Install flood barriers
  - Establish early warning systems
  - Evacuate vulnerable populations
  - Activate emergency protocols

### Medium Risk 🟡
- **Criteria**: Rainfall 50-100mm OR Flood depth 20-50cm
- **Actions**:
  - Monitor conditions closely
  - Maintain drainage infrastructure
  - Prepare emergency channels
  - Increase monitoring

### Low Risk 🟢
- **Criteria**: Rainfall < 50mm AND Flood depth < 20cm
- **Actions**:
  - Continue routine monitoring
  - Track trends
  - Regular inspections
  - Maintain documentation

---

## 📞 Support & Feedback

- Report issues: Open an issue on GitHub
- Questions: Check the README.md
- Feature requests: Submit as GitHub issue

Good luck! 🌍
