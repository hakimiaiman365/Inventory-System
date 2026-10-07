import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(
    page_title="Sistem Pengurusan Inventori Rak",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom CSS yang Menyokong DUA-DUA (Light Mode & Dark Mode)
st.markdown("""
    <style>
    /* Banner Gradient Oren Utama (Kekal Terang & Jelas dalam Semua Mod) */
    .hero-banner {
        background: linear-gradient(135deg, #FF6B00 0%, #FF9E00 100%);
        border-radius: 20px;
        padding: 22px 28px;
        color: #FFFFFF !important;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(255, 107, 0, 0.3);
    }
    .hero-label {
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #FFFFFF !important;
        opacity: 0.95;
        font-weight: 600;
    }
    .hero-val {
        font-size: 38px;
        font-weight: 800;
        color: #FFFFFF !important;
        margin: 4px 0;
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

    /* Kad Metrik Dinamik (Mengikut Tema Light / Dark Automatik) */
    .metric-card-modern {
        background-color: var(--secondary-background-color, #FFFFFF);
        border-radius: 16px;
        padding: 18px 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 15px;
    }
    .metric-card-title {
        font-size: 13px;
        color: var(--text-color, #64748B);
        opacity: 0.8;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-card-value {
        font-size: 26px;
        font-weight: 800;
        color: var(--text-color, #0F172A);
    }
    
    /* Badges Status Stok (Transparent Overlay) */
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
    .location-tag {
        background-color: rgba(255, 107, 0, 0.15);
        color: #FF6B00;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
    }

    /* Penyesuaian Butang */
    .stButton>button {
        border-radius: 12px !important;
        font-weight: 600 !important;
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

# 🔍 1. RUANG CARIAN UTAMA (PALING ATAS)
st.title("📦 Inventori Rak")

col_search, col_filter, col_view = st.columns([3, 2, 2])

with col_search:
    search = st.text_input("🔍 Carian Pantas", placeholder="Taip P/N, nama barang, atau lokasi rak...", label_visibility="collapsed")

with col_filter:
    filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

with col_view:
    view_type = st.radio("Mod Paparan:", ["Jadual (Table)", "Kad (Cards)"], horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Kiraan Statistik
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# 📊 2. DASHBOARD BANNER & KAD METRIK (GAYA UI GAMBAR)
col_banner, col_metrics = st.columns([1.2, 2])

with col_banner:
    # Banner Gradient Oren
    st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-label">Jumlah Kuantiti Stok</div>
            <div class="hero-val">{total_qty:,} <span style="font-size: 18px; font-weight: normal;">unit</span></div>
            <div class="hero-badge">📦 {total_pn} Part Number Berdaftar</div>
        </div>
    """, unsafe_allow_html=True)

with col_metrics:
    # Kad-kad Metrik Dinamik
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

# 🔴 3. SENARAI PANTAS ITEM STOK RENDAH
with st.expander(f"🔴 Tekan Sini Untuk Senarai P/N Stok Rendah ≤ 50 Unit ({low_stock_count} item)", expanded=False):
    if not low_stock_df.empty:
        st.dataframe(
            low_stock_df[['P/N', 'Description', 'Location', 'Quantity']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "P/N": "Part Number (P/N)",
                "Description": "Nama Item",
                "Location": "Lokasi Rak",
                "Quantity": st.column_config.NumberColumn("Kuantiti (Unit)", format="%d")
            }
        )
    else:
        st.success("✅ Semua stok mencukupi (Tiada item bawah 50 unit).")

st.divider()

# Tapis Data Mengikut Carian dan Checkbox
filtered_df = df.copy()

if search:
    mask = (
        filtered_df['P/N'].astype(str).str.contains(search, case=False, na=False) |
        filtered_df['Description'].astype(str).str.contains(search, case=False, na=False) |
        filtered_df['Location'].astype(str).str.contains(search, case=False, na=False)
    )
    filtered_df = filtered_df[mask]

if filter_low_stock:
    filtered_df = filtered_df[filtered_df['Quantity'] <= 50]

# 📋 4. PAPARAN DATA UTAMA
st.subheader(f"Senarai Barang ({len(filtered_df)} dijumpai)")

if not filtered_df.empty:
    if view_type == "Jadual (Table)":
        display_df = filtered_df.copy()
        display_df['Status'] = display_df['Quantity'].apply(lambda x: "⚠️ Stok Rendah" if x <= 50 else "✅ Mencukupi")
        
        st.dataframe(
            display_df[['P/N', 'Description', 'Location', 'Quantity', 'Status']],
            use_container_width=True,
            hide_index=True,
            column_config={
                "P/N": st.column_config.TextColumn("Part Number (P/N)"),
                "Description": st.column_config.TextColumn("Nama / Perincian Item"),
                "Location": st.column_config.TextColumn("Lokasi Rak"),
                "Quantity": st.column_config.NumberColumn("Kuantiti (Unit)", format="%d"),
                "Status": st.column_config.TextColumn("Status Stok")
            }
        )
    else:
        for idx, row in filtered_df.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 4, 2, 2])
                c1.markdown(f"**P/N:** `{row['P/N']}`")
                c2.write(f"**Description:** {row['Description']}")
                c3.markdown(f"**Rak:** <span class='location-tag'>📍 {row['Location']}</span>", unsafe_allow_html=True)
                
                status_badge = "<span class='badge-low'>⚠️ Stok Rendah</span>" if row['Quantity'] <= 50 else "<span class='badge-ok'>✅ Mencukupi</span>"
                c4.markdown(f"**Qty:** `{row['Quantity']} unit` &nbsp; {status_badge}", unsafe_allow_html=True)
                st.divider()
else:
    st.warning("⚠️ Tiada maklumat rekod dijumpai.")

# ⚙️ SIDEBAR (Pengurusan & Kawalan)
with st.sidebar:
    st.header("⚙️ Panel Kawalan")
    tab1, tab2, tab3 = st.tabs(["➕ Kemaskini", "🗑️ Padam", "📥 Muat Turun"])
    
    # TAB 1: Tambah / Edit
    with tab1:
        st.caption("Masukkan P/N sedia ada untuk kemaskini, atau P/N baru untuk tambah.")
        pn = st.text_input("Part Number (P/N)")
        desc = st.text_input("Description")
        loc = st.text_input("Lokasi Rak (cth: R2-B-1)")
        qty = st.number_input("Kuantiti (Qty)", min_value=0, value=1)
        
        if st.button("💾 Simpan / Update Data", use_container_width=True, type="primary"):
            if pn and loc:
                pn_clean = str(pn).strip()
                if pn_clean in df['P/N'].astype(str).values:
                    df.loc[df['P/N'].astype(str) == pn_clean, ['Description', 'Location', 'Quantity']] = [desc, loc, qty]
                    st.toast(f"P/N {pn_clean} berjaya dikemaskini!", icon="🔄")
                else:
                    new_row = pd.DataFrame([{"P/N": pn_clean, "Description": desc, "Location": loc, "Quantity": qty}])
                    df = pd.concat([df, new_row], ignore_index=True)
                    st.toast(f"P/N {pn_clean} baru ditambah!", icon="✅")
                
                df.to_csv("data.csv", index=False)
                st.rerun()
            else:
                st.error("Sila pastikan P/N dan Lokasi diisi.")

    # TAB 2: Padam Item
    with tab2:
        st.caption("Pilih item untuk dipadam secara kekal.")
        if not df.empty:
            options = df.apply(lambda r: f"{r['P/N']} - {r['Description']}", axis=1).tolist()
            selected_option = st.selectbox("Pilih item:", options)
            
            if st.button("🗑️ Padam Item Ini", type="primary", use_container_width=True):
                selected_pn = selected_option.split(" - ")[0]
                df = df[df['P/N'].astype(str) != str(selected_pn)]
                df.to_csv("data.csv", index=False)
                st.toast(f"P/N {selected_pn} dipadam!", icon="🗑️")
                st.rerun()
        else:
            st.info("Tiada data stok.")

    # TAB 3: Eksport Data
    with tab3:
        st.caption("Muat turun pangkalan data inventori terkini dalam format CSV.")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun CSV",
            data=csv_data,
            file_name="inventori_rak_terkini.csv",
            mime="text/csv",
            use_container_width=True
        )
