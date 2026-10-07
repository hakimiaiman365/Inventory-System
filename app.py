import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Tema
st.set_page_config(
    page_title="Sistem Pengurusan Inventori Rak",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk Rekaan Moden & Profesional
st.markdown("""
    <style>
    /* Styling Kad Utama */
    .metric-card {
        background-color: #1e222d;
        border: 1px solid #2e364f;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #4da6ff;
    }
    .metric-label {
        font-size: 14px;
        color: #a0aec0;
    }
    
    /* Styling Badge Status Stok */
    .badge-ok {
        background-color: #1c4532;
        color: #68d391;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-low {
        background-color: #742a2a;
        color: #feb2b2;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .location-tag {
        background-color: #2b6cb0;
        color: #ffffff;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 13px;
        font-weight: 600;
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
st.title("📦 Sistem Pengurusan Inventori Rak")
st.caption("Pangkalan Data Carian, Kawalan Stok, & Lokasi Rak Barangan")

# 📊 Dashboard Ringkasan (Metrics)
m1, m2, m3, m4 = st.columns(4)

total_pn = len(df)
total_qty = int(df["Quantity"].sum()) if not df.empty else 0
low_stock_df = df[df['Quantity'] <= 50] if not df.empty else pd.DataFrame()
low_stock_count = len(low_stock_df)
total_locations = df['Location'].nunique() if not df.empty else 0

m1.markdown(f'<div class="metric-card"><div class="metric-value">{total_pn}</div><div class="metric-label">Total P/N Berdaftar</div></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card"><div class="metric-value">{total_qty}</div><div class="metric-label">Jumlah Unit Stok</div></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #feb2b2;">{low_stock_count}</div><div class="metric-label">Item Stok Rendah (≤50)</div></div>', unsafe_allow_html=True)
m4.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #68d391;">{total_locations}</div><div class="metric-label">Jumlah Lokasi Rak</div></div>', unsafe_allow_html=True)

st.divider()

# ⚠️ Ruang Khas: Tekan Untuk Lihat Senarai Stok Rendah
with st.expander(f"🔴 Tekan Sini Untuk Lihat Senarai P/N Stok Rendah ≤ 50 Unit ({low_stock_count} item)", expanded=False):
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

# 🔍 Carian dan Penapis (Filters)
col_search, col_filter, col_view = st.columns([3, 2, 2])

with col_search:
    search = st.text_input("🔍 Carian Pantas", placeholder="Taip P/N, Description, atau Lokasi...")

with col_filter:
    filter_low_stock = st.checkbox("⚠️ Papar Stok Rendah Sahaja (≤ 50 unit)")

with col_view:
    view_type = st.radio("Mod Paparan:", ["Jadual (Table)", "Kad (Cards)"], horizontal=True)

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

# 📋 Paparan Data Utama
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
        
        if st.button("💾 Simpan / Update Data", use_container_width=True):
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
