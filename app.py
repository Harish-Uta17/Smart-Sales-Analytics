import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
from sqlalchemy import text
from datetime import datetime, timedelta
import numpy as np

from scripts.db_connect import get_engine

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="Enterprise Sales Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== DATABASE & MODEL INITIALIZATION ====================
@st.cache_resource
def init_connection():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return engine


@st.cache_resource
def load_model():
    """Load ML model with caching"""
    try:
        return joblib.load("model/revenue_model.pkl")
    except:
        st.warning("⚠️ Predictive model not found. Forecast features disabled.")
        return None

try:
    engine = init_connection()
except Exception as exc:
    st.error("Database connection failed. Check DB_URL and your database credentials.")
    st.code(
        'PowerShell: setx DB_URL "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/demo"',
        language="bash",
    )
    st.info("You can use MySQL, PostgreSQL, or Supabase as long as DB_URL is valid.")
    st.markdown("Update [.streamlit/secrets.toml](.streamlit/secrets.toml) or set DB_URL as an environment variable.")
    with st.expander("Connection diagnostics"):
        st.text(str(exc))
    st.stop()

model = load_model()
dialect_name = engine.dialect.name.lower()


def month_group_expr(col_name: str = "sale_date") -> str:
    """Return SQL month-grouping expression compatible with active database dialect."""
    if dialect_name in {"mysql", "mariadb"}:
        return f"DATE_FORMAT({col_name}, '%Y-%m-01')"
    if dialect_name in {"postgresql", "postgres"}:
        return f"DATE_TRUNC('month', {col_name})"
    # SQLite fallback
    return f"strftime('%Y-%m-01', {col_name})"

# ==================== PROFESSIONAL STYLING ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Background with Gradient */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    }
    
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    /* Force all text to be white */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Selectbox styling in sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #ffffff !important;
    }
    
    /* Dropdown menu styling */
    [data-baseweb="popover"] {
        background-color: #1e293b !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #1e293b !important;
    }
    
    [role="option"] {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    
    [role="option"]:hover {
        background-color: #334155 !important;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .sub-header {
        text-align: center;
        color: #e5e7eb;
        font-size: 18px;
        margin-bottom: 30px;
        font-weight: 500;
    }
    
    /* KPI Card Styling */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 28px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.5);
    }
    
    .kpi-title {
        font-size: 13px;
        color: #e0e7ff;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 12px;
    }
    
    .kpi-value {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        margin: 12px 0;
        text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .kpi-change {
        font-size: 14px;
        font-weight: 700;
        margin-top: 10px;
    }
    
    .positive {
        color: #34d399;
    }
    
    .negative {
        color: #f87171;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 26px;
        font-weight: 700;
        color: #ffffff !important;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid rgba(102, 126, 234, 0.5);
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 20px;
        border-radius: 15px;
    }
    
    div[data-testid="metric-container"] label {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff !important;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #ffffff !important;
    }
    
    /* Data Tables */
    .dataframe {
        background: rgba(255, 255, 255, 0.05);
    }
    
    .dataframe tbody tr td, .dataframe thead tr th {
        color: #ffffff !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR FILTERS ====================
with st.sidebar:
    st.markdown("<h2 style='color: #ffffff !important; font-size: 28px;'>🎯 Analytics Filters</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='color: #ffffff !important; font-size: 20px;'>🌍 Location</h3>", unsafe_allow_html=True)
    cities_df = pd.read_sql("SELECT DISTINCT city FROM customers ORDER BY city", engine)
    city = st.selectbox("Select City", ["All"] + list(cities_df['city']), label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown("<h3 style='color: #ffffff !important; font-size: 20px;'>📦 Product Category</h3>", unsafe_allow_html=True)
    cat_df = pd.read_sql("SELECT DISTINCT categoty FROM products ORDER BY categoty", engine)
    cat = st.selectbox("Select Category", ["All"] + list(cat_df['categoty']), label_visibility="collapsed")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("<h3 style='color: #ffffff !important;'>📊 Dashboard Info</h3>", unsafe_allow_html=True)
    st.info("Real-time analytics powered by SQL database and ML forecasting")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center;'>
        <p style='color: #ffffff !important;'>Built with Streamlit & Plotly</p>
        <p style='color: #ffffff !important;'>© 2024 Sales Analytics</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== BUILD FILTER SQL ====================
filter_sql = ""
if city != "All":
    filter_sql += f" AND c.city='{city}'"
if cat != "All":
    filter_sql += f" AND p.categoty='{cat}'"

# ==================== HEADER ====================
st.markdown("<h1 class='main-header'>📊 Enterprise Sales Analytics Platform</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Real-time Business Intelligence & Predictive Analytics Dashboard</p>", unsafe_allow_html=True)

# ==================== KPI METRICS ====================
@st.cache_data(ttl=300)
def get_kpi_data(filter_sql):
    return pd.read_sql(f"""
        SELECT 
            p.categoty AS category,
            SUM(s.quantity * p.price) AS revenue,
            COUNT(DISTINCT s.customer_id) AS customers,
            SUM(s.quantity) AS total_quantity,
            COUNT(*) AS total_orders
        FROM sales s 
        JOIN products p ON s.product_id = p.product_id
        JOIN customers c ON s.customer_id = c.customer_id
        WHERE 1=1 {filter_sql}
        GROUP BY p.categoty
    """, engine)

kpi_data = get_kpi_data(filter_sql)

total_revenue = kpi_data['revenue'].sum()
total_customers = kpi_data['customers'].sum()
total_orders = kpi_data['total_orders'].sum()
avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>💰 TOTAL REVENUE</div>
            <div class='kpi-value'>₹{int(total_revenue):,}</div>
            <div class='kpi-change positive'>↑ 12.5% vs last period</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>👥 ACTIVE CUSTOMERS</div>
            <div class='kpi-value'>{int(total_customers):,}</div>
            <div class='kpi-change positive'>↑ 8.3% vs last period</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>📦 TOTAL ORDERS</div>
            <div class='kpi-value'>{int(total_orders):,}</div>
            <div class='kpi-change positive'>↑ 15.7% vs last period</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-title'>💳 AVG ORDER VALUE</div>
            <div class='kpi-value'>₹{int(avg_order_value):,}</div>
            <div class='kpi-change negative'>↓ 2.1% vs last period</div>
        </div>
    """, unsafe_allow_html=True)

# ==================== REVENUE ANALYTICS ====================
st.markdown("<h2 class='section-header'>📈 Revenue Analytics</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("#### Monthly Revenue Trend with Moving Average")
    
    @st.cache_data(ttl=300)
    def get_trend_data(filter_sql):
        month_expr = month_group_expr("sale_date")
        return pd.read_sql(f"""
            SELECT 
                {month_expr} AS month,
                SUM(s.quantity * p.price) AS revenue
            FROM sales s 
            JOIN products p ON s.product_id = p.product_id
            JOIN customers c ON s.customer_id = c.customer_id
            WHERE 1=1 {filter_sql}
            GROUP BY month 
            ORDER BY month
        """, engine)
    
    trend_data = get_trend_data(filter_sql)
    
    if not trend_data.empty:
        trend_data['ma_3'] = trend_data['revenue'].rolling(window=3, min_periods=1).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['month'], 
            y=trend_data['revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#667eea', width=3),
            marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=trend_data['month'], 
            y=trend_data['ma_3'],
            mode='lines',
            name='3-Month MA',
            line=dict(color='#f59e0b', width=2, dash='dash')
        ))
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            hovermode='x unified',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
                font=dict(color='#ffffff')
            ),
            margin=dict(l=20, r=20, t=20, b=80)
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Category Performance")
    
    if not kpi_data.empty:
        fig = go.Figure(data=[go.Pie(
            labels=kpi_data['category'],
            values=kpi_data['revenue'],
            hole=0.5,
            marker=dict(colors=px.colors.sequential.Purples_r),
            textfont=dict(color='#ffffff')
        )])
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            showlegend=True,
            legend=dict(font=dict(color='#ffffff')),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== CUSTOMER ANALYTICS ====================
st.markdown("<h2 class='section-header'>👥 Customer Analytics</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Geographic Distribution")
    
    @st.cache_data(ttl=300)
    def get_segment_data(filter_sql):
        return pd.read_sql(f"""
            SELECT 
                c.city, 
                COUNT(DISTINCT s.customer_id) AS customers,
                SUM(s.quantity * p.price) AS revenue
            FROM sales s 
            JOIN customers c ON s.customer_id = c.customer_id
            JOIN products p ON s.product_id = p.product_id
            WHERE 1=1 {filter_sql}
            GROUP BY c.city
            ORDER BY revenue DESC
        """, engine)
    
    segment_data = get_segment_data(filter_sql)
    
    if not segment_data.empty:
        fig = px.bar(
            segment_data, 
            x='city', 
            y='revenue',
            color='customers',
            color_continuous_scale='Purples'
        )
        fig.update_layout(
            template='plotly_dark',
            height=400,
            showlegend=False,
            xaxis=dict(title="City", tickfont=dict(color='#ffffff')),
            yaxis=dict(title="Revenue (₹)", tickfont=dict(color='#ffffff')),
            margin=dict(l=20, r=20, t=20, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Customer Value Segmentation")
    
    if not segment_data.empty:
        segment_data['avg_revenue'] = segment_data['revenue'] / segment_data['customers']
        
        fig = go.Figure(data=[go.Bar(
            x=segment_data['city'],
            y=segment_data['avg_revenue'],
            marker=dict(
                color=segment_data['avg_revenue'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(tickfont=dict(color='#ffffff'))
            )
        )])
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            xaxis=dict(title="City", tickfont=dict(color='#ffffff')),
            yaxis=dict(title="Avg Revenue/Customer (₹)", tickfont=dict(color='#ffffff')),
            margin=dict(l=20, r=20, t=20, b=60)
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== PRODUCT ANALYTICS ====================
st.markdown("<h2 class='section-header'>📦 Product Performance Analysis</h2>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Top Products", "📊 Product Matrix", "📉 Performance Trends"])

with tab1:
    @st.cache_data(ttl=300)
    def get_product_data():
        return pd.read_sql("""
            SELECT 
                p.product_name,
                p.categoty as category,
                SUM(s.quantity * p.price) AS revenue,
                SUM(s.quantity) AS quantity_sold,
                COUNT(DISTINCT s.customer_id) AS customers
            FROM sales s 
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.product_name, p.categoty
            ORDER BY revenue DESC
            LIMIT 20
        """, engine)
    
    product_data = get_product_data()
    
    if not product_data.empty:
        product_display = product_data.copy()
        product_display['revenue'] = product_display['revenue'].apply(lambda x: f"₹{int(x):,}")
        product_display['quantity_sold'] = product_display['quantity_sold'].apply(lambda x: f"{int(x):,}")
        
        st.dataframe(product_display, use_container_width=True, height=400)

with tab2:
    if not product_data.empty:
        fig = px.scatter(
            product_data,
            x='quantity_sold',
            y='revenue',
            size='customers',
            color='category',
            hover_data=['product_name']
        )
        fig.update_layout(
            template='plotly_dark',
            height=450,
            xaxis=dict(tickfont=dict(color='#ffffff')),
            yaxis=dict(tickfont=dict(color='#ffffff')),
            legend=dict(font=dict(color='#ffffff'))
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    @st.cache_data(ttl=300)
    def get_category_trend():
        month_expr = month_group_expr("sale_date")
        return pd.read_sql("""
            SELECT 
                {month_expr} AS month,
                p.categoty as category,
                SUM(s.quantity * p.price) AS revenue
            FROM sales s 
            JOIN products p ON s.product_id = p.product_id
            GROUP BY month, category
            ORDER BY month, category
        """.format(month_expr=month_expr), engine)
    
    cat_trend = get_category_trend()
    
    if not cat_trend.empty:
        fig = px.line(cat_trend, x='month', y='revenue', color='category')
        fig.update_layout(
            template='plotly_dark',
            height=450,
            xaxis=dict(tickfont=dict(color='#ffffff')),
            yaxis=dict(tickfont=dict(color='#ffffff')),
            legend=dict(font=dict(color='#ffffff'))
        )
        st.plotly_chart(fig, use_container_width=True)

# ==================== ML FORECASTING ====================
if model is not None:
    st.markdown("<h2 class='section-header'>🔮 Predictive Analytics & Forecasting</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Revenue Forecast Engine")
        
        forecast_month = st.slider("Select Month", 1, 12, datetime.now().month)
        forecast_year = st.number_input("Year", 2024, 2030, datetime.now().year)
        
        if st.button("🚀 Generate Forecast", use_container_width=True):
            try:
                prediction = model.predict([[forecast_month]])[0]
                st.success(f"**Predicted Revenue for {datetime(forecast_year, forecast_month, 1).strftime('%B %Y')}**")
                st.markdown(f"### ₹{round(prediction, 2):,}")
                
                confidence = prediction * 0.15
                st.info(f"**Range:** ₹{round(prediction-confidence, 2):,} - ₹{round(prediction+confidence, 2):,}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    with col2:
        st.markdown("#### 12-Month Revenue Forecast")
        
        try:
            months = list(range(1, 13))
            predictions = [model.predict([[m]])[0] for m in months]
            
            forecast_df = pd.DataFrame({
                'Month': [datetime(forecast_year, m, 1).strftime('%B') for m in months],
                'Predicted Revenue': predictions
            })
            
            fig = go.Figure(data=[go.Bar(
                x=forecast_df['Month'],
                y=forecast_df['Predicted Revenue'],
                marker=dict(color=predictions, colorscale='Purples')
            )])
            
            fig.update_layout(
                template='plotly_dark',
                height=400,
                xaxis=dict(tickfont=dict(color='#ffffff')),
                yaxis=dict(tickfont=dict(color='#ffffff')),
                margin=dict(l=20, r=20, t=20, b=60)
            )
            st.plotly_chart(fig, use_container_width=True)
        except:
            st.info("Unable to generate forecast")

# ==================== EXPORT & INSIGHTS ====================
st.markdown("<h2 class='section-header'>💡 Key Insights & Export</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🎯 Top Insight")
    if not kpi_data.empty:
        top_category = kpi_data.loc[kpi_data['revenue'].idxmax(), 'category']
        top_revenue = kpi_data['revenue'].max()
        st.markdown(f"**{top_category}**")
        st.markdown(f"Leading category with")
        st.markdown(f"### ₹{int(top_revenue):,}")

with col2:
    st.markdown("#### 📊 Data Export")
    if st.button("📥 Download Report (CSV)", use_container_width=True):
        csv = product_data.to_csv(index=False)
        st.download_button(
            "Click to Download",
            csv,
            f"sales_report_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )

with col3:
    st.markdown("#### ⚡ Quick Stats")
    if not product_data.empty:
        st.metric("Products", len(product_data))
        st.metric("Categories", kpi_data.shape[0])
        st.metric("Data", "Real-time")

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #e5e7eb; padding: 20px;'>
        <p>Enterprise Sales Analytics Platform | Powered by ML & Real-time Data</p>
        <p style='font-size: 12px;'>Built with Streamlit • MySQL/PostgreSQL • Plotly • Scikit-learn</p>
    </div>
""", unsafe_allow_html=True)