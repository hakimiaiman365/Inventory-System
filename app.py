import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Selamat & Stabil
st.markdown("""
    <style>
    .hero-banner {
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%);
        border-radius: 16px;
        padding: 20px;
        color: #FFFFFF !important;
        box-shadow: 0 8px 20px rgba(255, 94, 0, 0.3);
        margin-bottom: 16px;
    }
    .hero-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.9;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    .hero-val {
        font-size: 36px;
        font-weight: 900;
        margin: 2px 0;
        color: #FFFFFF !important;
    }
    .hero-badge {
        background: rgba(0, 0, 0, 0.25);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        display: inline-block;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: #FFFFFF !important;
    }
    .badge-ok {
        background-color: #064E3B;
        color: #34D399;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-sederhana {
        background-color: #78350F;
        color: #FBBF24;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }
    .badge-rendah {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 3px 10px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: 800;
    }
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi Muat Data Pangkalan
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv("data.csv", dtype={"P/N": str})
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# Header Utama
st.title("📦 Inventori Rak")
st.caption("Sistem Stok & Lokasi Barangan")

# Carian & Penapis
search_query = st.text_input("🔍 Carian", placeholder="Taip P/N, nama barang, atau lokasi rak...")

col_chk, col_view = st.columns([1, 1])
with col_chk:
    filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

with col_view:
    view_mode = st.radio("Mod Paparan", ["📋 Jadual (Table)", "🔲 Kad (Cards)"], horizontal=True)

# Kiraan Statistik
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# Hero Banner & Metrik
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-label">JUMLAH KUANTITI STOK</div>
        <div class="hero-val">{total_qty:,} <span style="font-size: 18px; font-weight: normal;">unit</span></div>
        <div class="hero-badge">📦 {total_pn} Part Number Berdaftar</div>
    </div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m1.metric("Total P/N", total_pn)
m2.metric("Stok Rendah (≤50)", low_stock_count)
m3.metric("Lokasi Rak", total_locations)

st.divider()

# Tapis Data Mengikut Carian
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

# Paparan Data Utama
st.subheader(f"📚 Senarai Inventori ({len(filtered_df)})")

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
