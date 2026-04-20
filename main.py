import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. SETUP & SESSION STATE (เก็บข้อมูลให้คงอยู่) ---
st.set_page_config(page_title="Master Engineering Control", layout="wide")

if 'team' not in st.session_state:
    st.session_state.team = [f"นาย {n}" for n in ["ก", "ข", "ค", "ง", "จ", "ฉ", "ช", "ซ", "ฌ", "ญ"]]

if 'projects' not in st.session_state:
    # เริ่มต้นด้วย 1 โปรเจกต์ตัวอย่าง (สามารถเพิ่มได้ถึง 10)
    st.session_state.projects = {
        "Snapcon Project 01": {
            "start": datetime.today(),
            "tasks": [{"name": f"งานย่อยที่ {i+1}", "who": "นาย ก", "done": False} for i in range(5)]
        }
    }

# --- 2. SIDEBAR: CONTROL PANEL (จัดการคนและโปรเจกต์) ---
with st.sidebar:
    st.header("⚙️ การตั้งค่าระบบ")
    
    # ส่วนจัดการรายชื่อพนักงาน
    with st.expander("👥 จัดการรายชื่อทีม (10 คน)"):
        for i in range(10):
            st.session_state.team[i] = st.text_input(f"คนที่ {i+1}", st.session_state.team[i], key=f"t_{i}")
    
    st.divider()
    
    # ส่วนเพิ่มโปรเจกต์ใหม่
    new_p = st.text_input("➕ ชื่อโปรเจกต์ใหม่")
    if st.button("เพิ่มโปรเจกต์") and new_p:
        if len(st.session_state.projects) < 10:
            st.session_state.projects[new_p] = {
                "start": datetime.today(),
                "tasks": [{"name": "งานเริ่มต้น", "who": st.session_state.team[0], "done": False}]
            }
        else:
            st.error("จำกัดสูงสุด 10 โปรเจกต์")

# --- 3. MAIN DASHBOARD ---
st.title("🚀 Engineering Master Command Center")

# ส่วนที่ 1: รายละเอียดงาน (Task Management)
st.subheader("📝 รายละเอียดงานย่อย (20 เรื่องต่อโปรเจกต์)")
for p_name, p_data in st.session_state.projects.items():
    # คำนวณ % ความสำเร็จ
    done_count = sum(1 for t in p_data['tasks'] if t['done'])
    total_count = len(p_data['tasks'])
    progress = done_count / total_count if total_count > 0 else 0
    
    with st.expander(f"📂 {p_name} | ความคืบหน้า {progress:.0%}"):
        st.progress(progress)
        
        # แสดงรายการงานย่อย
        for idx, task in enumerate(p_data['tasks']):
            c1, c2, c3 = st.columns([0.1, 0.5, 0.4])
            task['done'] = c1.checkbox("", value=task['done'], key=f"check_{p_name}_{idx}")
            task['name'] = c2.text_input("ชื่องาน", value=task['name'], key=f"name_{p_name}_{idx}", label_visibility="collapsed")
            task['who'] = c3.selectbox("ผู้รับผิดชอบ", st.session_state.team, index=st.session_state.team.index(task['who']) if task['who'] in st.session_state.team else 0, key=f"who_{p_name}_{idx}", label_visibility="collapsed")
        
        if st.button(f"➕ เพิ่มงานย่อยใน {p_name}", key=f"add_{p_name}"):
            if len(p_data['tasks']) < 20:
                p_data['tasks'].append({"name": "งานใหม่", "who": st.session_state.team[0], "done": False})
                st.rerun()

st.divider()

# ส่วนที่ 2: วิเคราะห์ภาพรวม (Gantt & Workload)
st.subheader("📊 วิเคราะห์ภาพรวมแผนก")

# เตรียมข้อมูลสำหรับ Gantt
gantt_list = []
workload_data = {name: 0 for name in st.session_state.team}

for p_name, p_data in st.session_state.projects.items():
    for task in p_data['tasks']:
        gantt_list.append({
            "Project": p_name,
            "Task": task['name'],
            "Assignee": task['who'],
            "Status": "Done" if task['done'] else "Pending",
            "Start": p_data['start'],
            "End": p_data['start'] + timedelta(days=2) # สมมติระยะเวลา
        })
        if not task['done']:
            workload_data[task['who']] += 1

if gantt_list:
    df_gantt = pd.DataFrame(gantt_list)
    fig = px.timeline(df_gantt, x_start="Start", x_end="End", y="Project", color="Assignee", text="Task")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    # กราฟโหลดงาน
    st.subheader("👨‍🔧 โหลดงานที่ยังค้างอยู่ (Pending Tasks)")
    df_load = pd.DataFrame(list(workload_data.items()), columns=['Name', 'Tasks'])
    fig_load = px.bar(df_load, x='Name', y='Tasks', color='Tasks', color_continuous_scale='Reds')
    st.plotly_chart(fig_load, use_container_width=True)
