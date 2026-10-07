import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Tema Dark
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Dark Cyberpunk dengan Segmented Box Button (Tiada Bulatan Radio)
st.markdown("""
    <style>
    /* Latar Belakang & Fon Utama */
    .stApp {
        background-color: #0B0E17 !important;
        color: #E2E8F0 !important;
    }
    
    /* Header Box */
    .header-box {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }
    .header-title {
        font-size: 26px;
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
        padding: 22px 24px;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(255, 94, 0, 0.3);
        margin-bottom: 16px;
    }
    .hero-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.95;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    .hero-val {
        font-size: 38px;
        font-weight: 900;
        margin: 2px 0;
        color: #FFFFFF !important;
    }
    .hero-badge {
        background: rgba(0, 0, 0, 0.3);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #FFFFFF !important;
    }

    /* Kad Metrik Dark Neon */
    .metric-card-dark {
        background: #121726;
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-num {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
    }

    /* Action Badges */
    .btn-pill-red {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    .btn-pill-purple {
        background: rgba(124, 58, 237, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }

    /* Badges Status Stok */
    .badge-ok {
        background: #064E3B;
        color: #34D399;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-sederhana {
        background: #78350F;
        color: #FBBF24;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-rendah {
        background: #7F1D1D;
        color: #FCA5A5;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
    }

    /* 🔲 KOTAK MOD PAPARAN PROFESIONAL (MENUKAR BULATAN RADIO JADI KOTAK BUTTON) */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    div[role="radiogroup"] {
        display: flex !important;
        background-color: #121726 !important;
        padding: 5px !important;
        border-radius: 14px !important;
        border: 1px solid #1E293B !important;
        gap: 6px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] > label {
        flex: 1 !important;
        text-align: center !important;
        background-color: transparent !important;
        border-radius: 10px !important;
        padding: 10px 14px !important;
        margin: 0 !important;
        border: none !important;
        cursor: pointer !important;
        color: #94A3B8 !important;
        font-weight: 600 !important;
        transition: all 0.2s ease-in-out !important;
        justify-content: center !important;
    }
    /* Sembunyikan bulatan radio */
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    /* Kotak aktif bila dipilih */
    div[role="radiogroup"] > label:has(input:checked),
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(255, 94, 0, 0.4) !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F1422 !important;
        border-right: 1px solid #1E293B;
    }
    .sidebar-tips {
        background: #131B2E;
        border: 1px solid #1D4ED8;
        border-radius: 14px;
        padding: 14px;
        margin-top: 20px;
    }

    /* Styling Butang Simpan/Update */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(
