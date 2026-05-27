"""
Chaneng // PIXEL TERMINAL PRO
==============================
Longbridge 风格融合 · 暗黑像素终端
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, market_tabs, ticker_strip,
                             index_card, compact_card, section_header, hline, badge, breath_dot, PIXEL)
from chaneng.mock_data import get_market_indices, get_top_stocks, get_sector_heatmap, get_recent_events, get_macro_indicators
import random, math

st.set_page_config(page_title="CHANENG // PRO", page_icon="◆", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

# ==== SIDEBAR ====
with st.sidebar:
    brand_header()
    st.markdown(f"""
    <div style="margin:12px 0; font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:1px; line-height:2;">
        {breath_dot(PIXEL['positive'])} SYSTEM ONLINE<br>
        <span style="color:{PIXEL['text_secondary']};">├─ MARKETS<br>├─ WATCHLIST<br>├─ AI CHAT<br>├─ COMPARE<br>└─ CALENDAR</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="margin-top:16px; font-size:9px; color:{PIXEL["accent"]}; letter-spacing:2px;">◆ QUICK NAV</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0;"></div>', unsafe_allow_html=True)

    nav_items = [
        ("📊 Dashboard", "Dashboard"),
        ("💬 AI Chat", "AI_Chat"),
        ("🔍 Search", "Search"),
        ("📈 Screener", "Screener"),
        ("📋 Stock", "Stock"),
        ("⭐ Watchlist", "Watchlist"),
        ("🔗 Compare", "Compare"),
        ("📅 Calendar", "Calendar"),
    ]
    for label, page in nav_items:
        st.markdown(f'<a href="/{page}" style="display:block; padding:4px 0; font-size:10px; color:{PIXEL["text_secondary"]}; text-decoration:none; letter-spacing:1px;">{label}</a>', unsafe_allow_html=True)

    st.markdown(f'<div style="margin-top:20px; font-size:8px; color:{PIXEL["text_dim"]};">v0.2.0 · PRIVATE BETA</div>', unsafe_allow_html=True)

# ==== MAIN ====
# 1. Market Tabs
st.markdown(market_tabs("OVERVIEW"), unsafe_allow_html=True)

# 2. Ticker Strip
indices = get_market_indices()
st.markdown(ticker_strip(indices), unsafe_allow_html=True)

# 3. 三列布局: 主要指数(2/3) | 侧边信息(1/3)
col_main, col_side = st.columns([2, 1])

with col_main:
    # 3.1 主要指数网格 (3x2)
    st.markdown(section_header("MAJOR INDICES", badge_text="LIVE"), unsafe_allow_html=True)

    idx_grid_cols = st.columns(3)
    for i, idx in enumerate(indices[:6]):
        with idx_grid_cols[i % 3]:
            # 生成伪 sparkline 数据
            spark_data = [math.sin(j * 0.5 + i) * random.uniform(0.5, 1.5) for j in range(30)]
            st.markdown(index_card(
                symbol=idx.symbol.split('.')[0] if '.' in idx.symbol else idx.symbol,
                name=idx.name,
                price=f"{idx.price:,.0f}",
                change=f"{idx.change_amt:+.0f}",
                pct=f"{idx.change_pct:+.2f}%",
                trend=idx.trend,
                sparkline_data=spark_data,
            ), unsafe_allow_html=True)

    st.markdown(hline(), unsafe_allow_html=True)

    # 3.2 热门标的 + 板块热力
    st.markdown(section_header("TOP MOVERS", "/Dashboard", "HOT"), unsafe_allow_html=True)

    stocks = get_top_stocks()
    mover_cols = st.columns(4)
    for i, s in enumerate(stocks[:8]):
        with mover_cols[i % 4]:
            trend = "positive" if s["change_pct"] >= 0 else "negative"
            clr = PIXEL['positive'] if trend == "positive" else PIXEL['negative']
            arrow = "▲" if trend == "positive" else "▼"
            st.markdown(f"""
            <div style="background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']}; padding:10px 12px; margin-bottom:6px;
                        cursor:pointer; transition:all 0.2s;"
                 onclick="window.location.href='/Stock?symbol={s["code"]}&name={s["name"]}&market={s["market"]}'"
                 onmouseover="this.style.borderColor='{PIXEL['accent']}';"
                 onmouseout="this.style.borderColor='{PIXEL['border']}';">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:11px; color:{PIXEL['text_primary']}; font-weight:600;">{s['name']}</div>
                        <div style="font-size:8px; color:{PIXEL['text_dim']}; letter-spacing:1px;">{s['code']} · PE{s['pe']:.1f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:13px; color:{PIXEL['text_primary']};">¥{s['price']:.1f}</div>
                        <div style="font-size:10px; color:{clr}; font-weight:600;">{arrow}{abs(s['change_pct']):.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col_side:
    # 3.3 研报/公告
    st.markdown(section_header("REPORTS", "/Search", "NEW"), unsafe_allow_html=True)
    events = get_recent_events()
    for ev in events[:4]:
        impact_badge = badge(
            {"positive": "BULL", "negative": "BEAR", "neutral": "--"}.get(ev['impact'], '--'),
            ev['impact']
        )
        st.markdown(f"""
        <div style="background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']}; padding:10px 12px; margin-bottom:6px;
                    transition:all 0.2s;" 
             onmouseover="this.style.borderColor='{PIXEL['accent']}';"
             onmouseout="this.style.borderColor='{PIXEL['border']}';">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="font-size:8px; color:{PIXEL['text_dim']}; letter-spacing:1px;">{ev['date']}</span>
                {impact_badge}
            </div>
            <div style="font-size:11px; color:{PIXEL['text_primary']}; line-height:1.5;">{ev['event'][:80]}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(hline(), unsafe_allow_html=True)

    # 3.4 宏观数据
    st.markdown(section_header("MACRO"), unsafe_allow_html=True)
    macros = get_macro_indicators()
    for m in macros[:6]:
        trend = m.get("trend", "neutral")
        chg = m.get("change", "")
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:5px 0; border-bottom:1px solid rgba(26,39,64,0.3); font-size:10px;">
            <span style="color:{PIXEL['text_dim']};">{m['label']}</span>
            <div>
                <span style="color:{PIXEL['text_primary']}; font-weight:500;">{m['value']}</span>
                {f'<span style="color:{PIXEL["positive"] if trend == "positive" else PIXEL["negative"] if trend == "negative" else PIXEL["text_dim"]}; font-size:9px; margin-left:6px;">{chg}</span>' if chg else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

# 4. 底部
st.markdown(hline(), unsafe_allow_html=True)

sectors = get_sector_heatmap()
hot = sorted(sectors, key=lambda x: x["change_pct"], reverse=True)[:5]
cold = sorted(sectors, key=lambda x: x["change_pct"])[:5]
st.markdown(section_header("SECTOR HEAT"), unsafe_allow_html=True)
scols = st.columns(10)
for i, s in enumerate(hot + cold):
    with scols[i]:
        clr = PIXEL['positive'] if s['change_pct'] >= 0 else PIXEL['negative']
        st.markdown(f"""
        <div style="text-align:center; padding:8px 4px; background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']};
                    transition:all 0.2s;"
             onmouseover="this.style.borderColor='{clr}';"
             onmouseout="this.style.borderColor='{PIXEL['border']}';">
            <div style="font-size:11px; color:{PIXEL['text_primary']};">{s['sector'][:4]}</div>
            <div style="font-size:12px; color:{clr}; font-weight:600; margin-top:2px;">{s['change_pct']:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f'<div style="text-align:center; padding:20px 0; font-size:8px; color:{PIXEL["text_dim"]}; letter-spacing:2px;">CHANENG PIXEL TERMINAL PRO © 2026 · DATA FOR REFERENCE</div>', unsafe_allow_html=True)
