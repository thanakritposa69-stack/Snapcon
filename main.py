import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. การตั้งค่าหน้าจอหลัก (Page Config)
# ==========================================
st.set_page_config(page_title="Personal Eng-Manager Dashboard", layout="wide")
st.title("📊 Engineering Workload & Resource Dashboard")
st.markdown("ระบบมอนิเตอร์สถานะโปรเจกต์และโหลดงานส่วนตัว (Skunkworks Project)")
st.markdown("---")

# ==========================================
# 2. จำลองข้อมูลจากตาราง Excel
# ==========================================
# แปลง Timeline (1-10) ให้เป็นวันที่จริง เพื่อให้วาดกราฟ Gantt ได้
today = datetime.today()

raw_data = [
    {"Project": "A", "Start_Day": 1, "End_Day": 2, "Assignee": "นาย ก"},
    {"Project": "A", "Start_Day": 2, "End_Day": 3, "Assignee": "นาย ข"},
    {"Project": "A", "Start_Day": 3, "End_Day": 4, "Assignee": "นาย จ"},
    {"Project": "B", "Start_Day": 2, "End_Day": 3, "Assignee": "นาย จ"},
    {"Project": "B", "Start_Day": 3, "End_Day": 4, "Assignee": "นาย ง"},
    {"Project": "B", "Start_Day": 4, "End_Day": 6, "Assignee": "นาย ค"},
    {"Project": "C", "Start_Day": 5, "End_Day": 7, "Assignee": "นาย ข"},
    {"Project": "C", "Start_Day": 7, "End_Day": 9, "Assignee": "นาย ง"},
    {"Project": "D", "Start_Day": 1, "End_Day": 5, "Assignee": "นาย ค"},
    {"Project": "E", "Start_Day": 2, "End_Day": 6, "Assignee": "นาย ก"},
    {"Project": "F", "Start_Day": 4, "End_Day": 10,"Assignee": "นาย จ"},
]

df = pd.DataFrame(raw_data)
# แปลง Day เป็น วันที่จริงสำหรับการแสดงผลใน Timeline
df["Start"] = df["Start_Day"].apply(lambda x: today + timedelta(days=x-1))
df["End"] = df["End_Day"].apply(lambda x: today + timedelta(days=x-1))
df["Task_Duration"] = df["End_Day"] - df["Start_Day"]

# ==========================================
# 3. ส่วน KPI สรุปผลด้านบน (Top Metrics)
# ==========================================
total_projects = df["Project"].nunique()
total_active_tasks = len(df)
# คำนวณหาคนที่รับงานเยอะที่สุด
busiest_person = df.groupby("Assignee")["Task_Duration"].sum().idxmax()

col1, col2, col3 = st.columns(3)
col1.metric("Active Projects (โปรเจกต์ที่รันอยู่)", f"{total_projects} โปรเจกต์")
col2.metric("Total Tasks (งานย่อยทั้งหมด)", f"{total_active_tasks} งาน")
col3.metric("🚨 High Workload Alert (คนโหลดสุด)", f"{busiest_person}")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 4. กราฟ Gantt Chart (มองภาพรวม Timeline)
# ==========================================
st.subheader("📅 Project Timeline (แยกสีตามพนักงาน)")
fig_timeline = px.timeline(
    df, 
    x_start="Start", 
    x_end="End", 
    y="Project", 
    color="Assignee",
    hover_name="Assignee",
    category_orders={"Project": ["F", "E", "D", "C", "B", "A"]} # เรียงจากบนลงล่าง
)
# ปรับแต่งกราฟให้ดูง่ายขึ้น
fig_timeline.update_yaxes(autorange="reversed") 
st.plotly_chart(fig_timeline, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. กราฟวิเคราะห์ Resource (กราฟแท่งคู่ด้านล่าง)
# ==========================================
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("👨‍🔧 ปริมาณงานรายบุคคล (Workload per Person)")
    # รวมจำนวนวันทำงานของแต่ละคน
    workload_df = df.groupby("Assignee")["Task_Duration"].sum().reset_index()
    fig_workload = px.bar(
        workload_df, 
        x="Assignee", 
        y="Task_Duration", 
        text="Task_Duration",
        labels={"Task_Duration": "ปริมาณงาน (วันรวม)", "Assignee": "พนักงาน"},
        color="Assignee"
    )
    # ใส่เส้นขีดจำกัด (Red Line)
    fig_workload.add_hline(y=5, line_dash="dot", annotation_text="ขีดจำกัดปกติ (Overload Line)", annotation_position="top left", line_color="red")
    st.plotly_chart(fig_workload, use_container_width=True)

with col_right:
    st.subheader("📦 สัดส่วนงานแต่ละโปรเจกต์ (Task by Project)")
    fig_project_dist = px.pie(
        df, 
        names="Project", 
        values="Task_Duration", 
        hole=0.4, # ทำเป็น Donut Chart ให้ดูทันสมัย
        color="Project"
    )
    st.plotly_chart(fig_project_dist, use_container_width=True)
