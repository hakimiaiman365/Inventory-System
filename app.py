import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Pengurusan Inventori Rak",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS Mengikut UI Gambar & Sokongan Dark/Light Mode
st.markdown("""
    <style>
    /* Banner Gradient Oren Utama */
    .hero-banner {
        background: linear-gradient(135deg, #FF6B00 0%, #FF9E00 100%);
        border-radius: 20px;
        padding: 20px 24px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(255, 107, 0, 0.25);
    }
    .hero-label {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #FFFFFF !important;
        opacity: 0.95;
        font-weight: 600;
    }
    .hero-val {
        font-size: 34px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 2px 0;
    }
    .hero-badge {
        background: rgba(255, 255, 255, 0.25);
        color: #FFFFFF !important;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }

    /* Kad Metrik Statistik Dinamik */
    .metric-card-modern {
        background-color: var(--secondary-background-color, #FFFFFF);
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 12px;
    }
    .metric-card-title {
        font-size: 12px;
        color: var(--text-color, #64748B);
        opacity: 0.8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-card-value {
        font-size: 24px;
        font-weight: 800;
        color: var(--text-color, #0F172A);
    }

    /* 🎟️ REKAAN KAD TIKET LOKASI RAK */
    .ticket-card {
        background-color: var(--secondary-background-color, #FFFFFF);
        border-left: 6px solid #FF6B00;
        border-radius: 16px;
        padding: 18px 22px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border-top: 1px solid rgba(128, 128, 128, 0.15);
        border-right: 1px solid rgba(128, 128, 128, 0.15);
        border-bottom: 1px solid rgba(128, 128, 128, 0.15);
    }
    .ticket-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #FF6B00;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .ticket-pn {
        font-size: 22px;
        font-weight: 800;
        color: var(--text-color, #0F172A);
    }
    .ticket-location {
        background-color: rgba(255, 107, 0, 0.15);
        color: #FF6B00;
        padding: 6px 14px;
        border-radius: 10px;
        font-size: 14px;
        font-weight: 700;
        display: inline-block;
    }

    /* Status Badges */
    .badge-ok {
        background-color: rgba(0, 168, 84, 0.15);
        color: #00A854;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
    }
    .badge-low {
        background-color: rgba(230, 0, 0, 0.15);
        color: #FF4D4D;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# Fungsi Muat Data
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv("data.csv", dtype={"P/N": str})
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# 🔀 SWITCHER PANDANGAN ATAS (Ganti Sale / Product)
col_title, col_toggle = st.columns([2, 1])
with col_title:
    st.title("📦 Inventori Rak")

with col_toggle:
    view_mode = st.radio(
        "Mod Paparan:",
        ["📋 Jadual", "🎴 Kad"],
        horizontal=True,
        label_visibility="collapsed"
    )

# 📱 TABS NAVIGASI UTAMA (Ganti Home / Analysis / Store)
tab_home, tab_search = st.tabs(["🏠 Home", "🔍 Carian Tiket"])

# kiraan statistik
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# ==================== TAB 1: HOME ====================
with tab_home:
    st.write("")
    # Dashboard Banner & Metrics
    col_banner, col_metrics = st.columns([1.2, 2])

    with col_banner:
        st.markdown(f"""
            <div class="hero-banner">
                <div class="hero-label">Jumlah Kuantiti Stok</div>
                <div class="hero-val">{total_qty:,} <span style="font-size: 16px; font-weight: normal;">unit</span></div>
                <div class="hero-badge">📦 {total_pn} P/N Berdaftar</div>
            </div>
        """, unsafe_allow_html=True)

    with col_metrics:
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
                <div class="metric-card-modern">
                    <div class="metric-card-title">Total P/N</div>
                    <div class="metric-card-value">{total_pn}</div>
                </div>
            """, unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
                <div class="metric-card-modern">
                    <div class="metric-card-title">Stok Rendah (≤50)</div>
                    <div class="metric-card-value" style="color: #FF4D4D;">{low_stock_count}</div>
                </div>
            """, unsafe_allow_html=True)
        with m3:
            st.markdown(f"""
                <div class="metric-card-modern">
                    <div class="metric-card-title">Lokasi Rak</div>
                    <div class="metric-card-value" style="color: #FF6B00;">{total_locations}</div>
                </div>
            """, unsafe_allow_html=True)

    # Senarai Stok Rendah
    with st.expander(f"🔴 Lihat Senarai Stok Rendah ≤ 50 Unit ({low_stock_count} item)", expanded=False):
        if not low_stock_df.empty:
            st.dataframe(
                low_stock_df[['P/N', 'Description', 'Location', 'Quantity']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.success("✅ Semua stok mencukupi.")

    st.divider()

    # Paparan Senarai Barang Mengikut Mod (Jadual / Kad)
    st.subheader(f"Senarai Semua Barang ({total_pn})")
    
    if not df.empty:
        if view_mode == "📋 Jadual":
            display_df = df.copy()
            display_df['Status'] = display_df['Quantity'].apply(lambda x: "⚠️ Stok Rendah" if x <= 50 else "✅ Mencukupi")
            st.dataframe(
                display_df[['P/N', 'Description', 'Location', 'Quantity', 'Status']],
                use_container_width=True,
                hide_index=True
            )
        else:
            for idx, row in df.iterrows():
                with st.container():
                    c1, c2, c3, c4 = st.columns([2, 4, 2, 2])
                    c1.markdown(f"**P/N:** `{row['P/N']}`")
                    c2.write(f"**Description:** {row['Description']}")
                    c3.markdown(f"**Rak:** `<span style='color:#FF6B00; font-weight:bold;'>📍 {row['Location']}</span>`", unsafe_allow_html=True)
                    status_badge = "<span class='badge-low'>⚠️ Stok Rendah</span>" if row['Quantity'] <= 50 else "<span class='badge-ok'>✅ Mencukupi</span>"
                    c4.markdown(f"**Qty:** `{row['Quantity']} unit` {status_badge}", unsafe_allow_html=True)
                    st.divider()
    else:
        st.info("Tiada data barangan.")


# =================
