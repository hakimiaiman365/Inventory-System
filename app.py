import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Layout
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS Cyberpunk Dark Mode (Sama 100% & Kalis Ralat)
st.markdown("""
<style>
/* Global App Container */
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

/* Header Bar */
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
}
.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.main-title {
    font-size: 24px;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.1;
}
.main-title span {
    color: #FF7A00;
}
.sub-title {
    font-size: 11px;
    color: #8A99AD;
    font-weight: 500;
}

/* Hero Banner Card */
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

/* Stacked Metric Cards */
.metric-item-card {
    background-color: #111625;
    border: 1px solid #1C253B;
    border-radius: 18px;
    padding: 14px 18px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.metric-left-box {
    display: flex;
    align-items: center;
    gap: 14px;
}
.icon-square {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}
.icon-purple { background: rgba(124, 58, 237, 0.15); color: #A78BFA; }
.icon-red { background: rgba(239, 68, 68, 0.15); color: #EF4444; }
.icon-blue { background: rgba(59, 130, 246, 0.15); color: #60A5FA; }

.metric-label-text { font-size: 11px; color: #8A99AD; font-weight: 600; }
.metric-value-text { font-size: 24px; font-weight: 800; color: #FFFFFF; line-height: 1; }

.pill-action-red {
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
}
.pill-action-purple {
    background: rgba(124, 58, 237, 0.15);
    color: #C084FC;
    border: 1px solid rgba(124, 58, 237, 0.3);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
}

/* BUANG SEPENUHNYA BULATAN RADIO TICK2 DI FON & DESKTOP */
[data-testid="stRadio"] [data-testid="stWidgetLabel"] { display: none !important; }
[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    background-color: #111625 !important;
    padding: 4px !important;
    border-radius: 16px !important;
    border: 1px solid #1C253B !important;
    gap: 6px !important;
    width: 100% !important;
}
[data-testid="stRadio"] div[role="radiogroup"] label {
    flex: 1 !important;
    text-align: center !important;
    background-color: transparent !important;
    border-radius: 12px !important;
    padding: 10px 12px !important;
    margin: 0 !important;
    border: none !important;
    cursor: pointer !important;
    color: #8A99AD !important;
    font-weight: 700 !important;
    justify-content: center !important;
    font-size: 13px !important;
}
/* Sembunyi semua elemen radio icon/dot */
[data-testid="stRadio"] div[role="radiogroup"] label > div:first-child,
[data-testid="stRadio"] div[role="radiogroup"] label input,
[data-testid="stRadio"] div[role="radiogroup"] label svg {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}
/* Style bila butang dipilih */
[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked),
[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, #FF6B00 0%, #FFA800 100%) !important;
    color: #FFFFFF !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 0, 0.35) !important;
}

/* Status Badges */
.badge-ok { background-color: #064E3B; color: #34D399; padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 800; display: inline-block; }
.badge-sederhana { background-color: #78350F; color: #FBBF24; padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 800; display: inline-block; }
.badge-rendah { background-color: #7F1D1D; color: #FCA5A5; padding: 4px 10px; border-radius: 10px; font-size: 11px; font-weight: 800; display: inline-block; }

/* Item Card dalam Senarai */
.inventory-item-card {
    background-color: #111625;
    border: 1px solid #1C253B;
    border-radius: 14px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: #0B0E1B !important;
    border-right: 1px solid #1C253B;
}

.stTextInput input {
    background-color: #111625 !important;
    color: #FFFFFF !important;
    border: 1px solid #1C253B !important;
    border-radius: 14px !important;
}
.stButton>button {
    border-radius: 12px !important;
    background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%) !important;
    color: white !important;
    border: none !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# 3. Fungsi Muat Data Pangkalan Asal (data.csv)
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv("data.csv", dtype={"P/N": str})
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# 4. Header Bar
st.markdown("""
<div class="header-container">
    <div class="header-left">
        <span style="font-size: 30px;">📦</span>
        <div>
            <div class="main-title">Inventori <span>Rak</span></div>
            <div class="sub-title">Sistem Stok & Lokasi</div>
        </div>
    </div>
    <div style="font-size: 22px; color: #60A5FA;">👤</div>
</div>
""", unsafe_allow_html=True)

# 5. Carian Pantas (Paling Atas)
search_query = st.text_input(
    "🔍 Carian Pantas", 
    placeholder="Taip P/N, nama barang, atau lokasi rak...", 
    label_visibility="collapsed"
)

filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

# Segmented Control (Jadual vs Kad)
view_mode = st.radio(
    "Mod Paparan", 
    ["📋 Jadual (Table)", "🔲 Kad (Cards)"], 
    horizontal=True, 
    label_visibility="collapsed"
)

st.write("")

# Kiraan Statistik Data
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# 6. Hero Banner Card
st.markdown(f"""
<div class="hero-banner-card">
    <div class="hero-content-left">
        <div class="hero-box-icon">📦</div>
        <div>
            <div class="hero-text-label">JUMLAH KUANTITI STOK</div>
            <div class="hero-text-qty">{total_qty:,} <span>unit</span></div>
        </div>
    </div>
    <div class="hero-badge-pill">📦 {total_pn} Part Number Berdaftar</div>
</div>
""", unsafe_allow_html=True)

# 7. Stacked KPI Metric Cards
st.markdown(f"""
<div class="metric-item-card">
    <div class="metric-left-box">
        <div class="icon-square icon-purple">📊</div>
        <div>
            <div class="metric-label-text">Total P/N</div>
            <div class="metric-value-text">{total_pn}</div>
        </div>
    </div>
</div>

<div class="metric-item-card">
    <div class="metric-left-box">
        <div class="icon-square icon-red">⚠️</div>
        <div>
            <div class="metric-label-text">Stok Rendah (≤50)</div>
            <div class="metric-value-text" style="color: #FF5E00;">{low_stock_count}</div>
        </div>
    </div>
    <div class="pill-action-red">Perlu Diperiksa</div>
</div>

<div class="metric-item-card">
    <div class="metric-left-box">
        <div class="icon-square icon-blue">📍</div>
        <div>
            <div class="metric-label-text">Lokasi Rak</div>
            <div class="metric-value-text">{total_locations}</div>
        </div>
    </div>
    <div class="pill-action-purple">Lihat Semua →</div>
</div>
""", unsafe_allow_html=True)

st.write("")

# 8. Filter Data
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

# 9. Header Section Inventori
st.markdown("""
<div style="display:flex; align-items:center; gap:8px; margin-top:8px; margin-bottom:12px;">
    <span style="font-size:20px;">🥞</span>
    <span style="font-size:18px; font-weight:800; color:#FFFFFF;">Senarai Inventori</span>
</div>
""", unsafe_allow_html=True)

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
        display_df['Status'] = display_df['Quantity'].apply(lambda x: "Rendah" if x <= 20 else ("Sederhana" if x <= 50 else "OK"))
        
        # Paparan Jadual Native Streamlit yang Responsif
        st.dataframe(
            display_df[['P/N', 'Description', 'Location', 'Quantity', 'Status']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "P/N": st.column_config.TextColumn("P/N"),
                "Description": st.column_config.TextColumn("Nama Barang"),
                "Location": st.column_config.TextColumn("Lokasi Rak"),
                "Quantity": st.column_config.NumberColumn("Stok", format="%d"),
                "Status": st.column_config.TextColumn("Status")
            }
        )
    else:
        for idx, row in filtered_df.iterrows():
            st.markdown(f"""
            <div class="inventory-item-card">
                <div>
                    <div style="font-size: 15px; font-weight: 800; color: #FFF;">P/N: {row['P/N']}</div>
                    <div style="font-size: 12px; color: #8A99AD; margin-top:2px;"><b>Barang:</b> {row['Description']} | <b>Rak:</b> 📍 {row['Location']}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 15px; font-weight: 800; color: #FFF;">{row['Quantity']} unit</div>
                    <div style="margin-top: 4px;">{get_status_badge(row['Quantity'])}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Tiada maklumat rekod dijumpai.")

# 10. Sidebar Panel Kawalan
with st.sidebar:
    st.header("⚙️ Panel Kawalan")
    
    tab1, tab2, tab3 = st.tabs(["➕ Kemaskini", "🗑️ Padam", "📥 Muat Turun"])
    
    with tab1:
        st.caption("Masukkan P/N sedia ada untuk kemaskini, atau P/N baru untuk tambah.")
        pn_in = st.text_input("Part Number (P/N) *", placeholder="Contoh: P01234")
        desc_in = st.text_input("Description *", placeholder="Contoh: Server Board / Memory DIMM")
        loc_in = st.text_input("Lokasi Rak (cth: R2-B-1) *", placeholder="Contoh: R2-B-1")
        qty_in = st.number_input("Kuantiti (Qty) *", min_value=0, value=1)
        
        if st.button("💾 Simpan / Update Data", use_container_width=True, type="primary"):
            if pn_in and loc_in:
                pn_clean = str(pn_in).strip()
                if pn_clean in df['P/N'].astype(str).values:
                    df.loc[df['P/N'].astype(str) == pn_clean, ['Description', 'Location', 'Quantity']] = [desc_in, loc_in, qty_in]
                    st.toast(f"P/N {pn_clean} dikemaskini!", icon="🔄")
                else:
                    new_row = pd.DataFrame([{"P/N": pn_clean, "Description": desc_in, "Location": loc_in, "Quantity": qty_in}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    st.toast(f"P/N {pn_clean} ditambah!", icon="✅")
                
                df.to_csv("data.csv", index=False)
                st.rerun()
            else:
                st.error("Sila isi P/N dan Lokasi Rak.")

    with tab2:
        if not df.empty:
            options = df.apply(lambda r: f"{r['P/N']} - {r['Description']}", axis=1).tolist()
            selected = st.selectbox("Pilih item untuk dipadam:", options)
            if st.button("🗑️ Padam Item Ini", use_container_width=True, type="primary"):
                target_pn = selected.split(" - ")[0]
                df = df[df['P/N'].astype(str) != str(target_pn)]
                df.to_csv("data.csv", index=False)
                st.toast(f"P/N {target_pn} dipadam!", icon="🗑️")
                st.rerun()
        else:
            st.info("Tiada data stok.")

    with tab3:
        csv_bytes = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun CSV",
            data=csv_bytes,
            file_name="inventori_rak_terkini.csv",
            mime="text/csv",
            use_container_width=True
        )
