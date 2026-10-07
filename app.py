import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Pengurusan Inventori Rak",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🎨 Custom CSS Untuk Rekaan Sebiji Seperti UI Rujukan
st.markdown("""
    <style>
    /* Kemasan Container Utama */
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 5rem;
        max-width: 850px;
    }
    
    /* Tajuk Atas */
    .app-title {
        font-size: 26px;
        font-weight: 800;
        margin-bottom: 12px;
        color: var(--text-color, #1E2022);
    }

    /* Kad Putih / Gelap (Rounded Card UI) */
    .custom-card {
        background-color: var(--secondary-background-color, #FFFFFF);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.15);
    }
    
    .card-header-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }

    .card-title {
        font-size: 16px;
        font-weight: 700;
        color: var(--text-color, #1E2022);
    }

    /* Target / Prediction Styling */
    .target-val {
        font-size: 30px;
        font-weight: 800;
        color: var(--text-color, #1E2022);
        text-align: center;
        margin: 10px 0;
    }

    .progress-bg {
        background-color: rgba(128, 128, 128, 0.15);
        border-radius: 10px;
        height: 12px;
        width: 100%;
        overflow: hidden;
        margin-top: 8px;
    }

    .progress-fill {
        background: linear-gradient(90deg, #FF6B00 0%, #FF9E00 100%);
        height: 100%;
        border-radius: 10px;
    }

    /* Kad Tiket Carian Lokasi Rak & P/N */
    .ticket-card {
        background-color: var(--secondary-background-color, #FFFFFF);
        border-left: 6px solid #FF6B00;
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border-top: 1px solid rgba(128, 128, 128, 0.12);
        border-right: 1px solid rgba(128, 128, 128, 0.12);
        border-bottom: 1px solid rgba(128, 128, 128, 0.12);
    }
    
    .ticket-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #FF6B00;
        font-weight: 700;
    }

    .ticket-pn {
        font-size: 22px;
        font-weight: 800;
        color: var(--text-color, #0F172A);
        margin: 2px 0;
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

    /* Badges Status Stok */
    .badge-low {
        background-color: rgba(230, 0, 0, 0.15);
        color: #FF4D4D;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
    }
    .badge-ok {
        background-color: rgba(0, 168, 84, 0.15);
        color: #00A854;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
    }

    /* Styling Tab Bawah (Gaya App Navigation Bar) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        justify-content: space-around;
        background-color: var(--secondary-background-color, #F1F5F9);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid rgba(128, 128, 128, 0.15);
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 12px;
        font-weight: 700;
        color: var(--text-color, #64748B);
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6B00 0%, #FF9E00 100%) !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(255, 107, 0, 0.3);
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

# TAJUK UTAMA
st.markdown('<div class="app-title">Analysis Inventori</div>', unsafe_allow_html=True)

# 1. PILL SWITCHER UTAMA ATAS (GANTI SALE / PRODUCT)
top_mode = st.radio(
    "Top Mode",
    ["📊 Ringkasan", "📋 Senarai Item"],
    horizontal=True,
    label_visibility="collapsed"
)

st.write("")

# Kiraan Data Utama
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
stock_health_pct = min(100, int(((total_pn - low_stock_count) / total_pn * 100))) if total_pn > 0 else 0

# 2. NAVIGASI TAB BAWAH (GANTI HOME / ANALYSIS / STORE)
tab_home, tab_analysis, tab_ticket, tab_manage = st.tabs([
    "🏠 Home", 
    "📊 Analisis", 
    "🔍 Carian Tiket", 
    "⚙️ Kawalan"
])

# ==================== TAB 1: HOME ====================
with tab_home:
    if top_mode == "📊 Ringkasan":
        # KAD 1: STATISTIK STOK (GRAPH CARD INSP)
        st.markdown("""
            <div class="custom-card">
                <div class="card-header-flex">
                    <div class="card-title">Sales Statistics (Statistik Kuantiti)</div>
                    <span style="font-size: 12px; color: #8C8C8C; font-weight: 600;">📊 Mengikut P/N</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not df.empty:
            chart_data = df.set_index('P/N')[['Quantity']]
            st.area_chart(chart_data, color="#FF6B00", height=200)
        else:
            st.info("Tiada data stok untuk dipaparkan pada graf.")

        # KAD 2: TARGET PREDICTION (PROGRESS BAR INSP)
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Target Prediction (Ketersediaan Stok)</div>
                <div class="target-val">{total_qty:,} <span style="font-size:16px; font-weight:600; opacity:0.7;">unit</span></div>
                <div style="display:flex; justify-content:space-between; font-size:12px; font-weight:700; color:#8C8C8C;">
                    <span>Kesihatan Stok: {stock_health_pct}%</span>
                    <span>Stok Rendah: {low_stock_count} item</span>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {stock_health_pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    else:
        # PAPARAN SENARAI ITEM
        st.subheader(f"Senarai Semua Barang ({total_pn})")
        if not df.empty:
            display_df = df.copy()
            display_df['Status'] = display_df['Quantity'].apply(lambda x: "⚠️ Stok Rendah" if x <= 50 else "✅ Mencukupi")
            st.dataframe(
                display_df[['P/N', 'Description', 'Location', 'Quantity', 'Status']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Tiada data stok.")


# ==================== TAB 2: ANALISIS ====================
with tab_analysis:
    st.subheader("📊 Analisis Agihan Lokasi Rak")
    if not df.empty:
        loc_summary = df.groupby('Location')['Quantity'].sum().reset_index()
        st.bar_chart(loc_summary.set_index('Location'), color="#FF9E00")
        
        st.divider()
        st.markdown(f"**🔴 Senarai Stok Rendah (≤ 50 Unit): {low_stock_count} item**")
        if not low_stock_df.empty:
            st.dataframe(low_stock_df[['P/N', 'Description', 'Location', 'Quantity']], use_container_width=True, hide_index=True)
    else:
        st.info("Tiada data analisis.")


# ==================== TAB 3: CARIAN TIKET LOKASI ====================
with tab_ticket:
    st.subheader("🔍 Carian Tiket Lokasi Barang")
    search_q = st.text_input("Taip P/N, Description, atau Lokasi Rak:", placeholder="Cth: L1362279 atau RK1-C-1-1...")
    
    if search_q:
        mask = (
            df['P/N'].astype(str).str.contains(search_q, case=False, na=False) |
            df['Description'].astype(str).str.contains(search_q, case=False, na=False) |
            df['Location'].astype(str).str.contains(search_q, case=False, na=False)
        )
        filtered_df = df[mask]
    else:
        filtered_df = df

    st.caption(f"Menunjukkan {len(filtered_df)} tiket lokasi")

    if not filtered_df.empty:
        for idx, row in filtered_df.iterrows():
            badge = "<span class='badge-low'>⚠️ Stok Rendah</span>" if row['Quantity'] <= 50 else "<span class='badge-ok'>✅ Mencukupi</span>"
            
            st.markdown(f"""
                <div class="ticket-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="ticket-header">TICKET LOKASI INVENTORI</div>
                            <div class="ticket-pn">P/N: {row['P/N']}</div>
                            <div style="font-size: 14px; margin-top: 4px; opacity: 0.85;"><b>Description:</b> {row['Description']}</div>
                        </div>
                        <div style="text-align: right;">
                            <div class="ticket-location">📍 {row['Location']}</div>
                            <div style="margin-top: 8px; font-size: 13px;"><b>Qty:</b> {row['Quantity']} unit {badge}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Tiada tiket dijumpai untuk carian ini.")


# ==================== TAB 4: KAWALAN (CRUD) ====================
with tab_manage:
    st.subheader("⚙️ Pengurusan Data Stok")
    sub_tab1, sub_tab2, sub_tab3 = st.tabs(["➕ Kemaskini", "🗑️ Padam", "📥 Muat Turun"])
    
    with sub_tab1:
        pn = st.text_input("Part Number (P/N)")
        desc = st.text_input("Description")
        loc = st.text_input("Lokasi Rak (cth: R2-B-1)")
        qty = st.number_input("Kuantiti (Qty)", min_value=0, value=1)
        
        if st.button("💾 Simpan Data", use_container_width=True, type="primary"):
            if pn and loc:
                pn_clean = str(pn).strip()
                if pn_clean in df['P/N'].astype(str).values:
                    df.loc[df['P/N'].astype(str) == pn_clean, ['Description', 'Location', 'Quantity']] = [desc, loc, qty]
                    st.toast(f"P/N {pn_clean} dikemaskini!", icon="🔄")
                else:
                    new_row = pd.DataFrame([{"P/N": pn_clean, "Description": desc, "Location": loc, "Quantity": qty}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    st.toast(f"P/N {pn_clean} baru ditambah!", icon="✅")
                
                df.to_csv("data.csv", index=False)
                st.rerun()
            else:
                st.error("Sila pastikan P/N dan Lokasi diisi.")

    with sub_tab2:
        if not df.empty:
            options = df.apply(lambda r: f"{r['P/N']} - {r['Description']}", axis=1).tolist()
            selected_option = st.selectbox("Pilih item untuk dipadam:", options)
            
            if st.button("🗑️ Padam Item Ini", type="primary", use_container_width=True):
                selected_pn = selected_option.split(" - ")[0]
                df = df[df['P/N'].astype(str) != str(selected_pn)]
                df.to_csv("data.csv", index=False)
                st.toast(f"P/N {selected_pn} dipadam!", icon="🗑️")
                st.rerun()
        else:
            st.info("Tiada data stok.")

    with sub_tab3:
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun CSV Terkini",
            data=csv_data,
            file_name="inventori_rak_terkini.csv",
            mime="text/csv",
            use_container_width=True
        )
