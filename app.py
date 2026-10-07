import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Inventori Rak - Sistem Stok & Lokasi",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS UI Dark Neon Cyberpunk
st.markdown('''
    <style>
    /* Body & Background */
    .stApp {
        background-color: #0A0D16 !important;
        color: #E2E8F0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Container Padding */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 4rem !important;
        max-width: 800px !important;
    }

    /* Top Header Bar */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
    }
    .header-left {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-title-text {
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }
    .header-sub-text {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Hero Card (Jumlah Kuantiti Stok) */
    .hero-card {
        background: linear-gradient(135deg, #FF5E00 0%, #D9006C 100%);
        border-radius: 20px;
        padding: 22px 24px;
        color: #FFFFFF !important;
        box-shadow: 0 10px 25px rgba(255, 94, 0, 0.35);
        margin-bottom: 16px;
        position: relative;
    }
    .hero-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        opacity: 0.95;
        font-weight: 700;
        color: #FFFFFF !important;
    }
    .hero-qty {
        font-size: 40px;
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

    /* Metric Cards (Stacked Dark Cards) */
    .dark-metric-card {
        background-color: #121726;
        border: 1px solid #1E293B;
        border-radius: 18px;
        padding: 16px 20px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.25);
    }
    .metric-info-title {
        font-size: 12px;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .metric-info-val {
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
    }

    /* Pill Badges inside Metrics */
    .pill-red {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }
    .pill-purple {
        background: rgba(124, 58, 237, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(124, 58, 237, 0.4);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
    }

    /* Custom Radio Box Buttons (Menukar Radio Jadi Butang Kotak) */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    div[role="radiogroup"] {
        display: flex !important;
        background-color: #121726 !important;
        padding: 5px !important;
        border-radius: 16px !important;
        border: 1px solid #1E293B !important;
        gap: 6px !important;
        width: 100% !important;
    }
    div[role="radiogroup"] > label {
        flex: 1 !important;
        text-align: center !important;
        background-color: transparent !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        margin: 0 !important;
        border: none !important;
        cursor: pointer !important;
        color: #94A3B8 !important;
        font-weight: 700 !important;
        justify-content: center !important;
    }
    div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    div[role="radiogroup"] > label:has(input:checked),
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(135deg, #FF5E00 0%, #FF9E00 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        box-shadow: 0 4px 15px rgba(255, 94, 0, 0.4) !important;
    }

    /* Badges Status Stok */
    .status-ok {
        background-color: #064E3B;
        color: #34D399;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
        display: inline-block;
    }
    .status-sederhana {
        background-color: #78350F;
        color: #FBBF24;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
        display: inline-block;
    }
    .status-rendah {
        background-color: #7F1D1D;
        color: #FCA5A5;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 800;
        display: inline-block;
    }

    /* Custom Table Styling */
    .custom-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0 6px;
    }
    .custom-table th {
        color: #94A3B8;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #1E293B;
    }
    .custom-table td {
        background-color: #121726;
        padding: 12px;
        font-size: 13px;
        color: #E2E8F0;
    }
    .custom-table tr td:first-child {
        border-top-left-radius: 12px;
        border-bottom-left-radius: 12px;
        color: #94A3B8;
    }
    .custom-table tr td:last-child {
        border-top-right-radius: 12px;
        border-bottom-right-radius: 12px;
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

    /* Styling Input & Buttons */
    .stTextInput input {
        background-color: #121726 !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        border-radius: 14px !important;
    }
    .stButton>button {
        border-radius: 12px !important;
        background: linear-gradient(135deg, #FF5E00 0%, #D9006C 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 700 !important;
    }
    </style>
''', unsafe_allow_html=True)

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

# 4. Header Utama App
st.markdown('''
    <div class="app-header">
        <div class="header-left">
            <span style="font-size: 32px;">📦</span>
            <div>
                <div class="header-title-text">Inventori Rak</div>
                <div class="header-sub-text">Sistem Stok & Lokasi</div>
            </div>
        </div>
        <div style="font-size: 20px;">👤</div>
    </div>
''', unsafe_allow_html=True)

# 5. Carian Utama (Paling Atas)
search_query = st.text_input(
    "🔍 Carian Utama", 
    placeholder="Taip P/N, nama barang, atau lokasi rak...", 
    label_visibility="collapsed"
)

filter_low_stock = st.checkbox("⚠️ Stok Rendah Sahaja (≤ 50)")

# Mod Paparan Switcher (Jadual vs Kad)
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

# 6. Hero Card (Jumlah Kuantiti Stok)
st.markdown(f'''
    <div class="hero-card">
        <div class="hero-label">JUMLAH KUANTITI STOK</div>
        <div class="hero-qty">{total_qty:,} <span style="font-size: 18px; font-weight: normal;">unit</span></div>
        <div class="hero-badge">📦 {total_pn} Part Number Berdaftar</div>
    </div>
''', unsafe_allow_html=True)

# 7. Stacked Metric Cards
st.markdown(f'''
    <div class="dark-metric-card">
        <div>
            <div class="metric-info-title">Total P/N</div>
            <div class="metric-info-val">{total_pn}</div>
        </div>
        <span style="font-size: 24px;">📊</span>
    </div>
    
    <div class="dark-metric-card">
        <div>
            <div class="metric-info-title">Stok Rendah (≤50)</div>
            <div class="metric-info-val" style="color: #FF5E00;">{low_stock_count}</div>
        </div>
        <div class="pill-red">Perlu Diperiksa</div>
    </div>
    
    <div class="dark-metric-card">
        <div>
            <div class="metric-info-title">Lokasi Rak</div>
            <div class="metric-info-val">{total_locations}</div>
        </div>
        <div class="pill-purple">Lihat Semua →</div>
    </div>
''', unsafe_allow_html=True)

st.write("")

# 8. Penapis Data
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

# 9. Senarai Inventori
st.markdown("### 📚 Senarai Inventori")

def get_status_html(qty):
    if qty <= 20:
        return "<span class='status-rendah'>Rendah</span>"
    elif qty <= 50:
        return "<span class='status-sederhana'>Sederhana</span>"
    else:
        return "<span class='status-ok'>OK</span>"

if not filtered_df.empty:
    if "Jadual" in view_mode:
        table_rows = ""
        for i, row in filtered_df.reset_index(drop=True).iterrows():
            status_tag = get_status_html(row['Quantity'])
            table_rows += f'''
                <tr>
                    <td>{i+1}</td>
                    <td><b>{row['P/N']}</b></td>
                    <td>{row['Description']}</td>
                    <td><code>{row['Location']}</code></td>
                    <td><b>{row['Quantity']}</b></td>
                    <td>{status_tag}</td>
                </tr>
            '''
        
        st.markdown(f'''
            <table class="custom-table">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>P/N</th>
                        <th>Nama Barang</th>
                        <th>Lokasi Rak</th>
                        <th>Stok</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
        ''', unsafe_allow_html=True)
    else:
        for idx, row in filtered_df.iterrows():
            st.markdown(f'''
                <div class="dark-metric-card">
                    <div>
                        <div style="font-size: 16px; font-weight: 800; color: #FFF;">P/N: {row['P/N']}</div>
                        <div style="font-size: 13px; color: #94A3B8;"><b>Barang:</b> {row['Description']} | <b>Rak:</b> 📍 {row['Location']}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 16px; font-weight: 800;">{row['Quantity']} unit</div>
                        <div style="margin-top: 4px;">{get_status_html(row['Quantity'])}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
else:
    st.warning("⚠️ Tiada maklumat rekod dijumpai.")

# 10. Sidebar Panel Kawalan (Tambah, Edit, Padam, Export)
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

    st.markdown('''
        <div class="sidebar-tips">
            <div style="font-weight: 700; color: #60A5FA; font-size: 13px;">💡 Tips</div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                Pastikan format P/N, lokasi rak dan kuantiti adalah betul sebelum menyimpan data.
            </div>
        </div>
    ''', unsafe_allow_html=True)
