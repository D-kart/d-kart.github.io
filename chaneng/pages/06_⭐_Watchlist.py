"""
Chaneng // WATCHLIST
====================
自选股池 · 像素终端
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.db import get_all_watch, add_watch, remove_watch, WatchItem
from chaneng.mock_data import get_top_stocks

st.set_page_config(page_title="CHANENG // WATCHLIST", page_icon="⭐", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ WATCHLIST</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

    # 添加自选
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["accent"]}; letter-spacing:2px; margin-bottom:6px;">[ + ADD ]</div>', unsafe_allow_html=True)
    new_symbol = st.text_input("CODE", placeholder="600519", key="add_code", label_visibility="collapsed")
    new_name = st.text_input("NAME", placeholder="贵州茅台", key="add_name", label_visibility="collapsed")
    new_market = st.selectbox("MKT", ["A-SHARE", "HK"], key="add_market", label_visibility="collapsed")

    if st.button("[ + ADD TO WATCH ]", use_container_width=True):
        if new_symbol.strip() and new_name.strip():
            item = WatchItem(symbol=new_symbol.strip(), name=new_name.strip(), market=new_market)
            ok = add_watch(item)
            if ok:
                st.success(f"> ADDED: {new_symbol}")
            else:
                st.warning(f"> ALREADY EXISTS: {new_symbol}")
            st.rerun()
        else:
            st.warning("> ENTER CODE AND NAME")

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ WATCHLIST</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">YOUR CURATED STOCK POOL</div>
    </div>
    <div>{breath_indicator('live')} <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:2px;">TRACKING</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# ==== DATA ====
watched = get_all_watch()
mock_prices = {s["code"]: s for s in get_top_stocks()}

if watched:
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px; margin:8px 0;">◆ {len(watched)} STOCKS TRACKED</div>', unsafe_allow_html=True)

    rows = []
    for w in watched:
        # 尝试匹配模拟价格
        price_info = mock_prices.get(w.symbol)
        if price_info:
            price_str = f"¥{price_info['price']:.2f}"
            chg = price_info['change_pct']
            chg_str = f"{chg:+.2f}%"
            trend = "positive" if chg >= 0 else "negative"
            chg_color = PIXEL['positive'] if trend == "positive" else PIXEL['negative']
        else:
            price_str = "--"
            chg_str = "--"
            chg_color = PIXEL['text_dim']
            trend = "neutral"

        mkt_badge = badge(w.market, "accent" if w.market == "A-SHARE" else "positive")

        rows.append(f"""
        <tr>
            <td style="font-size:10px; color:{PIXEL['text_dim']};">{w.symbol}</td>
            <td style="font-weight:600; font-size:12px;">
                <a href="/Stock?symbol={w.symbol}&name={w.name}&market={w.market}" style="text-decoration:none;">
                    {w.name}
                </a>
            </td>
            <td>{mkt_badge}</td>
            <td style="font-size:12px;">{price_str}</td>
            <td style="color:{chg_color}; font-size:11px; font-weight:600;">{chg_str}</td>
            <td style="font-size:9px; color:{PIXEL['text_dim']};">{w.added_at[:10]}</td>
            <td>
                <form method="post" style="display:inline;">
                    <button type="submit" name="remove_{w.symbol}_{w.market}"
                     style="background:none; border:1px solid {PIXEL['negative']}; color:{PIXEL['negative']};
                            font-size:9px; padding:2px 8px; cursor:pointer; letter-spacing:1px;">
                    [ X ]</button>
                </form>
            </td>
        </tr>
        """)

    st.markdown(f"""
    <table class="pixel-table">
        <thead><tr>
            <th>CODE</th><th>NAME</th><th>MKT</th><th>PRICE</th><th>CHG%</th><th>SINCE</th><th></th>
        </tr></thead>
        <tbody>{''.join(rows)}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # 移除逻辑 — 通过 URL 参数处理
    st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
    # 使用列布局的按钮代替 form
    remove_cols = st.columns([1] * len(watched)) if len(watched) <= 6 else st.columns(6)
    for i, (col, w) in enumerate(zip(remove_cols, watched)):
        if i >= 6:
            break
        with col:
            if st.button(f"[DEL] {w.symbol}", key=f"del_{w.symbol}_{w.market}", use_container_width=True):
                remove_watch(w.symbol, w.market)
                st.rerun()

else:
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:40px; color:{PIXEL['text_dim']};">◆</div>
        <div style="font-size:14px; color:{PIXEL['text_primary']}; letter-spacing:3px; margin-top:12px;">NO STOCKS YET</div>
        <div style="font-size:10px; color:{PIXEL['text_secondary']}; margin-top:4px; letter-spacing:2px;">
            ADD YOUR FIRST STOCK IN THE SIDEBAR →
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG WATCHLIST · PRIVATE POOL</div>', unsafe_allow_html=True)
