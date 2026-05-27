"""
Chaneng // COMPARE
===================
同业横比 · 输入2只票直接对比
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.data_loader import get_financial_snapshot, get_recent_events
from chaneng.mock_data import get_top_stocks

st.set_page_config(page_title="CHANENG // COMPARE", page_icon="🔗", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ COMPARE</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

    st.markdown(f'<div style="font-size:9px; color:{PIXEL["accent"]}; letter-spacing:2px; margin-bottom:4px;">STOCK A</div>', unsafe_allow_html=True)
    sym_a = st.text_input("CODE A", placeholder="600519", key="sym_a", label_visibility="collapsed")
    name_a = st.text_input("NAME A", placeholder="贵州茅台", key="name_a", label_visibility="collapsed")

    st.markdown(f'<div style="margin-top:12px; font-size:9px; color:{PIXEL["accent"]}; letter-spacing:2px; margin-bottom:4px;">STOCK B</div>', unsafe_allow_html=True)
    sym_b = st.text_input("CODE B", placeholder="000858", key="sym_b", label_visibility="collapsed")
    name_b = st.text_input("NAME B", placeholder="五粮液", key="name_b", label_visibility="collapsed")

    compare_btn = st.button("[ >> COMPARE << ]", use_container_width=True)

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ INDUSTRY COMPARE</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">HEAD-TO-HEAD FINANCIAL COMPARISON</div>
    </div>
    <div>{breath_indicator('idle')} <span style="font-size:9px; color:{PIXEL['text_secondary']}; letter-spacing:2px;">READY</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

if compare_btn and sym_a.strip() and sym_b.strip():
    with st.spinner(f"> COMPARING {sym_a} vs {sym_b}..."):
        snap_a = get_financial_snapshot(sym_a.strip(), name_a.strip())
        snap_b = get_financial_snapshot(sym_b.strip(), name_b.strip())

    m_a = snap_a.get("metrics", {})
    m_b = snap_b.get("metrics", {})
    label_a = name_a.strip() or sym_a.strip()
    label_b = name_b.strip() or sym_b.strip()

    # 对比指标表
    compare_metrics = [
        ("REVENUE", "revenue", "亿"),
        ("NET PROFIT", "net_profit", "亿"),
        ("GROSS MARGIN", "gross_margin", "%"),
        ("NET MARGIN", "net_margin", "%"),
        ("ROE", "roe", "%"),
        ("OPER PROFIT", "oper_profit", "亿"),
        ("PE(TTM)", "pe_ttm", "x"),
    ]

    st.markdown(f"""
    <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-bottom:16px;">
        <div></div>
        <div class="metric-block"><div class="metric-label">{label_a}</div></div>
        <div class="metric-block"><div class="metric-label">{label_b}</div></div>
    </div>
    """, unsafe_allow_html=True)

    for display_name, key, unit in compare_metrics:
        val_a = m_a.get(key, "--")
        val_b = m_b.get(key, "--")

        # 判断优劣
        better = ""
        if isinstance(val_a, (int, float)) and isinstance(val_b, (int, float)):
            if key in ("revenue", "net_profit", "gross_margin", "net_margin", "roe", "oper_profit"):
                better = "a" if val_a > val_b else "b" if val_b > val_a else ""
            elif key == "pe_ttm":
                better = "b" if 0 < val_a < val_b else "a" if 0 < val_b < val_a else ""

        a_str = f"{val_a}{unit}" if val_a != "--" else "--"
        b_str = f"{val_b}{unit}" if val_b != "--" else "--"
        a_style = f"color:{PIXEL['positive']};" if better == "a" else ""
        b_style = f"color:{PIXEL['positive']};" if better == "b" else ""

        cols = st.columns([1, 1, 1])
        with cols[0]:
            st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px; padding:8px;">{display_name}</div>', unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f'<div class="metric-block" style="padding:8px;"><div class="metric-value" style="font-size:16px; {a_style}">{a_str}</div></div>', unsafe_allow_html=True)
        with cols[2]:
            st.markdown(f'<div class="metric-block" style="padding:8px;"><div class="metric-value" style="font-size:16px; {b_style}">{b_str}</div></div>', unsafe_allow_html=True)

    # 结果判定
    a_wins = 0
    b_wins = 0
    for _, key, _ in compare_metrics:
        va, vb = m_a.get(key), m_b.get(key)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
            if key == "pe_ttm":
                if 0 < va < vb: b_wins += 1
                elif 0 < vb < va: a_wins += 1
            else:
                if va > vb: a_wins += 1
                elif vb > va: b_wins += 1

    st.markdown(hline(), unsafe_allow_html=True)
    verdict_color = PIXEL['positive'] if a_wins > b_wins else PIXEL['negative'] if b_wins > a_wins else PIXEL['warning']
    verdict = f"{label_a} 领先 {a_wins}-{b_wins}" if a_wins > b_wins else f"{label_b} 领先 {b_wins}-{a_wins}" if b_wins > a_wins else "旗鼓相当"
    st.markdown(f"""
    <div class="pixel-card" style="text-align:center;">
        <div style="font-size:10px; color:{PIXEL['text_secondary']}; letter-spacing:2px;">VERDICT</div>
        <div style="font-size:18px; color:{verdict_color}; font-weight:700; letter-spacing:2px; margin-top:4px;">{verdict}</div>
    </div>
    """, unsafe_allow_html=True)

elif compare_btn and (not sym_a.strip() or not sym_b.strip()):
    st.warning("> ENTER BOTH STOCK CODES")

if not compare_btn or not sym_a or not sym_b:
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:40px; color:{PIXEL['text_dim']};">◆</div>
        <div style="font-size:14px; color:{PIXEL['text_primary']}; letter-spacing:3px; margin-top:12px;">PICK TWO STOCKS</div>
        <div style="font-size:10px; color:{PIXEL['text_secondary']}; margin-top:4px; letter-spacing:2px;">
            ENTER CODES IN SIDEBAR → COMPARE
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG COMPARE ENGINE · FINANCIAL DATA</div>', unsafe_allow_html=True)
