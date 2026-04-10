import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import random

# การตั้งค่าหน้ากระดาษ
st.set_page_config(
    page_title="Snapcon",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SESSION STATE ---
num_modules = 10
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'prod_counts' not in st.session_state:
    st.session_state.prod_counts = [0] * num_modules
if 'health_scores' not in st.session_state:
    st.session_state.health_scores = [100.0] * num_modules
if 'lang' not in st.session_state:
    st.session_state.lang = 'TH'

# --- CONFIGURATION (INPUTS) ---
# ค่าเหล่านี้สามารถปรับแต่งได้จาก Sidebar เพื่อเปลี่ยน Output
if 'config' not in st.session_state:
    st.session_state.config = {
        'carbon_factor': 0.0072,  # kgCO2e per unit
        'energy_factor': 0.0120,  # kWh per unit
        'health_decay': 0.05,     # Speed of health reduction
        'currency_symbol': '฿'
    }

# ข้อมูลข้อความ
text = {
    'TH': {
        'title': 'SNAPCON',
        'subtitle': 'ระบบควบคุมและติดตามผลการผลิตอัจฉริยะ',
        'status_label': 'สถานะการเชื่อมต่อ',
        'running': 'กำลังทำงาน (Online)',
        'idle': 'หยุดการทำงาน (Offline)',
        'start': 'START SYSTEM',
        'stop': 'STOP SYSTEM',
        'reset': 'RESET ALL',
        'report_toggle': 'ADVANCED REPORT',
        'kpi_total': 'ยอดรวมการผลิต',
        'kpi_carbon': 'คาร์บอนฟุตพริ้นท์',
        'kpi_energy': 'พลังงานที่ใช้',
        'kpi_health': 'สุขภาพระบบเฉลี่ย',
        'csv_btn': 'ดาวน์โหลดรายงาน CSV แบบละเอียด',
        'settings': 'ตั้งค่าระบบ (Inputs)'
    },
    'EN': {
        'title': 'SNAPCON',
        'subtitle': 'Smart Production Monitoring & Control',
        'status_label': 'CONNECTION STATUS',
        'running': 'RUNNING (Online)',
        'idle': 'IDLE (Offline)',
        'start': 'START SYSTEM',
        'stop': 'STOP SYSTEM',
        'reset': 'RESET ALL',
        'report_toggle': 'ADVANCED REPORT',
        'kpi_total': 'Total Production',
        'kpi_carbon': 'Carbon Footprint',
        'kpi_energy': 'Energy Usage',
        'kpi_health': 'Avg. Health',
        'csv_btn': 'Download Detailed CSV Report',
        'settings': 'System Settings (Inputs)'
    }
}

L = text[st.session_state.lang]

# --- SIMULATION LOGIC ---
if st.session_state.is_running:
    for i in range(num_modules):
        if random.random() > 0.6:
            st.session_state.prod_counts[i] += 1
            if random.random() > 0.95:
                decay = st.session_state.config['health_decay']
                st.session_state.health_scores[i] = max(0.0, st.session_state.health_scores[i] - decay)
    time.sleep(0.1)

# --- CSS Styling ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: #e6edf3; }}
    
    /* ปุ่มคำสั่งทั้งหมดให้เหมือนกัน (Uniform Design) */
    div.stButton > button {{
        width: 100% !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        font-weight: 600 !important;
        height: 48px !important;
        transition: all 0.3s ease !important;
    }}
    
    div.stButton > button:hover {{
        background-color: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(34, 211, 238, 0.5) !important;
    }}

    .metric-card {{
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
    }}
    
    .status-badge {{
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 8px 16px;
    }}

    .status-dot {{
        height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 10px;
        background-color: {"#10b981" if st.session_state.is_running else "#ef4444"};
        box-shadow: 0 0 12px {"#10b981" if st.session_state.is_running else "#ef4444"};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (INPUT EDITING) ---
with st.sidebar:
    st.header(f"⚙️ {L['settings']}")
    st.session_state.config['carbon_factor'] = st.number_input("Carbon Factor (kg/unit)", value=st.session_state.config['carbon_factor'], format="%.4f")
    st.session_state.config['energy_factor'] = st.number_input("Energy Factor (kWh/unit)", value=st.session_state.config['energy_factor'], format="%.4f")
    st.session_state.config['health_decay'] = st.slider("Maintenance Sensitivity", 0.01, 1.0, st.session_state.config['health_decay'])
    st.markdown("---")
    st.caption("การปรับค่าในหน้านี้จะส่งผลต่อการคำนวณ Output บน Dashboard ทันที")

# --- HEADER SECTION ---
h_col1, h_col2 = st.columns([3, 1])
with h_col1:
    st.markdown(f"""
        <div style="display:flex; align-items:center;">
            <div style="background:#22d3ee; width:42px; height:42px; border-radius:8px; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <span style="color:black; font-weight:900; font-size:1.3rem;">S</span>
            </div>
            <div>
                <h2 style="margin:0; font-weight:800; color:white;">{L['title']}</h2>
                <p style="margin:0; color:#94a3b8; font-size:0.85rem;">{L['subtitle']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with h_col2:
    st.markdown(f"""
        <div style="text-align:right;">
            <div class="status-badge">
                <span class="status-dot"></span>
                <span style="font-size:0.85rem; font-weight:600;">{L['running'] if st.session_state.is_running else L['idle']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin: 15px 0; border-bottom: 1px solid #30363d;'></div>", unsafe_allow_html=True)

# --- CONTROL AREA ---
c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1.2, 0.6])
with c1:
    if st.button(f"▶ {L['start']}", key="btn_start"):
        st.session_state.is_running = True
        st.rerun()
with c2:
    if st.button(f"⏹ {L['stop']}", key="btn_stop"):
        st.session_state.is_running = False
        st.rerun()
with c3:
    if st.button(f"🔄 {L['reset']}", key="btn_reset"):
        st.session_state.prod_counts = [0] * num_modules
        st.session_state.health_scores = [100.0] * num_modules
        st.rerun()
with c4:
    st.markdown("<div style='padding-top:10px;'></div>", unsafe_allow_html=True)
    show_adv = st.toggle(f"📊 {L['report_toggle']}", value=False)
with c5:
    if st.button(st.session_state.lang, key="btn_lang"):
        st.session_state.lang = 'EN' if st.session_state.lang == 'TH' else 'TH'
        st.rerun()

# --- KPI CALCULATION ---
total_p = sum(st.session_state.prod_counts)
avg_h = sum(st.session_state.health_scores) / num_modules
total_carbon = total_p * st.session_state.config['carbon_factor']
total_energy = total_p * st.session_state.config['energy_factor']

# --- DISPLAY AREA ---
if not show_adv:
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;">{L["kpi_total"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p:,}</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;">{L["kpi_carbon"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_carbon:.2f}</div><div style="color:#f87171;font-size:0.7rem;">kgCO2e</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;">{L["kpi_energy"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_energy:.2f}</div><div style="color:#f87171;font-size:0.7rem;">kWh</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;">{L["kpi_health"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{avg_h:.1f}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br><b style='color:#58a6ff;'>🌐 Hardware Nodes Status</b>", unsafe_allow_html=True)
    for r in range(2):
        row_cols = st.columns(5)
        for c in range(5):
            idx = (r * 5) + c
            health = st.session_state.health_scores[idx]
            h_color = "#10b981" if health > 90 else ("#f59e0b" if health > 70 else "#ef4444")
            with row_cols[c]:
                st.markdown(f"""
                <div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:20px; text-align:center; margin-top:10px;">
                    <div style="font-size:0.65rem; color:#8b949e;">Module #{idx+1:02d}</div>
                    <div style="font-size:1.8rem; font-weight:900; color:white;">{st.session_state.prod_counts[idx]}</div>
                    <div style="font-size:0.7rem; color:{h_color};">● {health:.1f}%</div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.markdown("### 📊 Enterprise Analytics Report")
    report_df = pd.DataFrame({
        "Module_ID": [f"MOD-{i+1:02d}" for i in range(10)],
        "Production": st.session_state.prod_counts,
        "Health_%": st.session_state.health_scores,
        "Energy_kWh": [round(c * st.session_state.config['energy_factor'], 4) for c in st.session_state.prod_counts],
        "Timestamp": datetime.now().strftime("%H:%M:%S")
    })
    
    st.dataframe(report_df, use_container_width=True)
    csv = report_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(f"📥 {L['csv_btn']}", data=csv, file_name="report.csv", mime="text/csv")

# --- AUTO REFRESH ---
if st.session_state.is_running:
    time.sleep(0.4)
    st.rerun()
