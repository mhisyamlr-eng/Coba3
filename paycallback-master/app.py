"""
Paycol Dashboard - Enhanced Complete Single File Application
====================================================
Dashboard aplikasi untuk manajemen Payment Collection (Paycol) dengan multi-level user access.

Version: 2.0.0
Date: 2025

Features:
- Multi-level user authentication
- Data dummy generator
- Excel download functionality
- Red theme color palette
- Bug fixes and improvements

Usage:
    streamlit run paycol_dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pathlib import Path
import io
import random

# ============================================================================
# CONFIGURATION & CUSTOM CSS
# ============================================================================

st.set_page_config(
    page_title="Paycol Dashboard",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS dengan Red Theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Color Palette Variables */
    :root {
        --primary-red: #D32F2F;
        --dark-red: #B71C1C;
        --light-red: #FF6659;
        --secondary-red: #C62828;
        --success-green: #43A047;
        --warning-yellow: #FBC02D;
        --error-red: #D50000;
        --bg-white: #FFFFFF;
        --bg-light: #F5F5F5;
        --bg-lighter: #FAFAFA;
        --text-primary: #212121;
        --text-secondary: #757575;
        --border-color: #E0E0E0;
    }
    
    /* Global Font */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main App Background */
    .stApp {
        background-color: var(--bg-light);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-red) 0%, var(--primary-red) 100%);
        box-shadow: 2px 0 10px rgba(0,0,0,0.1);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: rgba(255, 255, 255, 0.2);
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(255, 255, 255, 0.3);
        border-color: white;
    }
    
    /* Headers */
    h1 {
        color: var(--dark-red) !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: var(--primary-red) !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
    }
    
    h3 {
        color: var(--secondary-red) !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--primary-red);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.8rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(211, 47, 47, 0.2);
    }
    
    .stButton > button:hover {
        background-color: var(--light-red);
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(211, 47, 47, 0.2);
    }
    
    /* Download Button Specific */
    .stDownloadButton > button {
        background-color: var(--success-green);
        color: white;
    }
    
    .stDownloadButton > button:hover {
        background-color: #388E3C;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: var(--primary-red) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-weight: 600 !important;
    }
    
    /* Metric Container */
    [data-testid="metric-container"] {
        background-color: var(--bg-white);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid var(--primary-red);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: var(--bg-white);
        padding: 0.8rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary);
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(211, 47, 47, 0.05);
        color: var(--primary-red);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--primary-red);
        color: white !important;
        border-color: var(--primary-red);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input,
    .stTextArea textarea {
        border: 2px solid var(--border-color);
        border-radius: 8px;
        transition: all 0.3s ease;
        padding: 0.6rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary-red);
        box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
        outline: none;
    }
    
    /* Success Messages */
    .stSuccess {
        background-color: rgba(67, 160, 71, 0.1);
        border-left: 4px solid var(--success-green);
        color: #2E7D32;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Warning Messages */
    .stWarning {
        background-color: rgba(251, 192, 45, 0.1);
        border-left: 4px solid var(--warning-yellow);
        color: #F57F17;
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Error Messages */
    .stError {
        background-color: rgba(213, 0, 0, 0.1);
        border-left: 4px solid var(--error-red);
        color: var(--error-red);
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* Info Messages */
    .stInfo {
        background-color: rgba(211, 47, 47, 0.1);
        border-left: 4px solid var(--primary-red);
        color: var(--primary-red);
        padding: 1rem;
        border-radius: 8px;
    }
    
    /* DataFrames */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .dataframe thead tr th {
        background-color: var(--dark-red) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 14px !important;
        text-align: left !important;
        border: none !important;
    }
    
    .dataframe tbody tr {
        transition: background-color 0.2s ease;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: var(--bg-lighter);
    }
    
    .dataframe tbody tr:hover {
        background-color: rgba(211, 47, 47, 0.05);
    }
    
    .dataframe tbody td {
        padding: 12px !important;
        border: none !important;
        border-bottom: 1px solid var(--border-color) !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--bg-white);
        border: 2px solid var(--border-color);
        border-radius: 10px;
        color: var(--text-primary);
        font-weight: 600;
        padding: 1rem;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--primary-red);
        background-color: rgba(211, 47, 47, 0.02);
    }
    
    .streamlit-expanderContent {
        border: 2px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 1rem;
        background-color: var(--bg-white);
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 2px solid var(--primary-red);
        opacity: 0.3;
        margin: 2rem 0;
    }
    
    /* Form */
    [data-testid="stForm"] {
        background-color: var(--bg-white);
        border-radius: 12px;
        padding: 2rem;
        border: 2px solid var(--border-color);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* Charts */
    .js-plotly-plot {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        background-color: var(--bg-white);
        padding: 1rem;
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: var(--primary-red);
        color: white;
    }
    
    /* Selectbox Dropdown */
    [data-baseweb="popover"] {
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Login Form */
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# UTILITY CLASSES
# ============================================================================

class ExcelHandler:
    """Handler untuk operasi Excel dengan perbaikan"""
    
    def __init__(self):
        self.data_path = Path(__file__).parent / 'data'
        self.data_path.mkdir(exist_ok=True)
        
    def read_excel(self, filename):
        """Baca file Excel"""
        try:
            filepath = self.data_path / filename
            if filepath.exists():
                df = pd.read_excel(filepath)
                return df
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Error reading {filename}: {e}")
            return pd.DataFrame()
    
    def write_excel(self, df, filename):
        """Tulis ke file Excel"""
        try:
            filepath = self.data_path / filename
            df.to_excel(filepath, index=False)
            return True
        except Exception as e:
            st.error(f"Error writing {filename}: {e}")
            return False
    
    def append_row(self, filename, new_row):
        """Tambah baris baru ke Excel"""
        try:
            df = self.read_excel(filename)
            
            if df.empty:
                df = pd.DataFrame([new_row])
            else:
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            return self.write_excel(df, filename)
        except Exception as e:
            st.error(f"Error appending to {filename}: {e}")
            return False
    
    def update_row(self, filename, condition, updates):
        """Update baris berdasarkan kondisi"""
        try:
            df = self.read_excel(filename)
            
            if df.empty:
                return False
            
            mask = pd.Series([True] * len(df))
            for col, val in condition.items():
                if col in df.columns:
                    mask &= (df[col] == val)
            
            for col, val in updates.items():
                if col in df.columns:
                    df.loc[mask, col] = val
            
            return self.write_excel(df, filename)
        except Exception as e:
            st.error(f"Error updating {filename}: {e}")
            return False
    
    def delete_row(self, filename, condition):
        """Hapus baris berdasarkan kondisi"""
        try:
            df = self.read_excel(filename)
            
            if df.empty:
                return False
            
            mask = pd.Series([True] * len(df))
            for col, val in condition.items():
                if col in df.columns:
                    mask &= (df[col] == val)
            
            df = df[~mask]
            
            return self.write_excel(df, filename)
        except Exception as e:
            st.error(f"Error deleting from {filename}: {e}")
            return False

# ============================================================================
# DATA DUMMY GENERATOR
# ============================================================================

def generate_dummy_data():
    """Generate data dummy untuk testing"""
    excel = ExcelHandler()
    
    # Data Users
    users_data = pd.DataFrame({
        'username': ['admin', 'paycol_reg', 'paycol_witel', 'mgmt_sss', 'mgmt_nonsss', 'guest'],
        'password': ['admin123', 'reg123', 'witel123', 'sss123', 'nonsss123', 'guest123'],
        'role': ['Admin Aplikasi', 'Admin Paycol Reg', 'Admin Paycol Witel', 
                 'Management SSS', 'Management Non SSS', 'Guest'],
        'regional': ['Nasional', 'Regional 1', 'Witel Jakarta Selatan', 'Nasional', 'Nasional', 'Guest'],
        'status': ['Active'] * 6
    })
    excel.write_excel(users_data, 'users.xlsx')
    
    # Data Performansi CR
    regional_list = ['Regional 1', 'Regional 2', 'Regional 3', 'Regional 4', 'Regional 5']
    segmen_list = ['SSS', 'Non SSS', 'Consumer']
    witel_list = ['Witel Jakarta Selatan', 'Witel Jakarta Barat', 'Witel Bandung', 
                  'Witel Surabaya', 'Witel Medan', 'Witel Makassar']
    
    performansi_data = []
    for regional in regional_list:
        for segmen in segmen_list:
            for witel in witel_list:
                total_tagihan = random.randint(500000000, 2000000000)
                total_bayar = int(total_tagihan * random.uniform(0.75, 0.95))
                
                performansi_data.append({
                    'regional': regional,
                    'segmen': segmen,
                    'witel': witel,
                    'total_tagihan': total_tagihan,
                    'total_bayar': total_bayar,
                    'cr_persen': round((total_bayar / total_tagihan * 100), 2),
                    'bulan': 'Januari 2025',
                    'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
    
    df_performansi = pd.DataFrame(performansi_data)
    excel.write_excel(df_performansi, 'performansi_cr.xlsx')
    
    # Data Tunggakan
    tunggakan_data = []
    status_list = ['Belum Bayar', 'Sebagian', 'Follow Up']
    am_list = ['John Doe', 'Jane Smith', 'Bob Wilson', 'Alice Brown', 'Charlie Davis']
    
    for i in range(100):
        id_pelanggan = f"CUST{str(i+1).zfill(5)}"
        nama_pelanggan = f"PT Company {i+1}"
        segmen = random.choice(segmen_list)
        regional = random.choice(regional_list)
        witel = random.choice(witel_list)
        jumlah_tunggakan = random.randint(5000000, 500000000)
        status = random.choice(status_list)
        am = random.choice(am_list)
        
        tunggakan_data.append({
            'id_pelanggan': id_pelanggan,
            'nama_pelanggan': nama_pelanggan,
            'segmen': segmen,
            'regional': regional,
            'witel': witel,
            'jumlah_tunggakan': jumlah_tunggakan,
            'status': status,
            'am': am,
            'last_update': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
            'keterangan': f'Customer {segmen} - {status}'
        })
    
    df_tunggakan = pd.DataFrame(tunggakan_data)
    excel.write_excel(df_tunggakan, 'tunggakan.xlsx')
    
    return True

# ============================================================================
# DOWNLOAD FUNCTIONS
# ============================================================================

def convert_df_to_excel(df):
    """Convert DataFrame to Excel bytes"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    output.seek(0)
    return output.getvalue()

# ============================================================================
# AUTHENTICATION MODULE
# ============================================================================

def authenticate(username, password):
    """Authenticate user credentials"""
    try:
        excel = ExcelHandler()
        df_users = excel.read_excel('users.xlsx')
        
        if df_users.empty:
            create_default_users()
            df_users = excel.read_excel('users.xlsx')
        
        user = df_users[(df_users['username'] == username) & 
                        (df_users['password'] == password)]
        
        if not user.empty:
            return {
                'success': True,
                'role': user.iloc[0]['role'],
                'user_data': user.iloc[0].to_dict()
            }
        else:
            return {
                'success': False,
                'role': None,
                'user_data': None
            }
    except Exception as e:
        st.error(f"Error in authentication: {e}")
        return {
            'success': False,
            'role': None,
            'user_data': None
        }

def create_default_users():
    """Create default users.xlsx if not exists"""
    excel = ExcelHandler()
    
    default_users = pd.DataFrame({
        'username': ['admin', 'paycol_reg', 'paycol_witel', 'mgmt_sss', 'mgmt_nonsss', 'guest'],
        'password': ['admin123', 'reg123', 'witel123', 'sss123', 'nonsss123', 'guest123'],
        'role': ['Admin Aplikasi', 'Admin Paycol Reg', 'Admin Paycol Witel', 
                 'Management SSS', 'Management Non SSS', 'Guest'],
        'regional': ['Nasional', 'Regional 1', 'Witel Jakarta Selatan', 'Nasional', 'Nasional', 'Guest'],
        'status': ['Active'] * 6
    })
    
    excel.write_excel(default_users, 'users.xlsx')

# ============================================================================
# ADMIN APLIKASI MODULE
# ============================================================================

def show_admin_aplikasi():
    """Dashboard Admin Aplikasi - Performansi CR"""
    
    st.title("📊 Performansi CR Dashboard")
    st.markdown("### Admin Aplikasi - Collection Rate Performance")
    
    excel = ExcelHandler()
    
    # Action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        if st.button("🎲 Generate Data Dummy", use_container_width=True):
            with st.spinner("Generating dummy data..."):
                if generate_dummy_data():
                    st.success("✅ Data dummy berhasil dibuat!")
                    st.rerun()
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Nasional", "🗺️ Regional", "🏢 Per Segmen", 
        "📍 Per Witel", "🔍 GAP Detail"
    ])
    
    with tab1:
        show_nasional_view(excel)
    
    with tab2:
        show_regional_view(excel)
    
    with tab3:
        show_segmen_view(excel)
    
    with tab4:
        show_witel_view(excel)
    
    with tab5:
        show_gap_detail(excel)

def show_nasional_view(excel):
    """View Performansi CR Nasional"""
    st.subheader("Performansi CR Nasional")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Grab dari MyBrain", key="grab_nasional", use_container_width=True):
            st.success("✅ Data berhasil di-grab dari MyBrain!")
    
    df = excel.read_excel('performansi_cr.xlsx')
    
    if not df.empty:
        # Download button
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="📥 Download Data Nasional",
            data=excel_data,
            file_name=f"performansi_cr_nasional_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=False
        )
        
        st.markdown("---")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_tagihan = df['total_tagihan'].sum() if 'total_tagihan' in df.columns else 0
        total_bayar = df['total_bayar'].sum() if 'total_bayar' in df.columns else 0
        cr_rate = (total_bayar / total_tagihan * 100) if total_tagihan > 0 else 0
        tunggakan = total_tagihan - total_bayar
        
        with col1:
            st.metric("Total Tagihan", f"Rp {total_tagihan/1e9:.2f}M")
        with col2:
            st.metric("Total Pembayaran", f"Rp {total_bayar/1e9:.2f}M")
        with col3:
            st.metric("Collection Rate", f"{cr_rate:.2f}%", 
                     delta=f"{cr_rate - 85:.2f}%" if cr_rate > 85 else f"{cr_rate - 85:.2f}%")
        with col4:
            st.metric("Tunggakan", f"Rp {tunggakan/1e9:.2f}M")
        
        st.markdown("---")
        
        # Trend Chart
        st.subheader("Trend Collection Rate")
        
        # Generate trend data from actual data
        if 'bulan' in df.columns:
            trend_data = df.groupby('bulan').agg({
                'total_tagihan': 'sum',
                'total_bayar': 'sum'
            }).reset_index()
            trend_data['CR (%)'] = (trend_data['total_bayar'] / trend_data['total_tagihan'] * 100)
        else:
            # Default trend
            trend_data = pd.DataFrame({
                'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun'],
                'CR (%)': [82, 85, 83, 87, 86, 88]
            })
        
        fig = px.line(trend_data, x=trend_data.columns[0], y='CR (%)', 
                     title='Trend CR 6 Bulan Terakhir',
                     markers=True)
        fig.update_traces(line_color='#D32F2F', marker=dict(size=10, color='#B71C1C'))
        fig.update_layout(
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212121'),
            xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Data Table
        st.subheader("Data Detail")
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("📊 Belum ada data. Klik tombol 'Generate Data Dummy' atau 'Grab dari MyBrain' untuk mengambil data.")

def show_regional_view(excel):
    """View Performansi CR per Regional"""
    st.subheader("Performansi CR per Regional")
    
    df = excel.read_excel('performansi_cr.xlsx')
    
    if not df.empty and 'regional' in df.columns:
        regional_data = df.groupby('regional').agg({
            'total_tagihan': 'sum',
            'total_bayar': 'sum'
        }).reset_index()
        
        regional_data['CR (%)'] = (regional_data['total_bayar'] / 
                                    regional_data['total_tagihan'] * 100).round(2)
        regional_data['Tunggakan'] = regional_data['total_tagihan'] - regional_data['total_bayar']
        
        # Download button
        excel_data = convert_df_to_excel(regional_data)
        st.download_button(
            label="📥 Download Data Regional",
            data=excel_data,
            file_name=f"performansi_cr_regional_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("---")
        
        # Bar Chart
        fig = px.bar(regional_data, x='regional', y='CR (%)',
                    title='Collection Rate per Regional',
                    color='CR (%)',
                    color_continuous_scale=['#B71C1C', '#D32F2F', '#FF6659'],
                    text='CR (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212121'),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Data Table with formatting
        st.subheader("Data Detail Regional")
        display_df = regional_data.copy()
        display_df['total_tagihan'] = display_df['total_tagihan'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['total_bayar'] = display_df['total_bayar'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['Tunggakan'] = display_df['Tunggakan'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.info("📊 Data regional belum tersedia.")

def show_segmen_view(excel):
    """View Performansi CR per Segmen"""
    st.subheader("Performansi CR per Segmen")
    
    df = excel.read_excel('performansi_cr.xlsx')
    
    if not df.empty and 'segmen' in df.columns:
        segmen_data = df.groupby('segmen').agg({
            'total_tagihan': 'sum',
            'total_bayar': 'sum'
        }).reset_index()
        
        segmen_data['CR (%)'] = (segmen_data['total_bayar'] / 
                                  segmen_data['total_tagihan'] * 100).round(2)
        segmen_data['Tunggakan'] = segmen_data['total_tagihan'] - segmen_data['total_bayar']
        
        # Download button
        excel_data = convert_df_to_excel(segmen_data)
        st.download_button(
            label="📥 Download Data Segmen",
            data=excel_data,
            file_name=f"performansi_cr_segmen_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Pie Chart
            fig1 = px.pie(segmen_data, values='total_tagihan', names='segmen',
                        title='Distribusi Tagihan per Segmen',
                        color_discrete_sequence=['#D32F2F', '#C62828', '#B71C1C', '#FF6659'])
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            fig1.update_layout(
                height=400,
                paper_bgcolor='white',
                font=dict(color='#212121')
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Bar Chart CR
            fig2 = px.bar(segmen_data, x='segmen', y='CR (%)',
                         title='Collection Rate per Segmen',
                         color='CR (%)',
                         color_continuous_scale=['#B71C1C', '#D32F2F', '#FF6659'],
                         text='CR (%)')
            fig2.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig2.update_layout(
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='#212121'),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        
        # Data Table
        st.subheader("Data Detail Segmen")
        display_df = segmen_data.copy()
        display_df['total_tagihan'] = display_df['total_tagihan'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['total_bayar'] = display_df['total_bayar'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['Tunggakan'] = display_df['Tunggakan'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True, height=300)
    else:
        st.info("📊 Data segmen belum tersedia.")

def show_witel_view(excel):
    """View Performansi CR per Witel"""
    st.subheader("Performansi CR per Witel")
    
    df = excel.read_excel('performansi_cr.xlsx')
    
    if not df.empty and 'witel' in df.columns:
        witel_data = df.groupby('witel').agg({
            'total_tagihan': 'sum',
            'total_bayar': 'sum'
        }).reset_index()
        
        witel_data['CR (%)'] = (witel_data['total_bayar'] / 
                                 witel_data['total_tagihan'] * 100).round(2)
        witel_data['Tunggakan'] = witel_data['total_tagihan'] - witel_data['total_bayar']
        
        # Sort by CR descending
        witel_data = witel_data.sort_values('CR (%)', ascending=False)
        
        # Download button
        excel_data = convert_df_to_excel(witel_data)
        st.download_button(
            label="📥 Download Data Witel",
            data=excel_data,
            file_name=f"performansi_cr_witel_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("---")
        
        # Horizontal Bar Chart
        fig = px.bar(witel_data.head(10), y='witel', x='CR (%)',
                    title='Top 10 Witel - Collection Rate',
                    color='CR (%)',
                    color_continuous_scale=['#B71C1C', '#D32F2F', '#FF6659'],
                    orientation='h',
                    text='CR (%)')
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(
            height=500,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(color='#212121'),
            xaxis=dict(showgrid=True, gridcolor='#E0E0E0'),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Data Table
        st.subheader("Data Detail Witel")
        display_df = witel_data.copy()
        display_df['total_tagihan'] = display_df['total_tagihan'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['total_bayar'] = display_df['total_bayar'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['Tunggakan'] = display_df['Tunggakan'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.info("📊 Data witel belum tersedia.")

def show_gap_detail(excel):
    """View GAP Detail dengan navigasi"""
    st.subheader("GAP Detail Navigation")
    
    df = excel.read_excel('performansi_cr.xlsx')
    
    if not df.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            regional_list = ["Semua"] + sorted(df['regional'].unique().tolist()) if 'regional' in df.columns else ["Semua"]
            regional_filter = st.selectbox("Filter Regional", regional_list)
        
        with col2:
            segmen_list = ["Semua"] + sorted(df['segmen'].unique().tolist()) if 'segmen' in df.columns else ["Semua"]
            segmen_filter = st.selectbox("Filter Segmen", segmen_list)
        
        with col3:
            witel_list = ["Semua"] + sorted(df['witel'].unique().tolist()) if 'witel' in df.columns else ["Semua"]
            witel_filter = st.selectbox("Filter Witel", witel_list)
        
        with col4:
            cr_threshold = st.number_input("CR < (%)", min_value=0, max_value=100, value=85, step=5)
        
        # Apply filters
        filtered_df = df.copy()
        if regional_filter != "Semua" and 'regional' in df.columns:
            filtered_df = filtered_df[filtered_df['regional'] == regional_filter]
        if segmen_filter != "Semua" and 'segmen' in df.columns:
            filtered_df = filtered_df[filtered_df['segmen'] == segmen_filter]
        if witel_filter != "Semua" and 'witel' in df.columns:
            filtered_df = filtered_df[filtered_df['witel'] == witel_filter]
        
        # Calculate CR and filter by threshold
        if 'cr_persen' in filtered_df.columns:
            filtered_df = filtered_df[filtered_df['cr_persen'] < cr_threshold]
        
        st.markdown("---")
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Jumlah GAP", len(filtered_df))
        with col2:
            total_gap = (filtered_df['total_tagihan'].sum() - filtered_df['total_bayar'].sum()) if len(filtered_df) > 0 else 0
            st.metric("Total GAP", f"Rp {total_gap/1e9:.2f}M")
        with col3:
            avg_cr = filtered_df['cr_persen'].mean() if len(filtered_df) > 0 and 'cr_persen' in filtered_df.columns else 0
            st.metric("Rata-rata CR", f"{avg_cr:.2f}%")
        
        st.markdown("---")
        
        if not filtered_df.empty:
            # Download button
            excel_data = convert_df_to_excel(filtered_df)
            st.download_button(
                label="📥 Download Data GAP",
                data=excel_data,
                file_name=f"gap_detail_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.dataframe(filtered_df, use_container_width=True, height=500)
        else:
            st.success("✅ Tidak ada GAP yang ditemukan dengan kriteria filter saat ini.")
    else:
        st.info("📊 Data GAP belum tersedia.")

# ============================================================================
# ADMIN PAYCOL REGIONAL MODULE
# ============================================================================

def show_admin_paycol_reg():
    """Dashboard Admin Paycol Regional - Tunggakan"""
    
    st.title("💰 Tunggakan Dashboard")
    st.markdown("### Admin Paycol Regional - Pengelolaan Tunggakan")
    
    excel = ExcelHandler()
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", "🔍 Detail Pelanggan", 
        "✏️ Update Status", "👤 Update AM"
    ])
    
    with tab1:
        show_tunggakan_overview(excel)
    
    with tab2:
        show_detail_pelanggan(excel)
    
    with tab3:
        show_update_status_tunggakan(excel)
    
    with tab4:
        show_update_am(excel)

def show_tunggakan_overview(excel):
    """Overview Tunggakan"""
    st.subheader("Overview Tunggakan")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Grab dari MyBrain", key="grab_tunggakan", use_container_width=True):
            st.success("✅ Data tunggakan berhasil di-grab!")
    
    df = excel.read_excel('tunggakan.xlsx')
    
    if not df.empty:
        # Download button
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="📥 Download Data Tunggakan",
            data=excel_data,
            file_name=f"tunggakan_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("---")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_tunggakan = df['jumlah_tunggakan'].sum() if 'jumlah_tunggakan' in df.columns else 0
        jumlah_pelanggan = len(df)
        rata_tunggakan = total_tunggakan / jumlah_pelanggan if jumlah_pelanggan > 0 else 0
        status_lunas = len(df[df['status'] == 'Lunas']) if 'status' in df.columns else 0
        
        with col1:
            st.metric("Total Tunggakan", f"Rp {total_tunggakan/1e9:.2f}M")
        with col2:
            st.metric("Jumlah Pelanggan", f"{jumlah_pelanggan:,}")
        with col3:
            st.metric("Rata-rata Tunggakan", f"Rp {rata_tunggakan/1e6:.2f}M")
        with col4:
            persen_lunas = (status_lunas/jumlah_pelanggan*100) if jumlah_pelanggan > 0 else 0
            st.metric("Sudah Lunas", f"{status_lunas}", delta=f"{persen_lunas:.1f}%")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Chart by Segmen
            if 'segmen' in df.columns:
                st.subheader("Tunggakan per Segmen")
                segmen_data = df.groupby('segmen')['jumlah_tunggakan'].sum().reset_index()
                
                fig1 = px.bar(segmen_data, x='segmen', y='jumlah_tunggakan',
                            title='Distribusi Tunggakan per Segmen',
                            color='jumlah_tunggakan',
                            color_continuous_scale=['#FF6659', '#D32F2F', '#B71C1C'])
                fig1.update_layout(
                    height=350,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#212121'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Chart by Status
            if 'status' in df.columns:
                st.subheader("Distribusi Status")
                status_data = df['status'].value_counts().reset_index()
                status_data.columns = ['Status', 'Jumlah']
                
                fig2 = px.pie(status_data, values='Jumlah', names='Status',
                            title='Distribusi Status Pembayaran',
                            color_discrete_sequence=['#D32F2F', '#FF6659', '#C62828', '#B71C1C'])
                fig2.update_traces(textposition='inside', textinfo='percent+label')
                fig2.update_layout(
                    height=350,
                    paper_bgcolor='white',
                    font=dict(color='#212121')
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Data Tunggakan")
        
        # Format currency columns
        display_df = df.copy()
        if 'jumlah_tunggakan' in display_df.columns:
            display_df['jumlah_tunggakan_formatted'] = display_df['jumlah_tunggakan'].apply(lambda x: f"Rp {x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True, height=400)
    else:
        st.info("📊 Belum ada data tunggakan. Klik 'Generate Data Dummy' di menu Admin Aplikasi.")

def show_detail_pelanggan(excel):
    """Detail Pelanggan dengan Navigasi"""
    st.subheader("Detail Pelanggan")
    
    df = excel.read_excel('tunggakan.xlsx')
    
    if not df.empty:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search_query = st.text_input("🔍 Cari ID/Nama Pelanggan", 
                                        placeholder="Masukkan ID atau nama...")
        
        with col2:
            segmen_list = ["Semua"] + sorted(df['segmen'].unique().tolist()) if 'segmen' in df.columns else ["Semua"]
            segmen_filter = st.selectbox("Filter Segmen", segmen_list)
        
        with col3:
            status_list = ["Semua"] + sorted(df['status'].unique().tolist()) if 'status' in df.columns else ["Semua"]
            status_filter = st.selectbox("Filter Status", status_list)
        
        # Apply filters
        filtered_df = df.copy()
        
        if search_query:
            mask = (
                filtered_df['id_pelanggan'].astype(str).str.contains(search_query, case=False, na=False) |
                filtered_df['nama_pelanggan'].astype(str).str.contains(search_query, case=False, na=False)
            )
            filtered_df = filtered_df[mask]
        
        if segmen_filter != "Semua" and 'segmen' in df.columns:
            filtered_df = filtered_df[filtered_df['segmen'] == segmen_filter]
        
        if status_filter != "Semua" and 'status' in df.columns:
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        st.markdown("---")
        st.write(f"**Menampilkan {len(filtered_df)} dari {len(df)} data**")
        
        if not filtered_df.empty:
            # Download filtered data
            excel_data = convert_df_to_excel(filtered_df)
            st.download_button(
                label="📥 Download Data Filtered",
                data=excel_data,
                file_name=f"pelanggan_filtered_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.markdown("---")
            
            # Display as expandable cards
            for idx, row in filtered_df.head(20).iterrows():
                status_color = {
                    'Lunas': '🟢',
                    'Sebagian': '🟡',
                    'Belum Bayar': '🔴',
                    'Follow Up': '🟠'
                }.get(row.get('status', ''), '⚪')
                
                with st.expander(f"{status_color} {row['id_pelanggan']} - {row['nama_pelanggan']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Segmen:** {row.get('segmen', '-')}")
                        st.write(f"**Regional:** {row.get('regional', '-')}")
                        st.write(f"**Witel:** {row.get('witel', '-')}")
                        st.write(f"**Jumlah Tunggakan:** Rp {row.get('jumlah_tunggakan', 0):,.0f}")
                    
                    with col2:
                        st.write(f"**Status:** {row.get('status', '-')}")
                        st.write(f"**Account Manager:** {row.get('am', '-')}")
                        st.write(f"**Update Terakhir:** {row.get('last_update', '-')}")
                        st.write(f"**Keterangan:** {row.get('keterangan', '-')}")
            
            if len(filtered_df) > 20:
                st.info(f"📌 Menampilkan 20 data pertama. Total {len(filtered_df)} data tersedia.")
        else:
            st.info("Tidak ada data yang sesuai dengan filter.")
    else:
        st.info("📊 Belum ada data pelanggan.")

def show_update_status_tunggakan(excel):
    """Update Status Pembayaran"""
    st.subheader("Update Status Pembayaran")
    
    df = excel.read_excel('tunggakan.xlsx')
    
    if not df.empty and 'id_pelanggan' in df.columns:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            id_pelanggan = st.selectbox(
                "Pilih ID Pelanggan",
                options=df['id_pelanggan'].tolist(),
                format_func=lambda x: f"{x} - {df[df['id_pelanggan']==x]['nama_pelanggan'].iloc[0]}"
            )
        
        if id_pelanggan:
            pelanggan = df[df['id_pelanggan'] == id_pelanggan].iloc[0]
            
            st.markdown("---")
            
            # Current Info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Nama:** {pelanggan.get('nama_pelanggan', '-')}")
            with col2:
                st.info(f"**Tunggakan:** Rp {pelanggan.get('jumlah_tunggakan', 0):,.0f}")
            with col3:
                st.info(f"**Status:** {pelanggan.get('status', '-')}")
            
            st.markdown("---")
            
            # Update Form
            with st.form("update_status_form"):
                st.subheader("Update Informasi")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    new_status = st.selectbox(
                        "Status Baru",
                        ["Belum Bayar", "Sebagian", "Lunas", "Follow Up"],
                        index=["Belum Bayar", "Sebagian", "Lunas", "Follow Up"].index(pelanggan.get('status', 'Belum Bayar'))
                    )
                
                with col2:
                    max_bayar = int(pelanggan.get('jumlah_tunggakan', 0))
                    jumlah_bayar = st.number_input(
                        "Jumlah Pembayaran (Rp)",
                        min_value=0,
                        max_value=max_bayar,
                        value=0,
                        step=1000000
                    )
                
                keterangan = st.text_area("Keterangan", 
                                         value=pelanggan.get('keterangan', ''),
                                         height=100)
                
                submitted = st.form_submit_button("💾 Simpan Update", use_container_width=True)
                
                if submitted:
                    new_tunggakan = max(0, pelanggan.get('jumlah_tunggakan', 0) - jumlah_bayar)
                    
                    updates = {
                        'status': new_status,
                        'jumlah_tunggakan': new_tunggakan,
                        'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'keterangan': keterangan
                    }
                    
                    success = excel.update_row(
                        'tunggakan.xlsx',
                        {'id_pelanggan': id_pelanggan},
                        updates
                    )
                    
                    if success:
                        st.success(f"✅ Status berhasil diupdate! Tunggakan baru: Rp {new_tunggakan:,.0f}")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Gagal mengupdate status!")
    else:
        st.info("📊 Belum ada data untuk diupdate.")

def show_update_am(excel):
    """Update Account Manager"""
    st.subheader("Update Account Manager")
    
    df = excel.read_excel('tunggakan.xlsx')
    
    if not df.empty and 'id_pelanggan' in df.columns:
        # Display current AM distribution
        if 'am' in df.columns:
            am_data = df['am'].value_counts().reset_index()
            am_data.columns = ['Account Manager', 'Jumlah Pelanggan']
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(am_data, use_container_width=True, height=200)
        
        st.markdown("---")
        
        selected_ids = st.multiselect(
            "Pilih Pelanggan",
            options=df['id_pelanggan'].tolist(),
            format_func=lambda x: f"{x} - {df[df['id_pelanggan']==x]['nama_pelanggan'].iloc[0]}",
            help="Anda bisa memilih lebih dari satu pelanggan"
        )
        
        if selected_ids:
            st.write(f"**{len(selected_ids)} pelanggan dipilih**")
            
            # Show selected customers
            selected_df = df[df['id_pelanggan'].isin(selected_ids)][['id_pelanggan', 'nama_pelanggan', 'am']]
            st.dataframe(selected_df, use_container_width=True)
            
            st.markdown("---")
            
            with st.form("update_am_form"):
                new_am = st.text_input("Nama Account Manager Baru", 
                                      placeholder="Contoh: John Doe")
                
                submitted = st.form_submit_button("👤 Update AM", use_container_width=True)
                
                if submitted and new_am:
                    success_count = 0
                    
                    for id_pel in selected_ids:
                        success = excel.update_row(
                            'tunggakan.xlsx',
                            {'id_pelanggan': id_pel},
                            {
                                'am': new_am, 
                                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                        )
                        if success:
                            success_count += 1
                    
                    if success_count > 0:
                        st.success(f"✅ AM berhasil diupdate untuk {success_count} pelanggan")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Gagal mengupdate AM")
                elif submitted:
                    st.warning("⚠️ Nama Account Manager tidak boleh kosong")
    else:
        st.info("📊 Belum ada data pelanggan")

# ============================================================================
# ADMIN PAYCOL WITEL MODULE
# ============================================================================

def show_admin_paycol_witel(user_data):
    """Dashboard Admin Paycol Witel"""
    st.title("🏢 Dashboard Paycol Witel")
    st.markdown(f"### Witel: **{user_data.get('regional', '-')}**")

    excel = ExcelHandler()
    df = excel.read_excel('tunggakan.xlsx')

    if not df.empty and 'witel' in df.columns:
        df_witel = df[df['witel'] == user_data.get('regional')]
        
        if not df_witel.empty:
            # Download button
            excel_data = convert_df_to_excel(df_witel)
            st.download_button(
                label="📥 Download Data Witel",
                data=excel_data,
                file_name=f"tunggakan_witel_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.markdown("---")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tunggakan", f"Rp {df_witel['jumlah_tunggakan'].sum()/1e9:.2f}M")
            with col2:
                st.metric("Jumlah Pelanggan", len(df_witel))
            with col3:
                avg_tunggakan = df_witel['jumlah_tunggakan'].mean()
                st.metric("Rata-rata Tunggakan", f"Rp {avg_tunggakan/1e6:.2f}M")
            
            st.markdown("---")
            st.dataframe(df_witel, use_container_width=True, height=500)
        else:
            st.info(f"📊 Tidak ada data untuk witel {user_data.get('regional')}")
    else:
        st.info("📊 Data witel belum tersedia")

# ============================================================================
# MANAGEMENT MODULE
# ============================================================================

def show_management(role):
    """Dashboard Management"""
    st.title("📈 Dashboard Management")
    st.markdown(f"### Role: **{role}**")

    excel = ExcelHandler()
    df = excel.read_excel('performansi_cr.xlsx')

    if not df.empty:
        # Download button
        excel_data = convert_df_to_excel(df)
        st.download_button(
            label="📥 Download Data Performansi",
            data=excel_data,
            file_name=f"performansi_management_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.markdown("---")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        total_tagihan = df['total_tagihan'].sum() if 'total_tagihan' in df.columns else 0
        total_bayar = df['total_bayar'].sum() if 'total_bayar' in df.columns else 0
        cr_rate = (total_bayar/total_tagihan*100) if total_tagihan > 0 else 0
        tunggakan = total_tagihan - total_bayar

        with col1:
            st.metric("Total Tagihan", f"Rp {total_tagihan/1e9:.2f}M")
        with col2:
            st.metric("Total Bayar", f"Rp {total_bayar/1e9:.2f}M")
        with col3:
            st.metric("CR Nasional", f"{cr_rate:.2f}%",
                     delta=f"{cr_rate - 85:.2f}%")
        with col4:
            st.metric("Tunggakan", f"Rp {tunggakan/1e9:.2f}M")

        st.markdown("---")

        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            if 'segmen' in df.columns:
                segmen_data = df.groupby('segmen')['total_bayar'].sum().reset_index()
                fig1 = px.bar(
                    segmen_data,
                    x='segmen',
                    y='total_bayar',
                    title='Pembayaran per Segmen',
                    color='total_bayar',
                    color_continuous_scale=['#B71C1C', '#D32F2F', '#FF6659']
                )
                fig1.update_layout(
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#212121'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
                )
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            if 'regional' in df.columns:
                regional_data = df.groupby('regional').agg({
                    'total_tagihan': 'sum',
                    'total_bayar': 'sum'
                }).reset_index()
                regional_data['CR (%)'] = (regional_data['total_bayar'] / 
                                          regional_data['total_tagihan'] * 100)
                
                fig2 = px.bar(
                    regional_data,
                    x='regional',
                    y='CR (%)',
                    title='Collection Rate per Regional',
                    color='CR (%)',
                    color_continuous_scale=['#B71C1C', '#D32F2F', '#FF6659']
                )
                fig2.update_layout(
                    height=400,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#212121'),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=True, gridcolor='#E0E0E0')
                )
                st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("Data Detail")
        st.dataframe(df, use_container_width=True, height=400)
    else:
        st.info("📊 Belum ada data performansi. Generate dummy data di menu Admin Aplikasi.")

# ============================================================================
# GUEST MODULE
# ============================================================================

def show_guest():
    """Dashboard Guest - View Only"""
    st.title("👀 Guest Dashboard")
    st.markdown("### Informasi Umum Collection Rate")

    excel = ExcelHandler()
    df = excel.read_excel('performansi_cr.xlsx')

    if not df.empty:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        total_tagihan = df['total_tagihan'].sum() if 'total_tagihan' in df.columns else 0
        total_bayar = df['total_bayar'].sum() if 'total_bayar' in df.columns else 0
        cr_rate = (total_bayar/total_tagihan*100) if total_tagihan > 0 else 0
        
        with col1:
            st.metric("Total Tagihan", f"Rp {total_tagihan/1e9:.2f}M")
        with col2:
            st.metric("Total Pembayaran", f"Rp {total_bayar/1e9:.2f}M")
        with col3:
            st.metric("Collection Rate Nasional", f"{cr_rate:.2f}%")
        
        st.markdown("---")
        
        # Summary table
        if 'regional' in df.columns and 'segmen' in df.columns:
            summary_df = df.groupby(['regional', 'segmen']).agg({
                'total_tagihan': 'sum',
                'total_bayar': 'sum'
            }).reset_index()
            
            summary_df['CR (%)'] = (summary_df['total_bayar'] / 
                                   summary_df['total_tagihan'] * 100).round(2)
            
            st.dataframe(summary_df, use_container_width=True, height=400)
        else:
            st.dataframe(df[['regional', 'segmen', 'total_tagihan', 'total_bayar']] 
                        if all(col in df.columns for col in ['regional', 'segmen', 'total_tagihan', 'total_bayar'])
                        else df, 
                        use_container_width=True, height=400)
        
        st.info("ℹ️ Anda login sebagai Guest. Akses terbatas untuk melihat data saja.")
    else:
        st.info("📊 Data belum tersedia")

# ============================================================================
# LOGIN & ROUTING
# ============================================================================

def login_page():
    """Enhanced Login Page"""
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.title("🔐 Paycol Dashboard")
        st.markdown("### Sistem Manajemen Payment Collection")
        
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                login_btn = st.form_submit_button("🔓 Login", use_container_width=True)
            
            if login_btn:
                if username and password:
                    result = authenticate(username, password)
                    if result['success']:
                        st.session_state.logged_in = True
                        st.session_state.role = result['role']
                        st.session_state.user_data = result['user_data']
                        st.success("✅ Login berhasil! Mengalihkan...")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Username atau password salah")
                else:
                    st.warning("⚠️ Harap isi username dan password")
        
        st.markdown("---")
        
        # Login info
        with st.expander("ℹ️ Informasi Login Default"):
            st.markdown("""
            **Default Login Credentials:**
            
            | Role | Username | Password |
            |------|----------|----------|
            | Admin Aplikasi | admin | admin123 |
            | Admin Paycol Reg | paycol_reg | reg123 |
            | Admin Paycol Witel | paycol_witel | witel123 |
            | Management SSS | mgmt_sss | sss123 |
            | Management Non SSS | mgmt_nonsss | nonsss123 |
            | Guest | guest | guest123 |
            """)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main Application"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # Show login page if not logged in
    if not st.session_state.logged_in:
        login_page()
        return

    # Get user info
    role = st.session_state.role
    user_data = st.session_state.user_data

    # Sidebar
    with st.sidebar:
        st.title("💼 Paycol Dashboard")
        st.markdown("---")
        
        st.write("👤 **User Information**")
        st.info(f"**Username:** {user_data['username']}")
        st.info(f"**Role:** {role}")
        st.info(f"**Regional:** {user_data.get('regional', '-')}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Help section
        with st.expander("❓ Bantuan"):
            st.markdown("""
            **Fitur Dashboard:**
            - 📊 Lihat performansi CR
            - 💰 Kelola tunggakan
            - 📥 Download data Excel
            - 🎲 Generate data dummy
            - 👤 Update Account Manager
            """)
        
        st.markdown("---")
        st.caption(f"Version 2.0.0")
        st.caption(f"© 2025 Paycol Dashboard")

    # Route based on role
    if role == "Admin Aplikasi":
        show_admin_aplikasi()
    elif role == "Admin Paycol Reg":
        show_admin_paycol_reg()
    elif role == "Admin Paycol Witel":
        show_admin_paycol_witel(user_data)
    elif role in ["Management SSS", "Management Non SSS"]:
        show_management(role)
    elif role == "Guest":
        show_guest()
    else:
        st.error("❌ Role tidak dikenali")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
