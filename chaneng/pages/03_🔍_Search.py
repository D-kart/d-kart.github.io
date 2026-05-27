"""
Chaneng // SEARCH
=================
多源数据搜索 · 像素终端
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.api import get_client, ChanengAPIError, ChanengQuotaExceeded, VALID_SOURCES, SOURCE_LABELS

st.set_page_config(page_title="CHANENG // SEARCH", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ FILTERS</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

    source_icons = {"web": "WEB", "academic": "ACAD", "image": "IMG", "video": "VID", "announcement": "ANN"}
    source_filter = st.multiselect(
        "SOURCES",
        VALID_SOURCES,
        default=["announcement", "web"],
        format_func=lambda x: f"[{source_icons.get(x,x)}] {SOURCE_LABELS.get(x,x)}",
        label_visibility="collapsed",
    )
    search_mode = st.radio("MODE", ["advanced", "fast", "expert"], index=0,
                           format_func=lambda x: x.upper(), horizontal=True, label_visibility="collapsed")
    time_presets = {"1W": "past 1 week", "1M": "past 1 month", "3M": "past 3 months",
                    "6M": "past 6 months", "1Y": "past 1 year"}
    time_choice = st.selectbox("TIMEFRAME", list(time_presets.keys()), index=2,
                               format_func=lambda x: f"[{x}]", label_visibility="collapsed")
    time_range = time_presets[time_choice]
    count = st.slider("LIMIT", 5, 50, 15, step=5, label_visibility="collapsed")

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ DATA SEARCH</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">MULTI-SOURCE · SEMANTIC SEARCH</div>
    </div>
    <div>{breath_indicator('live')} <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:2px;">READY</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

query = st.text_input("", placeholder="> ENTER KEYWORDS...  E.G. 'AI COMPUTE' 'SOLAR POLICY' 'CATL'", label_visibility="collapsed")

# 快捷语义筛选
quick_tags = ["减持", "增持", "业绩预告", "重大合同", "分红", "回购", "股权激励", "重组"]
st.markdown(f'<div style="font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:2px; margin:4px 0;">◆ QUICK FILTERS (CLICK TO SEARCH)</div>', unsafe_allow_html=True)
tag_cols = st.columns(len(quick_tags))
active_tag = None
for col, tag in zip(tag_cols, quick_tags):
    with col:
        if st.button(f"[{tag}]", key=f"qt_{tag}", use_container_width=True):
            active_tag = tag
if active_tag:
    query = st.text_input("", value=active_tag, placeholder="> ENTER KEYWORDS...", label_visibility="collapsed")

col_btn1, _ = st.columns([1, 5])
with col_btn1:
    search_btn = st.button("[ SEARCH ]", use_container_width=True)

if search_btn and query and query.strip():
    if not source_filter:
        st.warning("> SELECT AT LEAST ONE SOURCE")
    else:
        with st.spinner(f"> SEARCHING: {query}..."):
            try:
                client = get_client()
                all_items = []

                for src in source_filter:
                    resp = client.search(query.strip(), source=src, search_mode=search_mode, count=count, time_range=time_range)
                    if resp.items:
                        for item in resp.items:
                            item.source_tag = src
                        all_items.extend(resp.items)

                if all_items:
                    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px; margin:10px 0;">◆ {len(all_items)} RESULTS FOUND</div>', unsafe_allow_html=True)

                    for i, r in enumerate(all_items):
                        src_tag = getattr(r, 'source_tag', '')
                        src_label = SOURCE_LABELS.get(src_tag, src_tag).upper()
                        src_cls = {"announcement": "positive", "web": "accent", "academic": "positive",
                                   "image": "accent", "video": "accent"}.get(src_tag, "accent")
                        st.markdown(f"""
                        <div class="pixel-card">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                                <div style="font-size:13px; color:{PIXEL['text_primary']}; font-weight:600; flex:1;">{r.title}</div>
                                <div style="display:flex; gap:8px; flex-shrink:0; margin-left:12px;">
                                    {badge(src_label, src_cls)}
                                    {f'<span style="font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:1px;">{r.date}</span>' if r.date else ''}
                                </div>
                            </div>
                            {f'<div style="font-size:11px; color:{PIXEL["text_secondary"]}; line-height:1.6;">{r.snippet[:280]}{"..." if len(r.snippet) > 280 else ""}</div>' if r.snippet else ''}
                            {f'<a href="{r.link}" target="_blank" style="font-size:10px; letter-spacing:1px; display:inline-block; margin-top:6px;">[ OPEN LINK → ]</a>' if r.link else ''}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("> NO RESULTS. ADJUST KEYWORDS OR FILTERS.")

            except ChanengQuotaExceeded:
                st.error("> // ERROR: QUOTA EXCEEDED")
            except ChanengAPIError as e:
                st.error(f"> // ERROR: {str(e)[:150]}")

elif search_btn and (not query or not query.strip()):
    st.warning("> ENTER KEYWORDS TO SEARCH")

if not search_btn or not query:
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:40px; margin-bottom:12px; color:{PIXEL['text_dim']};">◆</div>
        <div style="font-size:14px; color:{PIXEL['text_primary']}; letter-spacing:3px;">ENTER KEYWORDS</div>
        <div style="font-size:10px; color:{PIXEL['text_secondary']}; margin-top:4px; letter-spacing:2px;">ANN · WEB · ACAD · IMG · VID</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG SEARCH ENGINE · PUBLIC SOURCES</div>', unsafe_allow_html=True)
