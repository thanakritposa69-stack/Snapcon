import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import random
import io

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
        if random.random() > 0.6:
            st.session_state.prod_counts[i] += 1
            if random.random() > 0.95:
                st.session_state.health_scores[i] = max(0.0, st.session_state.health_scores[i] - 0.2)
    time.sleep(0.1)

# --- CSS Styling (Enhanced Consistency & Layout) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: #e6edf3; }}
    
    /* ปรับแต่งปุ่มคำสั่งให้เหมือนกัน (Uniform Design - White Transparent Style) */
    div.stButton > button {{
        width: 100% !important;
        border-radius: 6px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        background-color: rgba(255,255,255,0.05) !important;
        color: white !important;
        font-weight: 600 !important;
        height: 48px !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
    }}
    
    div.stButton > button:hover {{
        background-color: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }}

    /* สไตล์เฉพาะสำหรับสวิตช์ Toggle */
    .stCheckbox > label {{
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
    }}

    /* Card Metrics Layout */
    .metric-card {{
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #22d3ee;
    }}

    .status-badge {{
        background: rgba(22, 27, 34, 0.8);
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 8px 16px;
        display: inline-flex;
        align-items: center;
    }}

    .status-dot {{
        height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 10px;
        background-color: {"#10b981" if st.session_state.is_running else "#ef4444"};
        box-shadow: 0 0 12px {"#10b981" if st.session_state.is_running else "#ef4444"};
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
h_col1, h_col2 = st.columns([3, 1])
with h_col1:
    st.markdown(f"""
        <div style="display:flex; align-items:center;">
            <div style="background:#22d3ee; width:42px; height:42px; border-radius:8px; display:flex; align-items:center; justify-content:center; margin-right:15px; box-shadow: 0 0 15px rgba(34, 211, 238, 0.3);">
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

# --- DISPLAY AREA ---
if not show_adv:
    # Main Dashboard Metrics
    k1, k2, k3, k4 = st.columns(4)
    with k1: 
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_total"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p:,}</div><div style="color:#10b981;font-size:0.7rem;margin-top:4px;">↑ Units</div></div>', unsafe_allow_html=True)
    with k2:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_carbon"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p * 0.0072:.3f}</div><div style="color:#f87171;font-size:0.7rem;margin-top:4px;">↑ kgCO2e</div></div>', unsafe_allow_html=True)
    with k3:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_energy"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{total_p * 0.012:.2f}</div><div style="color:#f87171;font-size:0.7rem;margin-top:4px;">↑ kWh</div></div>', unsafe_allow_html=True)
    with k4:
        st.markdown(f'<div class="metric-card"><div style="color:#8b949e;font-size:0.75rem;margin-bottom:8px;">{L["kpi_health"]}</div><div style="font-size:2.2rem;font-weight:800;color:#e6edf3;">{avg_h:.1f}%</div><div style="color:#10b981;font-size:0.7rem;margin-top:4px;">System OK</div></div>', unsafe_allow_html=True)

    st.markdown("<br><div style='display:flex; align-items:center; gap:10px;'><span style='font-size:1.2rem;'>🌐</span><b style='color:#58a6ff;'>RS485 Topology - 10 Modules (Real-time)</b></div>", unsafe_allow_html=True)
    for r in range(2):
        row_cols = st.columns(5)
        for c in range(5):
            idx = (r * 5) + c
            health = st.session_state.health_scores[idx]
            h_color = "#10b981" if health > 90 else ("#f59e0b" if health > 70 else "#ef4444")
            with row_cols[c]:
                st.markdown(f"""
                <div style="background:#161b22; border:1px solid #30363d; border-radius:10px; padding:20px; text-align:center; margin-top:10px; transition: transform 0.2s;">
                    <div style="font-size:0.65rem; color:#8b949e; margin-bottom:10px; text-transform:uppercase; letter-spacing:1px;">Module #{idx+1:02d}</div>
                    <div style="font-size:1.8rem; font-weight:900; color:white; margin-bottom:5px;">{st.session_state.prod_counts[idx]}</div>
                    <div style="height:3px; width:30px; background:{h_color}; margin: 8px auto; border-radius:2px;"></div>
                    <div style="font-size:0.7rem; color:{h_color}; font-weight:600;">{health:.1f}% Health</div>
                </div>
                """, unsafe_allow_html=True)
else:
    # Advanced Report Section
    st.markdown("### 📊 Enterprise Analytics Report")
    
    # Generate CSV Data
    report_df = pd.DataFrame({
        "Module_ID": [f"MOD-{i+1:02d}" for i in range(10)],
        "Production_Count": st.session_state.prod_counts,
        "Health_Score_Percent": st.session_state.health_scores,
        "Energy_Consumption_kWh": [round(c * 0.012, 4) for c in st.session_state.prod_counts],
        "Carbon_Footprint_kgCO2e": [round(c * 0.0072, 4) for c in st.session_state.prod_counts],
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    
    csv = report_df.to_csv(index=False).encode('utf-8-sig')
    
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown("#### Export Section")
        st.download_button(
            label=f"📥 {L['csv_btn']}",
            data=csv,
            file_name=f"snapcon_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.info("💡 ข้อมูลถูกรวบรวมแบบ Real-time จากเกตเวย์ สามารถใช้ในการวิเคราะห์ประสิทธิภาพรายโมดูลได้")

    with col_b:
        st.markdown("#### Production Breakdown")
        fig = px.bar(report_df, x="Module_ID", y="Production_Count", color="Health_Score_Percent", 
                     color_continuous_scale="Viridis", title="Output Analysis by Hardware Node")
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# --- AUTO REFRESH ---
if st.session_state.is_running:
    time.sleep(0.4)
    st.rerun()
