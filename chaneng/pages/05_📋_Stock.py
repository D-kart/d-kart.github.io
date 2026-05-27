"""
Chaneng // STOCK
================
个股深度页 · 财报 / 事件 / 产业链一站看
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.data_loader import get_financial_snapshot, get_recent_events
from chaneng.db import is_watched, add_watch, remove_watch, WatchItem
from chaneng.mock_data import get_top_stocks

st.set_page_config(page_title="CHANENG // STOCK", page_icon="📋", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

# ==== 获取参数 ====
params = st.query_params
symbol = params.get("symbol", "")
name = params.get("name", "")
market = params.get("market", "A-SHARE")

# 如果从 URL 没拿到，就用输入框
if not symbol:
    symbol_input = st.text_input("STOCK CODE", placeholder="600519", label_visibility="collapsed")
    if symbol_input:
        symbol = symbol_input.strip()

# ==== 加载数据 ====
if symbol:
    with st.spinner(f"> LOADING {symbol}..."):
        snap = get_financial_snapshot(symbol, name)
        events = get_recent_events(symbol, name, limit=8)
        watched = is_watched(symbol, market)

    # 模拟价格
    mock_prices = {s["code"]: s for s in get_top_stocks()}
    price_info = mock_prices.get(symbol)

    # ==== 侧边栏 ====
    with st.sidebar:
        brand_header()
        st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ STOCK TOOLS</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

        # 自选按钮
        if watched:
            st.markdown(f'<span style="color:{PIXEL["positive"]}; font-size:10px;">{breath_indicator("live")} IN WATCHLIST</span>', unsafe_allow_html=True)
            if st.button("[ - REMOVE FROM WATCH ]", use_container_width=True):
                remove_watch(symbol, market)
                st.rerun()
        else:
            st.markdown(f'<span style="color:{PIXEL["text_dim"]}; font-size:10px;">◆ NOT IN WATCHLIST</span>', unsafe_allow_html=True)
            if st.button("[ + ADD TO WATCH ]", use_container_width=True):
                add_watch(WatchItem(symbol=symbol, name=name or symbol, market=market))
                st.rerun()

        st.markdown(f'<div style="margin-top:16px; font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:1px;">'
                    f'QUICK NAV<br>├─ Dashboard<br>├─ Compare<br>└─ Calendar</div>', unsafe_allow_html=True)

    # ==== 头部 ====
    price_str = f"¥{price_info['price']:.2f}" if price_info else "--"
    chg = price_info['change_pct'] if price_info else 0
    chg_str = f"{chg:+.2f}%" if price_info else "--"
    trend = "positive" if chg >= 0 else "negative"
    pe_str = f"PE {price_info['pe']:.1f}x" if price_info else ""

    st.markdown(f"""
    <div class="pixel-card" style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                    <span style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px;">{symbol}</span>
                    {badge(market, 'accent')}
                    {f'<span style="font-size:10px; color:{PIXEL["positive"]};">{breath_indicator("live")}WATCHED</span>' if watched else ''}
                </div>
                <div style="font-size:22px; color:{PIXEL['text_primary']}; font-weight:700; letter-spacing:3px;">
                    {name or symbol}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:24px; color:{PIXEL['text_primary']}; font-weight:700; letter-spacing:2px;">{price_str}</div>
                <div style="font-size:14px; color:{PIXEL['positive'] if trend == 'positive' else PIXEL['negative']}; letter-spacing:1px;">
                    {chg_str}
                </div>
                {f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; margin-top:2px;">{pe_str}</div>' if pe_str else ''}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ==== 财报速览 ====
    st.markdown(section_title("FINANCIAL SNAPSHOT"), unsafe_allow_html=True)

    metrics = snap.get("metrics", {})
    if metrics:
        # 指标卡片
        metric_items = [
            ("REVENUE", metrics.get("revenue"), "亿"),
            ("NET PROFIT", metrics.get("net_profit"), "亿"),
            ("GROSS MARGIN", metrics.get("gross_margin"), "%"),
            ("NET MARGIN", metrics.get("net_margin"), "%"),
            ("ROE", metrics.get("roe"), "%"),
            ("OPER PROFIT", metrics.get("oper_profit"), "亿"),
        ]
        cols = st.columns(6)
        for col, (label, val, unit) in zip(cols, metric_items):
            display = f"{val}{unit}" if val and unit != "%" else f"{val}%" if val and unit == "%" else "--"
            with col:
                st.markdown(f"""
                <div class="metric-block">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value" style="font-size:18px;">{display}</div>
                </div>
                """, unsafe_allow_html=True)

        # 原始数据表（折叠）
        with st.expander("> RAW FINANCIAL DATA"):
            st.markdown(f"```\n{snap.get('raw', 'NO DATA')[:2000]}\n```")
    else:
        st.markdown(f'<div style="color:{PIXEL["text_dim"]}; font-size:11px; padding:12px;">> NO FINANCIAL DATA AVAILABLE</div>', unsafe_allow_html=True)

    st.markdown(hline(), unsafe_allow_html=True)

    # ==== 事件时间线 ====
    st.markdown(section_title("EVENT TIMELINE"), unsafe_allow_html=True)

    if events:
        for ev in events:
            st.markdown(f"""
            <div class="pixel-card" style="padding:10px 14px; margin-bottom:6px;">
                <div style="display:flex; gap:12px; align-items:flex-start;">
                    <span style="font-size:9px; color:{PIXEL['accent']}; letter-spacing:1px; white-space:nowrap; min-width:80px;">{ev['date']}</span>
                    <div>
                        <div style="font-size:12px; color:{PIXEL['text_primary']}; font-weight:500;">{ev['title']}</div>
                        {f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; margin-top:3px;">{ev["snippet"]}</div>' if ev.get('snippet') else ''}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="color:{PIXEL["text_dim"]}; font-size:11px; padding:12px;">> NO RECENT EVENTS</div>', unsafe_allow_html=True)

    st.markdown(hline(), unsafe_allow_html=True)

    # ==== AI 分析入口 ====
    st.markdown(section_title("AI ANALYSIS"), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="pixel-card" style="text-align:center; padding:20px;">
        <div style="font-size:11px; color:{PIXEL['text_secondary']}; letter-spacing:2px; margin-bottom:12px;">
            GENERATE AI BRIEF · INDUSTRY COMPARE · DEEP DIVE
        </div>
        <a href="/AI_Chat" style="text-decoration:none;">
            <span style="color:{PIXEL['accent']}; font-size:12px; letter-spacing:2px; border:1px solid {PIXEL['accent']}; padding:8px 24px;">
                [ OPEN AI CHAT → ]
            </span>
        </a>
    </div>
    """, unsafe_allow_html=True)

else:
    # 空状态
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:48px; color:{PIXEL['text_dim']};">◆</div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; margin-top:12px;">ENTER STOCK CODE</div>
        <div style="font-size:10px; color:{PIXEL['text_secondary']}; margin-top:4px; letter-spacing:2px;">
            E.G. 600519 · 300750 · 00700
        </div>
        <div style="margin-top:20px; font-size:10px; color:{PIXEL['text_dim']}; letter-spacing:1px;">
            OR SELECT FROM <a href="/Watchlist">WATCHLIST</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG STOCK TERMINAL · DATA FOR REFERENCE</div>', unsafe_allow_html=True)
