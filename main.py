import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- CONFIG & STYLING ---
st.set_page_config(page_title="Engineering Gantt Dashboard", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATA PREPARATION ---
today = datetime.today()
raw_data = [
    {"Project": "Project A", "Start_Day": 1, "End_Day": 2, "Assignee": "นาย ก"},
    {"Project": "Project A", "Start_Day": 2, "End_Day": 3, "Assignee": "นาย ข"},
    {"Project": "Project A", "Start_Day": 3, "End_Day": 4, "Assignee": "นาย จ"},
    {"Project": "Project B", "Start_Day": 2, "End_Day": 3, "Assignee": "นาย จ"},
    {"Project": "Project B", "Start_Day": 3, "End_Day": 4, "Assignee": "นาย ง"},
    {"Project": "Project B", "Start_Day": 4, "End_Day": 6, "Assignee": "นาย ค"},
    {"Project": "Project C", "Start_Day": 5, "End_Day": 7, "Assignee": "นาย ข"},
    {"Project": "Project C", "Start_Day": 7, "End_Day": 9, "Assignee": "นาย ง"},
    {"Project": "Project D", "Start_Day": 1, "End_Day": 5, "Assignee": "นาย ค"},
    {"Project": "Project E", "Start_Day": 2, "End_Day": 6, "Assignee": "นาย ก"},
    {"Project": "Project F", "Start_Day": 4, "End_Day": 10, "Assignee": "นาย จ"},
]

df = pd.DataFrame(raw_data)
df["Start"] = df["Start_Day"].apply(lambda x: today + timedelta(days=x-1))
df["End"] = df["End_Day"].apply(lambda x: today + timedelta(days=x)) # เพิ่ม 1 วันเพื่อให้เห็นจบวันนั้นๆ
df["Duration"] = df["End_Day"] - df["Start_Day"]

# --- 2. SIDEBAR FILTER ---
st.sidebar.header("🛠 Control Panel")
selected_assignee = st.sidebar.multiselect("กรองตามรายชื่อพนักงาน:", options=df["Assignee"].unique(), default=df["Assignee"].unique())
filtered_df = df[df["Assignee"].isin(selected_assignee)]

# --- 3. TOP METRICS ---
st.title("📌 Engineering Project Schedule")
st.caption(f"อัปเดตล่าสุด: {today.strftime('%d %B %Y')}")

m1, m2, m3, m4 = st.columns(4)
m1.metric("โปรเจกต์ทั้งหมด", df["Project"].nunique())
m2.metric("จำนวนงาน (Tasks)", len(filtered_df))

# คำนวณ Load นาย จ (ตัวอย่างการเฝ้าระวัง)
p_load = df.groupby("Assignee")["Duration"].sum()
m3.metric("โหลดงานเฉลี่ย", f"{p_load.mean():.1f} วัน/คน")
m4.metric("Busiest Person", p_load.idxmax(), delta="Overloaded", delta_color="inverse")

st.markdown("---")

# --- 4. GANTT CHART (BEAUTIFIED) ---
st.subheader("🗓 แผนผังการดำเนินงาน (Gantt Chart)")

# เลือกใช้สี Pastel
color_map = {
    "นาย ก": "#8ECAE6", "นาย ข": "#219EBC", 
    "นาย ค": "#FFB703", "นาย ง": "#FB8500", "นาย จ": "#FF006E"
}

fig = px.timeline(
    filtered_df, 
    x_start="Start", 
    x_end="End", 
    y="Project", 
    color="Assignee",
    text="Assignee",
    color_discrete_map=color_map,
    hover_data={"Start": "|%d %b", "End": "|%d %b", "Duration": True}
)

fig.update_layout(
    xaxis_title="Timeline",
    yaxis_title="",
    height=450,
    margin=dict(l=20, r=20, t=20, b=20),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=True,
    legend_title_text="พนักงาน",
    font=dict(family="Arial", size=12)
)

# เพิ่มเส้น Grid ให้ดูง่าย
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
fig.update_yaxes(autorange="reversed", showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

# ทำให้แท่งกราฟมนและมีช่องไฟ
fig.update_traces(marker_line_color='rgb(255,255,255)', marker_line_width=1.5, opacity=0.85)

st.plotly_chart(fig, use_container_width=True)

# --- 5. WORKLOAD ANALYSIS TABLE ---
st.markdown("---")
col_a, col_b = st.columns([1, 1])

with col_a:
    st.subheader("📊 ตารางสรุปโหลดงาน (Workload Summary)")
    summary_table = filtered_df.groupby("Assignee").agg(
        จำนวนงาน=('Project', 'count'),
        ระยะเวลารวม_วัน=('Duration', 'sum')
    ).sort_values("ระยะเวลารวม_วัน", ascending=False)
    st.dataframe(summary_table, use_container_width=True)

with col_b:
    st.subheader("⚠️ การวิเคราะห์ทรัพยากร")
    if p_load.max() > 7:
        st.error(f"ตรวจพบปัญหา: **{p_load.idxmax()}** มีงานสะสมมากเกินไป อาจส่งผลต่อคุณภาพงาน")
    else:
        st.success("การกระจายงานอยู่ในระดับที่เหมาะสม")
