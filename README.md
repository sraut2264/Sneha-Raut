# 🏦 European Bank Customer Churn Analysis Dashboard

A comprehensive Streamlit web application for analyzing European Bank customer churn data.

## 📋 Features

- **📈 Overview Tab**: Dataset summary, statistics, and data types
- **📊 Distributions Tab**: Visualize distributions of numeric and categorical features
- **🔗 Relationships Tab**: Scatter plots and correlation heatmaps
- **📉 Churn Analysis Tab**: In-depth analysis of customer churn patterns
- **🔍 Data Explorer Tab**: Search, filter, and export data

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Navigate to the project directory:
```bash
cd "c:\Users\PRADEEP\Desktop\New folder"
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

### Running the App

Execute the following command:
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 📊 Tabs Overview

### 1. Overview
- Total customer count and churn metrics
- Sample data display
- Statistical summaries
- Data types overview

### 2. Distributions
- Interactive histograms, box plots, and violin plots
- Numeric feature analysis
- Categorical feature value counts
- Distribution comparisons

### 3. Relationships
- Scatter plot analysis with interactive controls
- Correlation matrix heatmap
- Multi-feature relationship exploration
- Color coding by churn status

### 4. Churn Analysis
- Churn rate metrics
- Churn distribution by numeric features
- Churn rate by categorical features
- Detailed summary tables

### 5. Data Explorer
- Full dataset browser
- Text search functionality
- Custom row filtering
- CSV and Excel export options

## 📁 Files

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `European_Bank .. vs churn.xlsx` - Dataset file

## 🛠️ Customization

You can modify the app by:
- Adding new visualizations in any tab
- Adjusting the color schemes in CSS
- Adding machine learning models for predictions
- Creating custom metrics

## 📊 Dataset Information

The European Bank customer churn dataset typically includes:
- Customer demographics (age, gender, location)
- Account information (balance, tenure, products)
- Activity metrics (transactions, interactions)
- Churn status (whether the customer left)

## 💡 Tips

- Use the sidebar filters for quick dataset information
- Click on legends to toggle data series on/off in charts
- Hover over data points for detailed information
- Use the search feature in Data Explorer for quick lookups
- Export data for further analysis in Excel or Python

## 🐛 Troubleshooting

**App not starting?**
- Ensure all packages are installed: `pip install -r requirements.txt`
- Check that Excel file is in the same directory as app.py

**Missing data visualizations?**
- Verify the Excel file format is correct
- Ensure column names match expected patterns (e.g., 'Exited' for churn)

## 📝 Notes

- Large datasets may take a few seconds to load initially
- Data is cached for better performance
- All charts are interactive and can be zoomed/panned

## 🔗 Requirements

- Streamlit 1.28.1+
- Pandas 2.0.3+
- Plotly 5.17.0+
- NumPy 1.24.3+

---

**Version**: 1.0  
**Last Updated**: May 2026
