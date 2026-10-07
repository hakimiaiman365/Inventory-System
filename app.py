import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Tema Dark
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Dark Cyberpunk / Neon Theme (Selamat & Mesra Paparan)
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

    /* Pill Badges */
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

    /* Status Badges untuk Jadual/Kad */
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

    /* Styling Butang */
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Fungsi Muat Data Pangkalan Asal (data.csv)
@st.cache_data(ttl=2)
def load_data():
    try:
        df = pd.read_csv("data.csv", dtype={"P/N": str})
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').fillna(0).astype(int)
        return df
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# 2. Header Utama
st.markdown("""
    <div class="header-box">
        <span style="font-size: 34px;">📦</span>
        <div>
            <div class="header-title">Inventori Rak</div>
            <div class="header-subtitle">Sistem Stok & Lokasi</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. Ruang Carian & Penapis
search_query = st.text_input("🔍 Carian", placeholder="Taip P/N, nama barang, atau lokasi rak...", label_visibility="collapsed")

col_chk, col_view = st.columns([1, 1])
with col_chk:
    filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

with col_view:
    view_mode = st.radio("Mod Paparan", ["📋 Jadual (Table)", "🔲 Kad (Cards)"], horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Kiraan Statistik Data Asal
total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

# 4. Hero Banner Utama
st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-label">JUMLAH KUANTITI STOK</div>
        <div class="hero-val">{total_qty:,} <span style="font-size: 18px; font-weight: normal;">unit</span></div>
        <div class="hero-badge">📦 {total_pn} Part Number Berdaftar</div>
    </div>
""", unsafe_allow_html=True)

# 5. Kad Metrik Ringkasan
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
        <div class="metric-card-dark">
            <div>
                <div class="metric-title">Total P/N</div>
                <div class="metric-num">{total_pn}</div>
            </div>
            <span style="font-size: 22px;">📊</span>
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

# 6. Tapis Data Mengikut Carian
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

# 7. Paparan Senarai Inventori
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
        display_df['Status'] = display_df['Quantity'].apply(lambda x: "Rendah" if x <= 20 else ("Sederhana" if x <= 50 else "OK"))
        
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
                <div class="metric-card-dark">
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #FFF;">P/N: {row['P/N']}</div>
                        <div style="font-size: 13px; color: #94A3B8;"><b>Barang:</b> {row['Description']} | <b>Rak:</b> 📍 {row['Location']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 16px; font-weight: 800;">{row['Quantity']} unit</div>
                        <div style="margin-top: 4px;">{get_status_badge(row['Quantity'])}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("⚠️ Tiada maklumat rekod dijumpai.")

# 8. Sidebar Panel Kawalan (Tambah, Edit, Padam, Export)
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

    st.markdown("""
        <div class="sidebar-tips">
            <div style="font-weight: 700; color: #60A5FA; font-size: 13px;">💡 Tips</div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                Pastikan format P/N, lokasi rak dan kuantiti adalah betul sebelum menyimpan data.
            </div>
        </div>
    """, unsafe_allow_html=True)
