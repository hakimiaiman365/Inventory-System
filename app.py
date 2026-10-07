import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS UI Dark Futuristic (Mesra Mobile & Boleh Scroll)
st.markdown("""
    <style>
    /* Paksa pergerakan scroll aktif secara lancar di telefon */
    html, body, [data-testid="stAppViewContainer"], .main {
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        background: #0B0E17 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Container Utama Mod Fon */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        max-width: 100% !important;
    }

    /* Header Tajuk Utama */
    .header-box {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
    }
    .header-title {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .header-subtitle {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Hero Banner Gradient Oren-Pink */
    .hero-banner {
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%);
        border-radius: 18px;
        padding: 20px 22px;
        color: #FFFFFF !important;
        box-shadow: 0 8px 25px rgba(255, 94, 0, 0.3);
        margin-bottom: 14px;
    }
    .hero-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.95;
        font-weight: 700;
    }
    .hero-val {
        font-size: 36px;
        font-weight: 900;
        margin: 2px 0;
    }
    .hero-badge {
        background: rgba(0, 0, 0, 0.25);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Kad Metrik Dark Neon */
    .metric-card-dark {
        background: #121726;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .metric-title {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 2px;
    }
    .metric-num {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
    }

    /* Action Pill Buttons */
    .btn-pill-red {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    .btn-pill-purple {
        background: rgba(124, 58, 237, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }

    /* Badges Status Stok */
    .badge-ok {
        background: #064E3B;
        color: #34D399;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-sederhana {
        background: #78350F;
        color: #FBBF24;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-rendah {
        background: #7F1D1D;
        color: #FCA5A5;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }

    /* Sidebar / Panel Kawalan */
    section[data-testid="stSidebar"] {
        background-color: #0F1422 !important;
        border-left: 1px solid #1E293B;
    }
    .sidebar-tips {
        background: #131B2E;
        border: 1px solid #1D4ED8;
        border-radius: 14px;
        padding: 14px;
        margin-top: 16px;
    }

    /* Penyesuaian Butang */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 8px 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Fungsi Muat Data Pangkalan
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv("data.csv", dtype={"P/N": str})
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# 4. TAJUK UTAMA (HEADER)
st.markdown("""
    <div class="header-box">
        <span style="font-size: 32px;">📦</span>
        <div>
            <div class="header-title">Inventori Rak</div>
            <div class="header-subtitle">Sistem Stok & Lokasi</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. CARIAN & PENAPIS (SEARCH & FILTERS)
