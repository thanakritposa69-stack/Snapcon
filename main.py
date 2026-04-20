import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- 1. การตั้งค่าเบื้องต้น ---
st.set_page_config(page_title="Snapcon Eng-Command Center", layout="wide")

# --- 2. การจัดการข้อมูล (Session State) ---
# กำหนดรายชื่อทีมเริ่มต้น 10 คน
if 'team_members' not in st.session_state:
    st.session_state.team_members = [f"นาย {n}" for n in ["ก", "ข", "ค", "ง", "จ", "ฉ", "ช", "ซ", "ฌ", "ญ"]]

# กำหนดโครงสร้างข้อมูลโปรเจกต์
if 'projects_db' not in st.session_state:
    st.session_state.projects_db = {
        "Snapcon Project Alpha": {
            "start_date": datetime.today().date(),
            "end_date": (datetime.today() + timedelta(days=7)).date(),
            "sub_tasks": [{"name": "เตรียมแบบ Drawing", "who": "นาย ก", "done": False}]
        }
    }

# --- 3. ส่วนควบคุมด้านข้าง (Sidebar) ---
with st.sidebar:
    st.header("⚙️ ระบบจัดการพื้นฐาน")
    
    # แก้ไขรายชื่อทีม 10 คน
    with st.expander("👥 แก้ไขชื่อทีมงาน"):
        for i in range(10):
            st.session_state.team_members[i] = st.text_input(f"พนักงานคนที่ {i+1}", st.session_state.team_members[i], key=f"team_{i}")
    
    st.divider()
    
    # เพิ่มโปรเจกต์ใหม่ (สูงสุด 10)
    st.subheader("➕ เพิ่มโปรเจกต์ใหม่")
    new_p_name = st.text_input("ชื่อโปรเจกต์")
    if st.button("บันทึกโปรเจกต์ใหม่"):
        if new_p_name and len(st.session_state.projects_db) < 10:
            st.session_state.projects_db[new_p_name] = {
                "start_date": datetime.today().date(),
                "end_date": (datetime.today() + timedelta(days=7)).date(),
                "sub_tasks": [{"name": "งานเริ่มต้น", "who": st.session_state.team_members[0], "done": False}]
            }
            st.success(f"เพิ่ม {new_p_name} เรียบร้อย")
            st.rerun()
        elif len(st.session_state.projects_db) >= 10:
            st.warning("จำกัดสูงสุด 10 โปรเจกต์")

# --- 4. หน้าจอหลัก (Main Dashboard) ---
st.title("🚀 Engineering Control Panel")
st.markdown(f"**โครงการหลัก:** Snapcon Automation | วันที่ปัจจุบัน: {datetime.today().strftime('%d/%m/%Y')}")

# ส่วนที่ 1: Visual Gantt Chart
st.subheader("🗓 แผนผังภาพรวม (Gantt Chart)")
gantt_data = []
for p_name, p_val in st.session_state.projects_db.items():
    gantt_data.append({
        "Project": p_name,
        "Start": p_val['start_date'],
        "End": p_val['end_date'],
        "Status": "On-going"
    })

if gantt_data:
    df_gantt = pd.DataFrame(gantt_data)
    fig = px.timeline(df_gantt, x_start="Start", x_end="End", y="Project", color="Project", 
                     text="Project", template="plotly_white")
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ส่วนที่ 2: รายละเอียดโปรเจกต์และงานย่อย (10 Projects x 20 Tasks)
st.subheader("📑 รายละเอียดงานย่อยและสถานะ")

for p_name, p_val in st.session_state.projects_db.items():
    # คำนวณเปอร์เซ็นต์งานที่เสร็จ
    done_tasks = sum(1 for t in p_val['sub_tasks'] if t['done'])
    total_tasks = len(p_val['sub_tasks'])
    progress = done_tasks / total_tasks if total_tasks > 0 else 0
    
    with st.expander(f"📂 {p_name} | ความคืบหน้า: {progress:.0%}"):
        # ส่วนกำหนดวันที่ เริ่ม-จบ
        col_s, col_e, col_add = st.columns([1, 1, 1])
        p_val['start_date'] = col_s.date_input("เริ่มเมื่อ", p_val['start_date'], key=f"sd_{p_name}")
        p_val['end_date'] = col_e.date_input("จบเมื่อ", p_val['end_date'], key=f"ed_{p_name}")
        
        if col_add.button(f"➕ เพิ่มงานย่อย", key=f"btn_add_{p_name}"):
            if len(p_val['sub_tasks']) < 20:
                p_val['sub_tasks'].append({"name": "ระบุชื่องาน", "who": st.session_state.team_members[0], "done": False})
                st.rerun()
        
        st.progress(progress)
        
        # แสดงรายการงานย่อย
        for idx, task in enumerate(p_val['sub_tasks']):
            c1, c2, c3 = st.columns([0.1, 0.5, 0.4])
            task['done'] = c1.checkbox("", value=task['done'], key=f"chk_{p_name}_{idx}")
            
            # ถ้าติ๊กจบงาน ให้ตัวหนังสือเป็นสีจางหรือขีดฆ่า (ในหน้าจอหลัก)
            label = f"~~{task['name']}~~" if task['done'] else task['name']
            task['name'] = c2.text_input("ชื่องานย่อย", value=task['name'], key=f"txt_{p_name}_{idx}", label_visibility="collapsed")
            
            task['who'] = c3.selectbox("ใครทำ", st.session_state.team_members, 
                                      index=st.session_state.team_members.index(task['who']) if task['who'] in st.session_state.team_members else 0,
                                      key=f"sel_{p_name}_{idx}", label_visibility="collapsed")

st.divider()

# ส่วนที่ 3: สรุปภาระงานรายคน (Workload Analytics)
st.subheader("📊 ตารางวิเคราะห์โหลดงาน (รายบุคคล)")
load_stats = {name: 0 for name in st.session_state.team_members}
for p_val in st.session_state.projects_db.values():
    for t in p_val['sub_tasks']:
        if not t['done']: # นับเฉพาะงานที่ยังไม่เสร็จ
            load_stats[t['who']] += 1

df_load = pd.DataFrame(list(load_stats.items()), columns=['ชื่อพนักงาน', 'งานที่ค้าง (Tasks)'])
fig_load = px.bar(df_load, x='ชื่อพนักงาน', y='งานที่ค้าง (Tasks)', color='งานที่ค้าง (Tasks)', 
                 text_auto=True, color_continuous_scale="Reds")
st.plotly_chart(fig_load, use_container_width=True)
