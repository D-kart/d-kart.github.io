"""
Chaneng // SCREENER
===================
标的筛选器 · 像素终端
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from chaneng.styles import (inject_pixel_theme, brand_header, section_title, hline, badge, breath_indicator, PIXEL)
from chaneng.mock_data import get_top_stocks

st.set_page_config(page_title="CHANENG // SCREENER", page_icon="📈", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ FILTERS</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

    market_filter = st.multiselect("MARKET", ["A-SHARE", "HK"], default=["A-SHARE", "HK"], label_visibility="collapsed")
    pe_min = st.number_input("PE MIN", value=0, step=1, label_visibility="collapsed")
    pe_max = st.number_input("PE MAX", value=100, step=1, label_visibility="collapsed")
    price_min = st.number_input("PRICE MIN", value=0.0, step=1.0, label_visibility="collapsed")
    price_max = st.number_input("PRICE MAX", value=5000.0, step=10.0, label_visibility="collapsed")
    search_name = st.text_input("SEARCH", placeholder="NAME OR CODE...", label_visibility="collapsed")

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ STOCK SCREENER</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">A-SHARE + HK · MULTI-DIMENSION FILTER</div>
    </div>
    <div>{breath_indicator('idle')} <span style="font-size:9px; color:{PIXEL['text_secondary']}; letter-spacing:2px;">SIMULATED</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# Data & Filter
stocks = get_top_stocks()
df = pd.DataFrame(stocks)
df['market'] = df['market'].replace({"A股": "A-SHARE", "港股": "HK"})

if market_filter:
    df = df[df['market'].isin(market_filter)]
if pe_min > 0:
    df = df[df['pe'] >= pe_min]
if pe_max < 100:
    df = df[df['pe'] <= pe_max]
if price_min > 0:
    df = df[df['price'] >= price_min]
if price_max < 5000:
    df = df[df['price'] <= price_max]
if search_name:
    df = df[df['name'].str.contains(search_name, case=False) | df['code'].str.contains(search_name)]

if not df.empty:
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px; margin:8px 0;">◆ {len(df)} RESULTS</div>', unsafe_allow_html=True)

    # Scatter plot
    fig = go.Figure()
    for _, row in df.iterrows():
        color = PIXEL['positive'] if row['trend'] == 'positive' else PIXEL['negative']
        fig.add_trace(go.Scatter(
            x=[row['pe']], y=[row['price']],
            mode='markers+text',
            marker=dict(size=abs(row['change_pct']) * 6 + 12, color=color, opacity=0.85,
                        line=dict(color=PIXEL['border'], width=1)),
            text=row['name'], textposition='top center',
            textfont=dict(color=PIXEL['text_primary'], size=10, family="JetBrains Mono"),
            name=row['name'],
            hovertemplate=f"<b>{row['name']}</b><br>PE: {row['pe']}<br>PRICE: ¥{row['price']}<br>CHG: {row['change_pct']:+.2f}%<extra></extra>",
        ))
    fig.update_layout(
        height=360, xaxis_title="PE (TTM)", yaxis_title="PRICE (¥)",
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=True, gridcolor=PIXEL['border'], zeroline=False,
                   tickfont=dict(color=PIXEL['text_dim'], family="JetBrains Mono")),
        yaxis=dict(showgrid=True, gridcolor=PIXEL['border'], zeroline=False,
                   tickfont=dict(color=PIXEL['text_dim'], family="JetBrains Mono")),
        showlegend=False, margin=dict(l=50, r=20, t=10, b=40),
        font=dict(family="JetBrains Mono"),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(hline(), unsafe_allow_html=True)

    # Table
    html_rows = []
    for _, row in df.iterrows():
        clr = PIXEL['positive'] if row['trend'] == 'positive' else PIXEL['negative']
        html_rows.append(f"""
        <tr>
            <td style="font-size:10px; color:{PIXEL['text_dim']};">{row['code']}</td>
            <td style="font-weight:600;">{row['name']}</td>
            <td>{badge(row['market'], 'accent')}</td>
            <td>¥{row['price']:.2f}</td>
            <td style="color:{clr}; font-weight:600;">{row['change_pct']:+.2f}%</td>
            <td>{row['pe']:.1f}x</td>
        </tr>
        """)

    st.markdown(f"""
    <table class="pixel-table">
        <thead><tr>
            <th>CODE</th><th>NAME</th><th>MKT</th><th>PRICE</th><th>CHG%</th><th>PE</th>
        </tr></thead>
        <tbody>{''.join(html_rows)}</tbody>
    </table>
    """, unsafe_allow_html=True)

else:
    st.markdown(f"""
    <div style="text-align:center; padding:60px 20px;">
        <div style="font-size:40px; color:{PIXEL['text_dim']};">◆</div>
        <div style="font-size:12px; color:{PIXEL['text_secondary']}; margin-top:8px; letter-spacing:2px;">NO RESULTS</div>
        <div style="font-size:10px; color:{PIXEL['text_dim']}; margin-top:4px;">ADJUST FILTERS</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG SCREENER · SIMULATED DATA · DEMO ONLY</div>', unsafe_allow_html=True)
