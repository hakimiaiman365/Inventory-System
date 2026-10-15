import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. Konfigurasi Halaman & Layout
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Auto-refresh setiap 10 minit (600,000 milisaat) supaya aplikasi tidak tidur
components.html(
    """
    <script>
        setTimeout(function(){
            window.parent.location.reload();
        }, 600000);
    </script>
    """,
    height=0,
)

# 2. Custom CSS Dark Mode Cyberpunk (Warna Kotak Sama Dengan Warna Kad Atas)
st.markdown(
    """
<style>
/* Background & Fon Utama */
.stApp {
    background-color: #070913 !important;
    color: #E2E8F0 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 5rem !important;
    max-width: 650px !important;
}

header[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 1 !important;
}

/* Sembunyikan Radio Dot / Tick sepenuhnya */
[data-testid="stRadio"] [data-testid="stWidgetLabel"] {
    display: none !important;
}
[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    background-color: #111625 !important;
    padding: 4px !important;
    border-radius: 14px !important;
    border: 1px solid #1C253B !important;
    gap: 6px !important;
    width: 100% !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    flex: 1 !important;
    text-align: center !important;
    background-color: transparent !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin: 0 !important;
    border: none !important;
    cursor: pointer !important;
    color: #8A99AD !important;
    font-weight: 700 !important;
    justify-content: center !important;
    font-size: 13px !important;
    display: flex !important;
    align-items: center !important;
}

[data-testid="stRadio"] label div[role="radio"],
[data-testid="stRadio"] label div[data-baseweb="radio"],
[data-testid="stRadio"] label input,
[data-testid="stRadio"] label svg,
[data-testid="stRadio"] label [data-testid="stRadioButtonCustomIcon"],
[data-testid="stRadio"] label > div:first-child {
    display: none !important;
    visibility: hidden !important;
    width: 0 !important;
    height: 0 !important;
    opacity: 0 !important;
}

[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked),
[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, #FF6B00 0%, #FFA800 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.35) !important;
}

/* Hero Banner Card (Kad Atas) */
.hero-banner-card {
    background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%);
    border-radius: 20px;
    padding: 20px 22px;
    color: #FFFFFF !important;
    box-shadow: 0 10px 30px rgba(255, 94, 0, 0.35);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.hero-content-left {
    display: flex;
    align-items: center;
    gap: 14px;
}
.hero-box-icon {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
}
.hero-text-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    color: #FFFFFF !important;
}
.hero-text-qty {
    font-size: 36px;
    font-weight: 900;
    line-height: 1;
    color: #FFFFFF !important;
}
.hero-text-qty span {
    font-size: 15px;
    font-weight: 500;
}
.hero-badge-pill {
    background: rgba(0, 0, 0, 0.25);
    padding: 6px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #FFFFFF !important;
}

/* Stacked Metric Cards (Warna Sama Mengikut Kad Atas) */
.metric-item-card {
    background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%);
    border: none;
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 8px 20px rgba(255, 94, 0, 0.25);
    color: #FFFFFF !important;
}
.metric-left-box {
    display: flex;
    align-items: center;
    gap: 14px;
}
.icon-square {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    background: rgba(255, 255, 255, 0.2);
    color: #FFFFFF !important;
}

.metric-label-text { 
    font-size: 11px; 
    color: rgba(255, 255, 255, 0.9); 
    font-weight: 700; 
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.metric-value-text { 
    font-size: 26px; 
    font-weight: 900; 
    color: #FFFFFF !important; 
    line-height: 1.1; 
}

.pill-action-red {
    background: rgba(0, 0, 0, 0.25);
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}
.pill-action-purple {
    background: rgba(0, 0, 0, 0.25);
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
}

/* Badge Lencana Warna Status Stok */
.badge-status-ok {
    background-color: #059669;
    color: #FFFFFF;
    padding: 4px 14px;
    border-radius
