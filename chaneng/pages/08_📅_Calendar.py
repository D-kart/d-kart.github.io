"""
Chaneng // CALENDAR
====================
财报日历 + 机构调研追踪
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.data_loader import get_earnings_calendar, get_institution_visits

st.set_page_config(page_title="CHANENG // CALENDAR", page_icon="📅", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ CALENDAR</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:1px; line-height:1.8;">'
                f'TRACKING<br>├─ 业绩预告<br>├─ 机构调研<br>└─ 投资者关系活动</div>', unsafe_allow_html=True)

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ EARNINGS CALENDAR</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">EARNINGS PREVIEWS · INSTITUTION VISITS</div>
    </div>
    <div>{breath_indicator('live')} <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:2px;">MONITORING</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# ==== 两列布局 ====
col_l, col_r = st.columns(2)

with col_l:
    st.markdown(section_title("EARNINGS PREVIEWS"), unsafe_allow_html=True)

    with st.spinner("> LOADING EARNINGS..."):
        earnings = get_earnings_calendar()

    if earnings:
        for ev in earnings:
            st.markdown(f"""
            <div class="pixel-card" style="padding:10px 14px; margin-bottom:6px;">
                <div style="display:flex; gap:10px; align-items:flex-start;">
                    <span style="font-size:9px; color:{PIXEL['accent']}; letter-spacing:1px; min-width:85px;">{ev['date']}</span>
                    <div>
                        <div style="font-size:12px; color:{PIXEL['text_primary']};">{ev['title'][:80]}</div>
                        {f'<div style="font-size:9px; color:{PIXEL["text_secondary"]}; margin-top:2px;">{ev["snippet"][:100]}</div>' if ev.get('snippet') else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:{PIXEL["text_dim"]}; font-size:11px; padding:12px;">> NO EARNINGS DATA</div>', unsafe_allow_html=True)

with col_r:
    st.markdown(section_title("INSTITUTION VISITS"), unsafe_allow_html=True)

    with st.spinner("> LOADING VISITS..."):
        visits = get_institution_visits()

    if visits:
        for v in visits:
            st.markdown(f"""
            <div class="pixel-card" style="padding:10px 14px; margin-bottom:6px;">
                <div style="display:flex; gap:10px; align-items:flex-start;">
                    <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:1px; min-width:85px;">{v['date']}</span>
                    <div>
                        <div style="font-size:12px; color:{PIXEL['text_primary']};">{v['title'][:80]}</div>
                        {f'<div style="font-size:9px; color:{PIXEL["text_secondary"]}; margin-top:2px;">{v["snippet"][:100]}</div>' if v.get('snippet') else ''}
                    </div>
                    {badge("VISIT", "positive")}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:{PIXEL["text_dim"]}; font-size:11px; padding:12px;">> NO VISIT DATA</div>', unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG CALENDAR · PUBLIC DISCLOSURES</div>', unsafe_allow_html=True)
