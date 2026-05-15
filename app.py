import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="European Bank Churn Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('European_Bank .. vs churn.xlsx')
    return df

try:
    df = load_data()
    st.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Title
st.title("🏦 European Bank Customer Churn Analysis")
st.markdown("---")

# Sidebar filters
st.sidebar.title("📊 Filters & Options")

# Display basic info
with st.sidebar.expander("📋 Dataset Info", expanded=True):
    st.metric("Total Records", len(df))
    st.metric("Total Columns", len(df.columns))
    st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

# Display columns info
st.sidebar.markdown("### Column Information")
with st.sidebar.expander("📚 View Columns"):
    st.write("**Dataset Columns:**")
    for i, col in enumerate(df.columns, 1):
        dtype = df[col].dtype
        non_null = df[col].notna().sum()
        st.write(f"{i}. **{col}** ({dtype}) - {non_null}/{len(df)} non-null")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overview", 
    "📊 Distributions", 
    "🔗 Relationships", 
    "📉 Churn Analysis",
    "🔍 Data Explorer"
])

# TAB 1: Overview
with tab1:
    st.header("Dataset Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Customers", len(df), delta=None)
    with col2:
        if 'Exited' in df.columns or 'churn' in df.columns.str.lower():
            churn_col = 'Exited' if 'Exited' in df.columns else [c for c in df.columns if 'churn' in c.lower()][0]
            churned = (df[churn_col] == 1).sum()
            st.metric("Churned Customers", churned, delta=f"{(churned/len(df)*100):.1f}%")
    with col3:
        retained = len(df) - (df[churn_col].sum() if 'churn_col' in locals() else 0)
        st.metric("Retained Customers", retained)
    
    st.markdown("---")
    
    # Display first rows
    st.subheader("Sample Data")
    st.dataframe(df.head(10), use_container_width=True)
    
    st.markdown("---")
    
    # Statistical Summary
    st.subheader("Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)
    
    # Data types summary
    st.subheader("Data Types Summary")
    dtype_summary = pd.DataFrame({
        'Data Type': df.dtypes.value_counts().index,
        'Count': df.dtypes.value_counts().values
    })
    st.dataframe(dtype_summary, use_container_width=True)

# TAB 2: Distributions
with tab2:
    st.header("Feature Distributions")
    
    # Numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        st.subheader("Numeric Features Distribution")
        
        col1, col2 = st.columns(2)
        selected_col = col1.selectbox("Select numeric column", numeric_cols)
        chart_type = col2.selectbox("Chart type", ["Histogram", "Box Plot", "Violin Plot"])
        
        if chart_type == "Histogram":
            fig = px.histogram(df, x=selected_col, nbins=30, 
                              title=f"Distribution of {selected_col}",
                              labels={selected_col: selected_col})
        elif chart_type == "Box Plot":
            fig = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
        else:
            fig = px.violin(df, y=selected_col, title=f"Violin Plot of {selected_col}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Multiple distributions
        st.subheader("All Numeric Features Distributions")
        cols_per_row = 2
        for i in range(0, len(numeric_cols), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(numeric_cols):
                    col_name = numeric_cols[i + j]
                    with col:
                        fig = px.histogram(df, x=col_name, nbins=20, 
                                         title=f"{col_name}",
                                         template="plotly_white")
                        st.plotly_chart(fig, use_container_width=True)
    
    # Categorical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if categorical_cols:
        st.subheader("Categorical Features Distribution")
        
        selected_cat = st.selectbox("Select categorical column", categorical_cols)
        
        fig = px.bar(df[selected_cat].value_counts().reset_index(),
                    x='count', y=selected_cat, orientation='h',
                    title=f"Distribution of {selected_cat}",
                    labels={'count': 'Count', selected_cat: selected_cat})
        st.plotly_chart(fig, use_container_width=True)

# TAB 3: Relationships
with tab3:
    st.header("Feature Relationships")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) >= 2:
        st.subheader("Scatter Plot Analysis")
        col1, col2 = st.columns(2)
        
        x_col = col1.selectbox("X-axis", numeric_cols, key="scatter_x")
        y_col = col2.selectbox("Y-axis", numeric_cols, key="scatter_y", index=1 if len(numeric_cols) > 1 else 0)
        
        # Color by churn if available
        color_col = None
        if 'Exited' in df.columns:
            color_col = 'Exited'
        elif any('churn' in c.lower() for c in df.columns):
            color_col = [c for c in df.columns if 'churn' in c.lower()][0]
        
        if color_col:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                           title=f"{x_col} vs {y_col} (colored by {color_col})",
                           hover_data=df.columns[:10].tolist())
        else:
            fig = px.scatter(df, x=x_col, y=y_col,
                           title=f"{x_col} vs {y_col}",
                           hover_data=df.columns[:10].tolist())
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("Correlation Matrix")
        
        corr_matrix = df[numeric_cols].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values,
            texttemplate='%{text:.2f}',
            textfont={"size": 10},
            hovertemplate='%{x} vs %{y}: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(width=800, height=800, title="Feature Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True)

# TAB 4: Churn Analysis
with tab4:
    st.header("Churn Analysis")
    
    # Find churn column
    churn_col = None
    if 'Exited' in df.columns:
        churn_col = 'Exited'
    elif any('churn' in c.lower() for c in df.columns):
        churn_col = [c for c in df.columns if 'churn' in c.lower()][0]
    
    if churn_col:
        # Churn rate
        churn_rate = (df[churn_col] == 1).sum() / len(df) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Churn Rate (%)", f"{churn_rate:.2f}%")
        with col2:
            st.metric("Churned", (df[churn_col] == 1).sum())
        with col3:
            st.metric("Retained", (df[churn_col] == 0).sum())
        
        st.markdown("---")
        
        # Churn by numeric features
        st.subheader("Churn Analysis by Features")
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        selected_feature = st.selectbox("Select feature to analyze", numeric_cols)
        
        # Create bins for numeric features
        fig = px.histogram(df, x=selected_feature, color=churn_col,
                          barmode='group', nbins=20,
                          title=f"Churn Distribution by {selected_feature}",
                          labels={churn_col: f"{churn_col} Status"})
        st.plotly_chart(fig, use_container_width=True)
        
        # Categorical analysis
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if categorical_cols:
            st.subheader("Churn Rate by Categorical Features")
            
            col1, col2 = st.columns([1, 3])
            selected_cat = col1.selectbox("Select categorical feature", categorical_cols)
            
            churn_by_cat = df.groupby(selected_cat)[churn_col].apply(
                lambda x: (x == 1).sum() / len(x) * 100
            ).reset_index()
            churn_by_cat.columns = [selected_cat, 'Churn Rate (%)']
            
            fig = px.bar(churn_by_cat, x=selected_cat, y='Churn Rate (%)',
                        title=f"Churn Rate by {selected_cat}",
                        text='Churn Rate (%)')
            fig.update_traces(texttemplate='%{text:.1f}%', textposition='auto')
            st.plotly_chart(fig, use_container_width=True)
            
            # Table summary
            st.dataframe(churn_by_cat, use_container_width=True)
    else:
        st.warning("No churn column found in dataset. Please ensure data contains churn/exit information.")

# TAB 5: Data Explorer
with tab5:
    st.header("Data Explorer")
    
    # Search and filter
    st.subheader("Search & Filter Data")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("Search in all columns")
    
    with col2:
        rows_to_show = st.number_input("Rows to display", min_value=5, max_value=1000, value=50)
    
    filtered_df = df.copy()
    
    if search_term:
        mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        filtered_df = df[mask]
        st.info(f"Found {len(filtered_df)} matching records")
    
    # Display filtered data
    st.dataframe(filtered_df.head(rows_to_show), use_container_width=True)
    
    # Download option
    st.subheader("Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name="churn_data.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        with open('temp.xlsx', 'rb') as f:
            st.download_button(
                label="📥 Download as Excel",
                data=f.read(),
                file_name="churn_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center">
    <p style="color: gray; font-size: 12px;">
    📊 European Bank Churn Analysis Dashboard | Data Explorer
    </p>
</div>
""", unsafe_allow_html=True)
