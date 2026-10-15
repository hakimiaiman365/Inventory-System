import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Inventori Rak", page_icon="📦", layout="centered"
)

# Auto-refresh setiap 10 minit
components.html(
    """
    <script>
        setTimeout(function(){
            window.parent.location.reload();
        }, 600000);
    </script>
    """,
    height=0,
)

st.markdown(
    """
<style>
.stApp { background-color: #070913; color: #E2E8F0; font-family: sans-serif; }
.hero-card { background: linear-gradient(135deg, #FF5E00 0%, #E60067 100%); border-radius: 16px; padding: 20px; color: white; margin-bottom: 14px; }
.inv-card { background-color: #111625; border: 1px solid #1C253B; border-radius: 12px; padding: 12px 16px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.loc-badge { background: #1E293B; color: #93C5FD; padding: 3px 8px; border-radius: 6px; font-family: monospace; font-weight: bold; }
.stTextInput input { background-color: #111625 !important; color: white !important; border: 1px solid #1C253B !important; border-radius: 12px !important; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(ttl=2)
def load_data():
  try:
    df = pd.read_csv("data.csv", dtype={"P/N": str})
    df["Quantity"] = (
        pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)
    )
    return df
  except:
    return pd.DataFrame(columns=["P/N", "Description", "Location", "Quantity"])


df = load_data()

st.markdown(
    """
<div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
    <span style="font-size: 30px;">📦</span>
    <div>
        <h1 style="margin: 0; font-size: 24px; font-weight: 900; color: white;">Inventori <span style="color: #FF7A00;">Rak</span></h1>
        <p style="margin: 0; font-size: 12px; color: #8A99AD;">Sistem Stok & Lokasi</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# Carian pantas terus keluar hasil tanpa perlu tekan Enter
search = st.text_input(
    "Carian", placeholder="Taip P/N atau lokasi rak...", label_visibility="collapsed"
)

total_qty = int(df["Quantity"].sum()) if not df.empty else 0
total_pn = len(df)

st.markdown(
    f"""
<div class="hero-card">
    <div style="font-size: 11px; font-weight: bold; text-transform: uppercase;">Jumlah Kuantiti Stok</div>
    <div style="font-size: 32px; font-weight: 900; line-height: 1.2;">{total_qty:,} <span style="font-size: 14px; font-weight: normal;">unit</span></div>
    <div style="margin-top: 8px; font-size: 12px; background: rgba(0,0,0,0.2); display: inline-block; padding: 4px 10px; border-radius: 12px;">📦 {total_pn} Part Number Berdaftar</div>
</div>
""",
    unsafe_allow_html=True,
)

filtered_df = df.copy()
if search:
  mask = (
      filtered_df["P/N"]
      .astype(str)
      .str.contains(search, case=False, na=False)
      | filtered_df["Description"]
      .astype(str)
      .str.contains(search, case=False, na=False)
      | filtered_df["Location"]
      .astype(str)
      .str.contains(search, case=False, na=False)
  )
  filtered_df = filtered_df[mask]

st.markdown(
    "<h3 style='font-size: 16px; margin-top: 15px;'>Senarai Inventori</h3>",
    unsafe_allow_html=True,
)

if not filtered_df.empty:
  for _, row in filtered_df.iterrows():
    st.markdown(
        f"""
    <div class="inv-card">
        <div>
            <div style="font-size: 14px; font-weight: 800; color: white;">P/N: {row['P/N']}</div>
            <div style="font-size: 12px; color: #8A99AD; margin-top: 2px;">{row['Description']} | Rak: <span class="loc-badge">{row['Location']}</span></div>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 14px; font-weight: 800; color: white;">{row['Quantity']} unit</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )
else:
  st.warning("Tiada rekod dijumpai.")

with st.sidebar:
  st.header("Panel Kawalan")
  if st.button("Muat Turun CSV", use_container_width=True):
    st.download_button(
        "Klik untuk Download",
        df.to_csv(index=False).encode("utf-8"),
        "inventori.csv",
        "text/csv",
    )
