import streamlit as st
import pandas as pd

# Konfigurasi Halaman
st.set_page_config(page_title="Sistem Inventori Rak", page_icon="📦", layout="wide")

st.title("📦 Sistem Carian & Lokasi Inventori Rak")

# Fungsi Muat Data
@st.cache_data(ttl=2)
def load_data():
    try:
        return pd.read_csv("data.csv", dtype={"P/N": str})
    except Exception:
        return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])

df = load_data()

# Ruang Carian Utama
search = st.text_input("🔍 Taip Part Number (P/N), Description, atau Lokasi Rak (cth: R1-A-1):", "")

# Filter Data
if search:
    mask = (
        df['P/N'].astype(str).str.contains(search, case=False, na=False) |
        df['Description'].astype(str).str.contains(search, case=False, na=False) |
        df['Location'].astype(str).str.contains(search, case=False, na=False)
    )
    filtered_df = df[mask]
else:
    filtered_df = df

# Dashboard KPI Ringkas
c1, c2, c3 = st.columns(3)
c1.metric("Total P/N Registered", len(df))
c2.metric("Jumlah Unit Stok", int(df["Quantity"].sum()) if not df.empty else 0)
c3.metric("Item Dijumpai", len(filtered_df))

st.divider()

# Paparan Senarai Barang
if not filtered_df.empty:
    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 4, 2, 2])
            col1.markdown(f"**P/N:** `{row['P/N']}`")
            col2.write(f"**Description:** {row['Description']}")
            col3.markdown(f"**Lokasi Rak:** 📍 `{row['Location']}`")
            col4.write(f"**Kuantiti:** {row['Quantity']} unit")
            st.divider()
else:
    st.warning("⚠️ Tiada barang dijumpai mengikut carian tersebut.")

# Sidebar untuk Tambah / Kemaskini / Padam
with st.sidebar:
    tab1, tab2 = st.tabs(["➕ Tambah / Edit", "🗑️ Padam Item"])
    
    with tab1:
        st.header("⚙️ Tambah / Kemaskini")
        pn = st.text_input("Part Number (P/N)")
        desc = st.text_input("Description")
        loc = st.text_input("Kod Lokasi Rak (cth: R2-B-1)")
        qty = st.number_input("Kuantiti (Qty)", min_value=0, value=1)
        
        if st.button("Simpan Data"):
            if pn and loc:
                if pn in df['P/N'].astype(str).values:
                    df.loc[df['P/N'].astype(str) == pn, ['Description', 'Location', 'Quantity']] = [desc, loc, qty]
                else:
                    new_row = pd.DataFrame([{"P/N": str(pn), "Description": desc, "Location": loc, "Quantity": qty}])
                    df = pd.concat([df, new_row], ignore_index=True)
                
                df.to_csv("data.csv", index=False)
                st.success(f"Data P/N {pn} berjaya disimpan!")
                st.rerun()
            else:
                st.error("Sila pastikan P/N dan Lokasi diisi.")

    with tab2:
        st.header("🗑️ Padam P/N")
        if not df.empty:
            # Pilihan dropdown P/N & Description
            options = df.apply(lambda r: f"{r['P/N']} - {r['Description']}", axis=1).tolist()
            selected_option = st.selectbox("Pilih item untuk dipadam:", options)
            
            if st.button("🚨 Padam Item Ini", type="primary"):
                selected_pn = selected_option.split(" - ")[0]
                df = df[df['P/N'].astype(str) != str(selected_pn)]
                df.to_csv("data.csv", index=False)
                st.success(f"P/N {selected_pn} berjaya dipadam!")
                st.rerun()
        else:
            st.info("Tiada data stok.")
