import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import random
import io

# การตั้งค่าหน้ากระดาษ
st.set_page_config(
    page_title="Snapcon Control Center",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
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

# --- SIDEBAR: PARAMETER CONTROL ---
with st.sidebar:
    st.markdown(f"### ⚙️ System Configuration")
    st.divider()
    
    st.markdown("**Production Settings**")
    sim_speed = st.slider("Simulation Speed (Seconds)", 0.1, 2.0, 0.4, help="ความเร็วในการ Refresh หน้าจอ")
    prod_chance = st.slider("Production Rate (%)", 10, 100, 60, help="โอกาสที่จะเกิดผลผลิตในแต่ละรอบ") / 100
    
    st.divider()
    st.markdown("**Health & Maintenance**")
    degrade_chance = st.slider("Degradation Risk (%)", 0, 20, 5, help="โอกาสที่สุขภาพเครื่องจักรจะลดลง") / 100
    degrade_step = st.number_input("Health Drop per Unit", 0.01, 1.0, 0.2)
    
    st.divider()
    st.markdown("**Eco-Metrics Factor**")
    carbon_factor = st.number_input("Carbon Factor (kgCO2e/Unit)", 0.0001, 0.1, 0.0072, format="%.4f")
    energy_factor = st.number_input("Energy Factor (kWh/Unit)", 0.0001, 0.1, 0.0120, format="%.4f")
    
    st.divider()
    target_goal = st.number_input("Production Target (Units)", 100, 100000, 5000)

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
        'csv_btn': 'ดาวน์โหลดรายงาน CSV แบบละเอียด'
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
        'csv_btn': 'Download Detailed CSV Report'
    }
}

L = text[st.session_state.lang]

# --- SIMULATION LOGIC ---
if st.session_state.is_running:
    for i in range(num_modules):
        if random.random() < prod_chance:
            st.session_state.prod_counts[i] += 1
            if random.random() < degrade_chance:
                st.session_state.health_scores[i] = max(0.0, st.session_state.health_scores[i] - degrade_step)
    time.sleep(0.1)

# --- CSS Styling ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@500&display=swap');
    .stApp {{ background-color: #0d1117; color: #e6edf3; font-family: 'Inter', sans-serif; }}
    
    div.stButton > button {{
        width: 100% !important; border-radius: 8px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important; font-weight: 600 !important; height: 48px !important;
    }}
    div.stButton > button:hover {{ background-color: rgba(255,255,255,0.15) !important; }}

    .metric-card {{
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 1.5rem;
        position: relative; overflow: hidden;
    }}
    .metric-card::before {{ content: ""; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #22d3ee; }}

    .status-badge {{ background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 8px 16px; display: inline-flex; align-items: center; }}
    .status-dot {{ height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 10px; background-color: {"#10b981" if st.session_state.is_running else "#ef4444"}; }}

    .node-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 22px; text-align: center; margin-top: 10px; }}
    .node-number {{ font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: #ffffff; }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
h_col1, h_col2 = st.columns([3, 1])
with h_col1:
    st.markdown(f"""
        <div style="display:flex; align-items:center;">
            <div style="background:#22d3ee; width:42px; height:42px; border-radius:8px; display:flex; align-items:center; justify-content:center; margin-right:15px;">
                <span style="color:black; font-weight:900; font-size:1.3rem;">S</span>
            </div>
            <div>
                <h2 style="margin:0; letter-spacing:-1px; font-weight:800; color:white;">{L['title']}</h2>
                <p style="margin:0; color:#94a3b8; font-size:0.85rem;">{L['subtitle']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
with h_col2:
    st.markdown(f"""
        <div style="text-align:right;">
            <div class="status-badge">
                <span class="status-dot"></span>
                <span style="font-size:0.85rem; font-weight:600; color:#c9d1d9;">{L['running'] if st.session_state.is_running else L['idle']}</span>
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
progress = min(1.0, total_p / target_goal)

# --- PROGRESS BAR ---
st.markdown(f"<div style='color:#94a3b8; font-size:0.75rem; margin-bottom:5px;'>PRODUCTION TARGET PROGRESS: {total_p:,} / {target_goal:,}</div>", unsafe_allow_html=True)
st.progress(progress)

# --- DISPLAY AREA ---
if not show_adv:
    # Main Dashboard Metrics
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_total"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p:,}</div><div style="color:#10b981;font-size:0.7rem;margin-top:4px;">Units Generated</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_carbon"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p * carbon_factor:.3f}</div><div style="color:#94a3b8;font-size:0.7rem;margin-top:4px;">kgCO2e Total</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_energy"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p * energy_factor:.2f}</div><div style="color:#94a3b8;font-size:0.7rem;margin-top:4px;">kWh Accumulated</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_health"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{avg_h:.1f}%</div><div style="color:#10b981;font-size:0.7rem;margin-top:4px;">Healthy Status</div></div>', unsafe_allow_html=True)

    st.markdown("<br><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:1.2rem;'>🌐</span><b style='color:#58a6ff;'>Node Network Status</b></div>", unsafe_allow_html=True)
    for r in range(2):
        row_cols = st.columns(5)
        for c in range(5):
            idx = (r * 5) + c
            health = st.session_state.health_scores[idx]
            h_color = "#10b981" if health > 90 else ("#f59e0b" if health > 70 else "#ef4444")
            with row_cols[c]:
                st.markdown(f"""
                <div class="node-card">
                    <div style="font-size:0.65rem; color:#8b949e; margin-bottom:12px; text-transform:uppercase; letter-spacing:1.2px;">Node-{idx+1:02d}</div>
                    <div class="node-number">{st.session_state.prod_counts[idx]}</div>
                    <div style="height:3px; width:36px; background:{h_color}; margin: 12px auto; border-radius:2px;"></div>
                    <div style="font-size:0.75rem; color:{h_color}; font-weight:600;">{health:.1f}% OK</div>
                </div>
                """, unsafe_allow_html=True)
else:
    # Advanced Report Section
    st.markdown("### 📊 Advanced Analytics")
    report_df = pd.DataFrame({
        "Module_ID": [f"MOD-{i+1:02d}" for i in range(10)],
        "Production": st.session_state.prod_counts,
        "Health": st.session_state.health_scores,
        "Energy_kWh": [round(c * energy_factor, 4) for c in st.session_state.prod_counts],
        "Carbon_kg": [round(c * carbon_factor, 4) for c in st.session_state.prod_counts]
    })
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.dataframe(report_df, hide_index=True, use_container_width=True)
        csv = report_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(label=f"📥 {L['csv_btn']}", data=csv, file_name="snapcon_data.csv", mime="text/csv")

    with col_b:
        fig = px.bar(report_df, x="Module_ID", y="Production", color="Health", color_continuous_scale="RdYlGn")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# --- AUTO REFRESH ---
if st.session_state.is_running:
    time.sleep(sim_speed)
    st.rerun()
