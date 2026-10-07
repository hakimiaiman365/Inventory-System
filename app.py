import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
from io import BytesIO

# ============================================================
# 📦 INVENTORI RAK
# Sistem Stok & Lokasi Rak
# ============================================================

DB_FILE = "inventory.db"
LOW_STOCK_LIMIT = 50

st.set_page_config(
    page_title="Inventori Rak",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DATABASE
# ============================================================

def get_conn():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part_number TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            rack_location TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL
        )
    """)

    conn.commit()
    return conn


conn = get_conn()


def load_data():
    return pd.read_sql_query(
        """
        SELECT
            id,
            part_number,
            description,
            rack_location,
            quantity,
            updated_at
        FROM inventory
        ORDER BY id DESC
        """,
        conn
    )


def save_item(part_number, description, rack_location, quantity):

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn.execute("""
        INSERT INTO inventory
        (
            part_number,
            description,
            rack_location,
            quantity,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)

        ON CONFLICT(part_number)
        DO UPDATE SET
            description = excluded.description,
            rack_location = excluded.rack_location,
            quantity = excluded.quantity,
            updated_at = excluded.updated_at
    """, (
        part_number.strip().upper(),
        description.strip(),
        rack_location.strip().upper(),
        int(quantity)
    ))

    conn.commit()


def delete_item(part_number):

    conn.execute(
        "DELETE FROM inventory WHERE part_number = ?",
        (part_number,)
    )

    conn.commit()


# ============================================================
# DEMO DATA
# ============================================================

def seed_demo_data():

    demo = [
        ("P00123", "Server Board", "R2-B-1", 83),
        ("P00456", "Memory DIMM", "R1-A-3", 12),
        ("P00789", "PSU 1200W", "R2-C-2", 36),
        ("P01011", "SSD 1.92TB", "R3-D-1", 5),
        ("P01337", "Fan Module", "R1-B-4", 50),
        ("P01771", "CPLD", "R2-A-2", 3),
        ("P02022", "Cable Network", "R3-C-3", 28),
        ("P02468", "Power Module", "R1-C-1", 72),
        ("P02880", "HDD 4TB", "R2-B-3", 9),
        ("P03102", "DIMM 32GB", "R3-A-1", 18),
    ]

    for item in demo:
        save_item(*item)


# ============================================================
# CUSTOM DESIGN
# ============================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(91,54,255,.16),
            transparent 30%
        ),

        radial-gradient(
            circle at 95% 5%,
            rgba(255,145,0,.12),
            transparent 25%
        ),

        #080b16;

    color: #f7f8ff;
}

.block-container {

    max-width: 1500px;

    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* SIDEBAR */

[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #0d1020 0%,
            #11142a 100%
        );

    border-right:
        1px solid rgba(126,103,255,.22);
}

[data-testid="stSidebar"] * {
    color: #e9ebff;
}


/* HEADER */

.hero {

    border:
        1px solid rgba(112,82,255,.45);

    border-radius: 26px;

    padding: 28px 30px;

    background:

        radial-gradient(
            circle at 85% 20%,
            rgba(255,132,0,.35),
            transparent 25%
        ),

        linear-gradient(
            135deg,
            #101633,
            #14113b 55%,
            #29154a
        );

    box-shadow:
        0 20px 60px rgba(0,0,0,.28);

    margin-bottom: 22px;
}

.hero-title {

    font-size: 40px;

    font-weight: 800;

    margin: 0;
}

.hero-title span {
    color: #ff9d00;
}

.hero-sub {

    color: #aeb6d7;

    margin-top: 5px;

    font-size: 14px;
}


/* DASHBOARD CARD */

.metric {

    border-radius: 22px;

    padding: 23px;

    min-height: 145px;

    border:
        1px solid rgba(123,99,255,.35);

    background:
        linear-gradient(
            145deg,
            #111734,
            #0c1127
        );

    box-shadow:
        0 12px 40px rgba(0,0,0,.20);
}


.metric-orange {

    background:
        linear-gradient(
            135deg,
            #ffb000 0%,
            #ff6d22 48%,
            #b52cff 100%
        );

    border: none;
}


.metric-danger {

    border-color:
        rgba(255,68,90,.65);

    background:
        linear-gradient(
            145deg,
            #1c1327,
            #170e1a
        );
}


.metric-label {

    color: #aab3cf;

    font-size: 14px;

    font-weight: 600;
}


.metric-orange .metric-label {
    color: rgba(255,255,255,.88);
}


.metric-value {

    font-size: 39px;

    font-weight: 800;

    margin-top: 5px;
}


.metric-small {

    color: #aab3cf;

    font-size: 13px;

    margin-top: 4px;
}


/* GENERAL CARD */

.card {

    border:
        1px solid rgba(116,91,255,.30);

    border-radius: 22px;

    padding: 22px;

    background:
        linear-gradient(
            145deg,
            rgba(19,24,52,.96),
            rgba(10,14,31,.96)
        );

    box-shadow:
        0 12px 40px rgba(0,0,0,.20);
}


/* STATUS */

.status-ok {

    display: inline-block;

    padding: 5px 12px;

    border-radius: 99px;

    background: #0a9d68;

    color: white;

    font-size: 12px;

    font-weight: 700;
}


.status-low {

    display: inline-block;

    padding: 5px 12px;

    border-radius: 99px;

    background: #ff4056;

    color: white;

    font-size: 12px;

    font-weight: 700;
}


/* SECTION */

.section-title {

    font-size: 21px;

    font-weight: 800;

    margin:
        12px 0 14px 0;
}


/* INFO */

.info-box {

    border:
        1px solid rgba(121,93,255,.35);

    border-radius: 18px;

    padding: 17px;

    background:
        rgba(19,20,55,.65);

    margin-top: 12px;
}


/* TIP */

.tip {

    border:
        1px solid rgba(164,95,255,.5);

    background:
        linear-gradient(
            135deg,
            rgba(82,46,160,.18),
            rgba(22,26,68,.65)
        );

    border-radius: 18px;

    padding: 17px;

    color: #d8d7ff;
}


/* BUTTON */

div.stButton > button {

    border-radius: 13px;

    border:
        1px solid rgba(121,96,255,.55);

    background:
        linear-gradient(
            135deg,
            #5d3cff,
            #8d32ff
        );

    color: white;

    font-weight: 700;
}


div.stButton > button:hover {

    border-color: #ff9f18;

    color: white;

    box-shadow:
        0 0 22px rgba(255,133,0,.20);
}


/* INPUT */

div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div {

    background: #0d101d;

    border:
        1px solid #30375c;

    border-radius: 12px;
}


div[data-baseweb="select"] > div {

    background: #0d101d;

    border-radius: 12px;
}


.stTextInput label,
.stNumberInput label,
.stTextArea label,
.stSelectbox label,
.stRadio label,
.stCheckbox label {

    color: #d9dcf1 !important;

    font-weight: 600;
}


/* DOWNLOAD */

[data-testid="stDownloadButton"] button {

    background:
        linear-gradient(
            135deg,
            #ff9e00,
            #ff4f75
        );

    color: white;

    border: none;

    font-weight: 800;
}


.small-muted {

    color: #8e97b8;

    font-size: 12px;
}


hr {

    border-color:
        rgba(125,110,190,.20);
}


</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        📦 Inventori <span>Rak</span>
    </div>

    <div class="hero-sub">
        Sistem Stok & Lokasi Rak
        • Pengurusan inventori yang pantas dan mudah
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

df = load_data()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Panel Kawalan")

    st.caption(
        "Tambah, kemaskini atau padam data inventori."
    )

    action = st.radio(
        "Tindakan",
        [
            "➕ Kemaskini / Tambah",
            "🗑️ Padam",
            "📥 Muat Turun"
        ]
    )


    # ========================================================
    # ADD / UPDATE
    # ========================================================

    if action == "➕ Kemaskini / Tambah":

        st.markdown("### 📦 Data Barang")

        selected_pn = ""

        if not df.empty:

            options = [
                "-- P/N Baru --"
            ] + df["part_number"].tolist()

            selected = st.selectbox(
                "Pilih P/N sedia ada",
                options
            )

            if selected != "-- P/N Baru --":
                selected_pn = selected


        existing = df[
            df["part_number"] == selected_pn
        ]


        default_desc = (
            existing.iloc[0]["description"]
            if not existing.empty
            else ""
        )


        default_rack = (
            existing.iloc[0]["rack_location"]
            if not existing.empty
            else ""
        )


        default_qty = (
            int(existing.iloc[0]["quantity"])
            if not existing.empty
            else 1
        )


        pn = st.text_input(
            "Part Number (P/N) *",
            value=selected_pn,
            placeholder="Contoh: P00123"
        )


        desc = st.text_input(
            "Description *",
            value=default_desc,
            placeholder="Contoh: Server Board / Memory DIMM"
        )


        rack = st.text_input(
            "Lokasi Rak *",
            value=default_rack,
            placeholder="Contoh: R2-B-1"
        )


        qty = st.number_input(
            "Kuantiti (Qty) *",
            min_value=0,
            value=default_qty,
            step=1
        )


        if st.button(
            "💾 Simpan / Update Data",
            use_container_width=True
        ):

            if (
                not pn.strip()
                or not desc.strip()
                or not rack.strip()
            ):

                st.error(
                    "Sila lengkapkan P/N, Description dan Lokasi Rak."
                )

            else:

                save_item(
                    pn,
                    desc,
                    rack,
                    qty
                )

                st.success(
                    f"Data {pn.upper()} berjaya disimpan."
                )

                st.rerun()


    # ========================================================
    # DELETE
    # ========================================================

    elif action == "🗑️ Padam":

        st.markdown("### 🗑️ Padam Barang")

        if df.empty:

            st.info(
                "Tiada data untuk dipadam."
            )

        else:

            del_pn = st.selectbox(
                "Pilih P/N",
                df["part_number"].tolist()
            )


            if st.button(
                "🗑️ Padam Data",
                use_container_width=True
            ):

                delete_item(del_pn)

                st.success(
                    f"{del_pn} telah dipadam."
                )

                st.rerun()


    # ========================================================
    # DOWNLOAD
    # ========================================================

    else:

        st.markdown("### 📥 Export")

        st.write(
            "Muat turun keseluruhan inventori."
        )


        csv_data = df.to_csv(
            index=False
        ).encode("utf-8-sig")


        st.download_button(
            "⬇️ Download CSV",
            csv_data,
            "inventori_rak.csv",
            "text/csv",
            use_container_width=True
        )


        excel_buffer = BytesIO()


        with pd.ExcelWriter(
            excel_buffer,
            engine="openpyxl"
        ):

            df.to_excel(
                excel_buffer,
                index=False,
                sheet_name="Inventori"
            )


        st.download_button(
            "📊 Download Excel",
            excel_buffer.getvalue(),
            "inventori_rak.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )


    st.markdown("---")


    if st.button(
        "🧪 Isi Data Demo",
        use_container_width=True
    ):

        seed_demo_data()

        st.success(
            "Data demo dimasukkan."
        )

        st.rerun()


# ============================================================
# DASHBOARD CALCULATION
# ============================================================

total_qty = (
    int(df["quantity"].sum())
    if not df.empty
    else 0
)


total_pn = len(df)


low_df = (
    df[df["quantity"] <= LOW_STOCK_LIMIT]
    if not df.empty
    else pd.DataFrame()
)


low_count = len(low_df)


rack_count = (
    df["rack_location"].nunique()
    if not df.empty
    else 0
)


# ============================================================
# DASHBOARD CARDS
# ============================================================

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(f"""
    <div class="metric metric-orange">

        <div class="metric-label">
            📦 JUMLAH KUANTITI STOK
        </div>

        <div class="metric-value">
            {total_qty:,}
            <span style="
                font-size:18px;
                font-weight:500;
            ">
                unit
            </span>
        </div>

        <div class="metric-small">
            📦 {total_pn} Part Number Berdaftar
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="metric">

        <div class="metric-label">
            🔢 TOTAL P/N
        </div>

        <div class="metric-value">
            {total_pn}
        </div>

        <div class="metric-small">
            Part Number aktif
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="metric metric-danger">

        <div class="metric-label">
            ⚠️ STOK RENDAH (≤50)
        </div>

        <div class="metric-value"
             style="color:#ff6478">

            {low_count}

        </div>

        <div class="metric-small">
            Perlu diperiksa
        </div>

    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# SEARCH
# ============================================================

st.markdown(
    '<div class="section-title">🔎 Carian Inventori</div>',
    unsafe_allow_html=True
)


search_col, filter_col, view_col = st.columns(
    [5, 2, 2]
)


with search_col:

    search = st.text_input(
        "Carian",
        placeholder=
        "Taip P/N, nama barang, atau lokasi rak...",
        label_visibility="collapsed"
    )


with filter_col:

    low_only = st.checkbox(
        "⚠️ Stok Rendah Sahaja (≤50)"
    )


with view_col:

    view = st.radio(
        "Paparan",
        ["Jadual", "Kad"],
        horizontal=True,
        label_visibility="collapsed"
    )


# ============================================================
# FILTER
# ============================================================

filtered = df.copy()


if search:

    s = search.lower().strip()

    mask = (

        filtered["part_number"]
        .str.lower()
        .str.contains(s, na=False)

        |

        filtered["description"]
        .str.lower()
        .str.contains(s, na=False)

        |

        filtered["rack_location"]
        .str.lower()
        .str.contains(s, na=False)
    )

    filtered = filtered[mask]


if low_only:

    filtered = filtered[
        filtered["quantity"] <= LOW_STOCK_LIMIT
    ]


# ============================================================
# INVENTORY LIST
# ============================================================

st.markdown(
    f"""
    <div class="section-title">
        📋 Senarai Inventori
        <span class="small-muted">
            ({len(filtered)} item)
        </span>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TABLE VIEW
# ============================================================

if view == "Jadual":

    if filtered.empty:

        st.info(
            "Tiada inventori dijumpai."
        )

    else:

        display = filtered.copy()


        display.insert(
            0,
            "#",
            range(
                1,
                len(display) + 1
            )
        )


        display["Status"] = display[
            "quantity"
        ].apply(

            lambda x:
                "🔴 Rendah"
                if x <= LOW_STOCK_LIMIT
                else "🟢 OK"
        )


        display = display.rename(
            columns={
                "part_number":
                    "P/N",

                "description":
                    "Nama Barang",

                "rack_location":
                    "Lokasi Rak",

                "quantity":
                    "Stok",

                "updated_at":
                    "Kemaskini"
            }
        )


        st.dataframe(

            display[
                [
                    "#",
                    "P/N",
                    "Nama Barang",
                    "Lokasi Rak",
                    "Stok",
                    "Status",
                    "Kemaskini"
                ]
            ],

            use_container_width=True,

            hide_index=True,

            height=500
        )


# ============================================================
# CARD VIEW
# ============================================================

else:

    if filtered.empty:

        st.info(
            "Tiada inventori dijumpai."
        )

    else:

        cards = filtered.to_dict(
            "records"
        )


        for start in range(
            0,
            len(cards),
            3
        ):

            cols = st.columns(3)


            for col, item in zip(
                cols,
                cards[start:start + 3]
            ):

                if (
                    item["quantity"]
                    <= LOW_STOCK_LIMIT
                ):

                    status_class = (
                        "status-low"
                    )

                    status_text = (
                        "RENDAH"
                    )

                else:

                    status_class = (
                        "status-ok"
                    )

                    status_text = (
                        "OK"
                    )


                with col:

                    st.markdown(
                        f"""
                        <div class="card"
                             style="margin-bottom:15px">

                            <div style="
                                display:flex;
                                justify-content:space-between;
                                gap:8px;
                            ">

                                <b style="
                                    font-size:17px;
                                ">
                                    {item["part_number"]}
                                </b>

                                <span class="
                                    {status_class}
                                ">
                                    {status_text}
                                </span>

                            </div>


                            <div style="
                                margin-top:15px;
                                color:#d9dcf1;
                                font-weight:600;
                            ">

                                {item["description"]}

                            </div>


                            <div class="small-muted"
                                 style="margin-top:12px">

                                📍
                                {item["rack_location"]}

                            </div>


                            <div style="
                                margin-top:12px;
                                font-size:28px;
                                font-weight:800;
                            ">

                                {item["quantity"]}

                                <span style="
                                    font-size:13px;
                                    color:#8e97b8;
                                ">
                                    unit
                                </span>

                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ============================================================
# QUICK INFORMATION
# ============================================================

st.write("")


a, b = st.columns(2)


with a:

    st.markdown(
        f"""
        <div class="info-box">

            <b>📍 Lokasi Rak</b>

            <br>

            <span style="
                font-size:28px;
                font-weight:800;
            ">
                {rack_count}
            </span>

            <span class="small-muted">
                lokasi unik
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


with b:

    st.markdown(
        """
        <div class="tip">

            💡 <b>Tips</b>

            <br>

            Pastikan format P/N,
            lokasi rak dan kuantiti
            adalah betul sebelum
            menyimpan data.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")


st.markdown(
    """
    <div style="
        text-align:center;
        color:#717a9d;
        font-size:12px;
    ">

        📦 Inventori Rak
        • Sistem Pengurusan Stok & Lokasi
        • SQLite Database

    </div>
    """,
    unsafe_allow_html=True
)
