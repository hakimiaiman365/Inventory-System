import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS UI Dark Futuristic (Neon Orange & Purple-Navy)
st.markdown("""
    <style>
    /* Latar Belakang Utama App */
    .stApp {
        background: #0B0E17 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Container Utama */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header Tajuk Utama */
    .header-box {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .header-subtitle {
        font-size: 13px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Hero Banner Gradient Oren-Pink */
    .hero-banner {
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%);
        border-radius: 20px;
        padding: 24px 28px;
        color: #FFFFFF !important;
        box-shadow: 0 10px 30px rgba(255, 94, 0, 0.3);
        margin-bottom: 16px;
        position: relative;
    }
    .hero-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        font-weight: 700;
    }
    .hero-val {
        font-size: 42px;
        font-weight: 900;
        margin: 2px 0;
    }
    .hero-badge {
        background: rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
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
        border-radius: 18px;
        padding: 18px 22px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-num {
        font-size: 28px;
        font-weight: 800;
        color: #FFFFFF;
    }

    /* Action Pill Buttons dalam Metrik */
    .btn-pill-red {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }
    .btn-pill-purple {
        background: rgba(124, 58, 237, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    /* Lencana Status Stok (Badges) */
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

    /* Sidebar / Panel Kawalan Styling */
    section[data-testid="stSidebar"] {
        background-color: #0F1422 !important;
        border-left: 1px solid #1E293B;
    }
    .sidebar-tips {
        background: #131B2E;
        border: 1px solid #1D4ED8;
        border-radius: 16px;
        padding: 16px;
        margin-top: 20px;
    }

    /* Penyesuaian Form & Buttons */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
        padding: 10px !important;
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
        # Data Default sekiranya fail belum wujud (seperti dalam contoh gambar)
        return pd.DataFrame([
            {"P/N": "P00123", "Description": "Server Board", "Location": "R2-B-1", "Quantity": 83},
            {"P/N": "P00456", "Description": "Memory DIMM", "Location": "R1-A-3", "Quantity": 12},
            {"P/N": "P00789", "Description": "PSU 1200W", "Location": "R2-C-2", "Quantity": 36},
            {"P/N": "P01011", "Description": "SSD 1.92TB", "Location": "R3-D-1", "Quantity": 5},
            {"P/N": "P01337", "Description": "Fan Module", "Location": "R1-B-4", "Quantity": 50},
            {"P/N": "P01771", "Description": "CPLD", "Location": "R2-A-2", "Quantity": 3},
            {"P/N": "P02022", "Description": "Cable Network", "Location": "R3-C-3", "Quantity": 28},
            {"P/N": "P02468", "Description": "Power Module", "Location": "R1-C-1", "Quantity": 72},
            {"P/N": "P02880", "Description": "HDD 4TB", "Location": "R2-B-3", "Quantity": 9},
            {"P/N": "P03102", "Description": "DIMM 32GB", "Location": "R3-A-1", "Quantity": 18}
        ])

df = load_data()

# 4. TAJUK UTAMA (HEADER)
st.markdown("""
    <div class="header-box">
        <span style="font-size: 36px;">📦</span>
        <div>
            <div class="header-title">Inventori Rak</div>
            <div class="header-subtitle">Sistem Stok & Lokasi</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 5. CARIAN & PENAPIS (SEARCH & FILTERS)
search_query = st.text_input("🔍 Carian", placeholder="Taip P/N, nama barang, atau lokasi rak...", label_visibility="collapsed")

col_chk, col_view = st.columns([2, 2])
with col_chk:
    filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

with col_view:
    view_mode = st.radio("Mod Paparan", ["📋 Jadual (Table)", "🔲 Kad (Cards)"], horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Kiraan Metrik Utama
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# 6. KAD DASHBOARD (HERO BANNER & METRICS)
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-label">JUMLAH KUANTITI STOK</div>
        <div class="hero-val">{total_qty:,} <span style="font-size: 20px; font-weight: normal;">unit</span></div>
        <div class="hero-badge">📦 {total_pn} Part Number Berdaftar</div>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
        <div class="metric-card-dark">
            <div>
                <div class="metric-title">Total P/N</div>
                <div class="metric-num">{total_pn}</div>
            </div>
            <span style="font-size: 24px;">📊</span>
        </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card-dark">
            <div>
                <div class="metric-title">Stok Rendah (≤50)</div>
                <div class="metric-num" style="color: #FF5E00;">{low_stock_count}</div>
            </div>
            <div class="btn-pill-red">Perlu Diperiksa</div>
        </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
        <div class="metric-card-dark">
            <div>
                <div class="metric-title">Lokasi Rak</div>
                <div class="metric-num">{total_locations}</div>
            </div>
            <div class="btn-pill-purple">Lihat Semua →</div>
        </div>
    """, unsafe_allow_html=True)

st.write("")

# Tapis Data Mengikut Input Carian
filtered_df = df.copy()

if search_query:
    mask = (
        filtered_df['P/N'].astype(str).str.contains(search_query, case=False, na=False) |
        filtered_df['Description'].astype(str).str.contains(search_query, case=False, na=False) |
        filtered_df['Location'].astype(str).str.contains(search_query, case=False, na=False)
    )
    filtered_df = filtered_df[mask]

if filter_low_stock:
    filtered_df = filtered_df[filtered_df['Quantity'] <= 50]

# 7. JADUAL SENARAI INVENTORI
st.subheader("📚 Senarai Inventori")

def get_status_badge(qty):
    if qty <= 20:
        return "<span class='badge-rendah'>Rendah</span>"
    elif qty <= 50:
        return "<span class='badge-sederhana'>Sederhana</span>"
    else:
        return "<span class='badge-ok'>OK</span>"

if not filtered_df.empty:
    if "Jadual" in view_mode:
        display_df = filtered_df.copy()
        display_df['Status'] = display_df['Quantity'].apply(get_status_badge)
        
        # Paparan Jadual Interaktif
        st.dataframe(
            display_df[['P/N', 'Description', 'Location', 'Quantity']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "P/N": st.column_config.TextColumn("P/N"),
                "Description": st.column_config.TextColumn("Nama Barang"),
                "Location": st.column_config.TextColumn("Lokasi Rak"),
                "Quantity": st.column_config.NumberColumn("Stok", format="%d")
            }
        )
    else:
        # Paparan Mod Kad
        for idx, row in filtered_df.iterrows():
            st.markdown(f"""
                <div class="metric-card-dark">
                    <div>
                        <div style="font-size: 18px; font-weight: 800; color: #FFF;">P/N: {row['P/N']}</div>
                        <div style="font-size: 14px; color: #94A3B8;"><b>Barang:</b> {row['Description']} | <b>Rak:</b> 📍 {row['Location']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 18px; font-weight: 800;">{row['Quantity']} unit</div>
                        <div style="margin-top: 4px;">{get_status_badge(row['Quantity'])}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Tiada maklumat rekod dijumpai.")


# 8. PANEL KAWALAN (SIDEBAR)
with st.sidebar:
    st.markdown("### ⚙️ Panel Kawalan")
    
    tab_add, tab_del, tab
