"""
Chaneng // DASHBOARD
====================
宏观仪表盘 · 像素风暗黑终端
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from chaneng.styles import (inject_pixel_theme, brand_header, section_title,
                             metric_block, hline, badge, breath_indicator, PIXEL)
from chaneng.mock_data import (get_market_indices, get_macro_indicators,
                                get_sector_heatmap, get_top_stocks, get_recent_events)

st.set_page_config(page_title="CHANENG // DASHBOARD", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_dim"]}; letter-spacing:2px; margin-bottom:8px;">◆ NAVIGATION</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:1px;">{breath_indicator("live")} DASHBOARD ACTIVE</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="margin-top:16px; font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:1px; line-height:1.8;">'
                f'DATA SOURCE<br>├─ MOCK MARKET DATA<br>└─ CHANENG ENGINE</div>', unsafe_allow_html=True)

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ MARKET OVERVIEW</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">A-SHARE + HK MARKET · SIMULATED DATA</div>
    </div>
    <div>{breath_indicator('live')} <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:2px;">LIVE</span></div>
</div>
""", unsafe_allow_html=True)

# ==== INDEX CARDS ====
indices = get_market_indices()
cols = st.columns(6)
for i, (col, idx) in enumerate(zip(cols, indices)):
    with col:
        arrow = "+" if idx.trend == "positive" else ""
        trend = "positive" if idx.change_pct >= 0 else "negative"
        change_str = f"{arrow}{idx.change_pct:+.2f}%  {arrow}{idx.change_amt:+.2f}" if idx.change_amt != 0 else f"{arrow}{idx.change_pct:+.2f}%"
        st.markdown(metric_block(
            label=idx.name.upper(),
            value=f"{idx.price:,.0f}",
            change=change_str,
            trend=trend,
        ), unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# ==== MACRO + HEATMAP ====
col_l, col_r = st.columns([1, 2])

with col_l:
    st.markdown(section_title("MACRO INDICATORS"), unsafe_allow_html=True)
    macros = get_macro_indicators()
    for m in macros:
        border_clr = PIXEL['positive'] if m['trend'] == 'positive' else PIXEL['negative'] if m['trend'] == 'negative' else PIXEL['border']
        chg_clr = PIXEL['positive'] if m['trend'] == 'positive' else PIXEL['negative'] if m['trend'] == 'negative' else PIXEL['text_secondary']
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:8px 12px; background:{PIXEL['bg_card']}; border-left:2px solid {border_clr};
                    margin-bottom:4px; font-size:11px;">
            <span style="color:{PIXEL['text_secondary']}; letter-spacing:1px;">{m['label']}</span>
            <div>
                <span style="color:{PIXEL['text_primary']}; font-weight:600;">{m['value']}</span>
                <span style="color:{chg_clr}; margin-left:8px; font-size:10px;">{m['change']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_r:
    st.markdown(section_title("SECTOR HEATMAP"), unsafe_allow_html=True)
    sectors = get_sector_heatmap()
    df_sec = pd.DataFrame(sectors)
    fig = go.Figure(data=go.Heatmap(
        z=[df_sec['change_pct'].values],
        x=df_sec['sector'].values,
        y=[''],
        text=[[f"{s} {c:+.1f}%" for s, c in zip(df_sec['sector'], df_sec['change_pct'])]],
        texttemplate="%{text}",
        textfont={"size": 10, "color": PIXEL['text_primary'], "family": "JetBrains Mono"},
        colorscale=[[0, PIXEL['negative']], [0.5, PIXEL['bg_card']], [1, PIXEL['positive']]],
        zmid=0, showscale=False,
    ))
    fig.update_layout(
        height=140, margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickfont=dict(size=9, color=PIXEL['text_secondary'], family="JetBrains Mono")),
        yaxis=dict(showticklabels=False),
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

st.markdown(hline(), unsafe_allow_html=True)

# ==== MOVERS (异动监控) ====
st.markdown(section_title("MARKET MOVERS"), unsafe_allow_html=True)
from chaneng.data_loader import get_top_movers
movers = get_top_movers()
if movers:
    mover_cols = st.columns(4)
    for i, (col, mv) in enumerate(zip(mover_cols, movers[:8])):
        with col:
            trend = "positive" if mv["change_pct"] >= 0 else "negative"
            clr = PIXEL['positive'] if trend == "positive" else PIXEL['negative']
            arrow = "▲" if trend == "positive" else "▼"
            st.markdown(f"""
            <div class="pixel-card" style="padding:10px 12px; margin-bottom:6px; cursor:pointer;"
                 onclick="window.location.href='/Stock?symbol={mv["code"]}&name={mv["name"]}&market={mv["market"]}'">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:11px; color:{PIXEL['text_primary']}; font-weight:600;">{mv['name']}</div>
                        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:1px;">{mv['code']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:13px; color:{PIXEL['text_primary']};">¥{mv['price']:.1f}</div>
                        <div style="font-size:11px; color:{clr}; font-weight:600;">{arrow}{abs(mv['change_pct']):.1f}%</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# ==== TOP STOCKS + EVENTS ====
col_l2, col_r2 = st.columns([2, 1])

with col_l2:
    st.markdown(section_title("TOP STOCKS"), unsafe_allow_html=True)
    stocks = get_top_stocks()
    df_st = pd.DataFrame(stocks)
    df_st['label'] = df_st.apply(lambda r: f"{r['name']} ({r['code']})", axis=1)
    colors = [PIXEL['positive'] if s['trend'] == 'positive' else PIXEL['negative'] for s in stocks]
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        y=df_st['label'], x=df_st['change_pct'], orientation='h',
        marker_color=colors,
        text=[f"{v:+.1f}%" for v in df_st['change_pct']],
        textposition='outside',
        textfont=dict(color=PIXEL['text_primary'], size=11, family="JetBrains Mono"),
    ))
    fig2.update_layout(
        height=260, margin=dict(l=0, r=50, t=5, b=5),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=True, zerolinecolor=PIXEL['border'],
                   tickfont=dict(color=PIXEL['text_dim'], family="JetBrains Mono")),
        yaxis=dict(showgrid=False, tickfont=dict(color=PIXEL['text_primary'], size=11, family="JetBrains Mono")),
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

with col_r2:
    st.markdown(section_title("RECENT EVENTS"), unsafe_allow_html=True)
    events = get_recent_events()
    for ev in events:
        impact_badge = badge(
            {"positive": "BULLISH", "negative": "BEARISH", "neutral": "NEUTRAL"}.get(ev['impact'], 'NEUTRAL'),
            ev['impact']
        )
        st.markdown(f"""
        <div class="pixel-card" style="padding:10px 12px; margin-bottom:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <span style="color:{PIXEL['text_dim']}; font-size:9px; letter-spacing:1px;">{ev['date']} · {ev['category']}</span>
                {impact_badge}
            </div>
            <div style="color:{PIXEL['text_primary']}; font-size:11px; line-height:1.5;">{ev['event']}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown(f'<div class="footer">CHANENG PIXEL TERMINAL · SIMULATED DATA · NOT INVESTMENT ADVICE</div>', unsafe_allow_html=True)
