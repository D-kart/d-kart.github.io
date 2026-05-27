"""
Chaneng — Pixel Terminal Pro
=============================
Longbridge 风格融合：高信息密度 · 模块化卡片 · 像素暗黑终端
"""

import streamlit as st

# ============================================================
# PIXEL COLOR SYSTEM
# ============================================================
PIXEL = {
    "bg_deep": "#06080d",
    "bg_surface": "#0a0e17",
    "bg_card": "#0d1320",
    "bg_card_hover": "#111827",
    "bg_raised": "#131a2a",
    "border": "#1a2740",
    "border_light": "#233056",
    "border_active": "#c9a84c",
    "text_primary": "#dde1ea",
    "text_secondary": "#5a6880",
    "text_dim": "#364258",
    "accent": "#c9a84c",
    "accent_dim": "rgba(201,168,76,0.12)",
    "accent_glow": "rgba(201,168,76,0.25)",
    "positive": "#34d399",
    "positive_dim": "rgba(52,211,153,0.12)",
    "negative": "#f87171",
    "negative_dim": "rgba(248,113,113,0.12)",
    "warning": "#fbbf24",
    "info": "#60a5fa",
    "scanline": "rgba(255,255,255,0.012)",
    "grid": "rgba(26,39,64,0.35)",
    "pixel_dot": "rgba(201,168,76,0.4)",
}


# ============================================================
# THEME INJECTION
# ============================================================
def inject_pixel_theme() -> None:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    * {{ font-family: 'JetBrains Mono', 'Consolas', monospace !important; }}

    .stApp {{
        background: {PIXEL['bg_deep']};
        background-image:
            linear-gradient({PIXEL['grid']} 1px, transparent 1px),
            linear-gradient(90deg, {PIXEL['grid']} 1px, transparent 1px);
        background-size: 40px 40px;
    }}

    .stApp::before {{
        content: ''; position: fixed; inset: 0;
        background: repeating-linear-gradient(0deg, transparent, transparent 2px, {PIXEL['scanline']} 2px, {PIXEL['scanline']} 4px);
        pointer-events: none; z-index: 9999;
    }}

    @keyframes scanBeam {{
        0% {{ top: -2px; opacity: 0; }} 10% {{ opacity: 0.25; }} 90% {{ opacity: 0.25; }} 100% {{ top: 100%; opacity: 0; }}
    }}
    .stApp::after {{
        content: ''; position: fixed; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, {PIXEL['accent']}, transparent);
        pointer-events: none; z-index: 10000;
        animation: scanBeam 10s linear infinite; opacity: 0.12;
    }}

    /* SIDEBAR */
    section[data-testid="stSidebar"] {{
        background: {PIXEL['bg_surface']} !important;
        border-right: 1px solid {PIXEL['border']} !important;
    }}
    section[data-testid="stSidebar"] * {{ color: {PIXEL['text_primary']} !important; }}

    /* SCROLLBAR */
    ::-webkit-scrollbar {{ width: 4px; height: 4px; }}
    ::-webkit-scrollbar-track {{ background: {PIXEL['bg_deep']}; }}
    ::-webkit-scrollbar-thumb {{ background: {PIXEL['border']}; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {PIXEL['accent']}; }}

    /* INPUTS */
    input, textarea, .stTextInput input {{
        background: {PIXEL['bg_card']} !important; border: 1px solid {PIXEL['border']} !important;
        color: {PIXEL['text_primary']} !important; padding: 8px 12px !important;
        font-size: 12px !important; letter-spacing: 1px !important;
    }}
    input:focus, textarea:focus {{
        border-color: {PIXEL['accent']} !important;
        box-shadow: 0 0 12px {PIXEL['accent_dim']} !important; outline: none !important;
    }}

    /* BUTTONS */
    .stButton > button {{
        background: {PIXEL['bg_card']} !important; color: {PIXEL['accent']} !important;
        border: 1px solid {PIXEL['border']} !important; font-size: 11px !important;
        letter-spacing: 1.5px !important; padding: 6px 16px !important;
        font-weight: 500 !important; transition: all 0.2s !important;
    }}
    .stButton > button:hover {{
        border-color: {PIXEL['accent']} !important;
        box-shadow: 0 0 16px {PIXEL['accent_dim']} !important;
        background: {PIXEL['bg_raised']} !important;
    }}

    /* SELECT / RADIO */
    .stSelectbox > div > div {{ background: {PIXEL['bg_card']} !important; border: 1px solid {PIXEL['border']} !important; }}

    h1 {{ font-size: 15px !important; letter-spacing: 3px !important; font-weight: 600 !important; }}
    h2 {{ font-size: 12px !important; letter-spacing: 2px !important; font-weight: 600 !important; }}
    h3 {{ font-size: 10px !important; letter-spacing: 2px !important; font-weight: 500 !important; color: {PIXEL['text_secondary']} !important; }}
    </style>

    <canvas id="pixel-particles"></canvas>
    <script>
    (function(){{
        var c=document.getElementById('pixel-particles');if(!c)return;
        var x=c.getContext('2d'),d=[],W,H,s=48;
        function r(){{W=c.width=window.innerWidth;H=c.height=window.innerHeight;}}
        r();window.addEventListener('resize',r);
        for(var i=0;i<Math.ceil(W/s);i++)for(var j=0;j<Math.ceil(H/s);j++)
            d.push({{x:i*s+Math.random()*12-6,y:j*s+Math.random()*12-6,r:Math.random()>.85?1.5:1,p:Math.random()*6.28,v:.3+Math.random()*.8}});
        function f(){{x.clearRect(0,0,W,H);var t=Date.now()*.001;
        for(var i=0;i<d.length;i++){{var a=.06+.08*Math.sin(t*d[i].v+d[i].p);
        x.fillStyle='rgba(201,168,76,'+a+')';x.fillRect(d[i].x,d[i].y,d[i].r,d[i].r);}}
        requestAnimationFrame(f);}}f();
    }})();
    </script>
    """, unsafe_allow_html=True)


# ============================================================
# BRAND & NAVIGATION
# ============================================================
def brand_header():
    st.markdown(f"""
    <div style="margin-bottom:16px;">
        <div style="font-size:18px; font-weight:700; letter-spacing:5px; color:{PIXEL['text_primary']};">
            CHAN<span style="color:{PIXEL['accent']};">ENG</span>
        </div>
        <div style="height:1px; background:linear-gradient(90deg,{PIXEL['accent']},transparent 80%); margin:8px 0 4px 0;"></div>
        <div style="font-size:8px; color:{PIXEL['text_dim']}; letter-spacing:3px;">PIXEL TERMINAL PRO</div>
    </div>
    """, unsafe_allow_html=True)


def market_tabs(active: str = "OVERVIEW") -> str:
    """市场切换标签 — 返回选中的 tab"""
    tabs = ["OVERVIEW", "A-SHARE", "HK", "US"]
    html = '<div style="display:flex; gap:0; margin-bottom:16px; border-bottom:1px solid ' + PIXEL['border'] + ';">'
    for t in tabs:
        is_active = t == active
        html += f'''
        <a href="?tab={t}" style="
            text-decoration:none; padding:8px 16px;
            font-size:11px; letter-spacing:2px; font-weight:{600 if is_active else 400};
            color:{PIXEL['text_primary'] if is_active else PIXEL['text_dim']};
            border-bottom:{'2px solid ' + PIXEL['accent'] if is_active else '2px solid transparent'};
            transition:all 0.2s;
        ">{t}</a>'''
    html += '</div>'
    return html


# ============================================================
# TICKER STRIP
# ============================================================
def ticker_strip(indices: list) -> str:
    """紧凑指数行情条"""
    items = []
    for idx in indices:
        arrow = "▲" if idx.trend == "positive" else "▼"
        color = PIXEL['positive'] if idx.trend == "positive" else PIXEL['negative']
        items.append(f'<span style="color:{PIXEL["text_secondary"]}; font-size:10px;">{idx.name[:4]}</span> '
                     f'<span style="color:{PIXEL["text_primary"]}; font-size:11px;">{idx.price:,.0f}</span> '
                     f'<span style="color:{color}; font-size:10px;">{arrow}{abs(idx.change_pct):.2f}%</span>')

    return f'''
    <div style="display:flex; align-items:center; gap:6px; padding:6px 12px;
                background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']};
                overflow-x:auto; white-space:nowrap; margin-bottom:14px; font-size:10px;">
        <span style="color:{PIXEL['accent']}; letter-spacing:2px; margin-right:4px;">◆</span>
        {" <span style='color:" + PIXEL['border'] + ";'>│</span> ".join(items)}
    </div>
    '''


# ============================================================
# CARD VARIANTS
# ============================================================
def index_card(symbol: str, name: str, price: str, change: str, pct: str, trend: str,
               sparkline_data: list = None) -> str:
    """Longbridge 风格指数卡片"""
    clr = PIXEL['positive'] if trend == "positive" else PIXEL['negative']
    arrow = "▲" if trend == "positive" else "▼"
    spark = ""
    if sparkline_data:
        spark = '<div style="height:24px; margin-top:4px;">' + ''.join(
            f'<span style="display:inline-block;width:3px;height:{max(4,abs(v)*3)}px;background:{clr};margin:0 1px;opacity:{0.4+abs(v)*0.5};"></span>'
            for v in sparkline_data[-20:]) + '</div>'

    return f'''
    <div style="
        background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']};
        padding:14px 16px; transition:all 0.25s; cursor:pointer;
    " onmouseover="this.style.borderColor='{PIXEL['accent']}';this.style.boxShadow='0 0 20px {PIXEL['accent_dim']}';"
       onmouseout="this.style.borderColor='{PIXEL['border']}';this.style.boxShadow='none';">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px;">{symbol}</div>
                <div style="font-size:12px; color:{PIXEL['text_primary']}; font-weight:600; letter-spacing:1px; margin-top:2px;">{name}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:16px; color:{PIXEL['text_primary']}; font-weight:700;">{price}</div>
                <div style="font-size:11px; color:{clr}; margin-top:2px;">
                    {arrow} {change} &nbsp;{pct}
                </div>
            </div>
        </div>
        {spark}
    </div>
    '''


def compact_card(title: str, lines: list, link: str = "", badge_text: str = "") -> str:
    """紧凑信息卡片"""
    badge_html = f'<span style="border:1px solid {PIXEL["border"]};padding:2px 6px;font-size:8px;color:{PIXEL["accent"]};letter-spacing:1px;margin-left:8px;">{badge_text}</span>' if badge_text else ''
    rows = ''.join(f'<div style="font-size:11px; color:{PIXEL["text_primary"]}; padding:3px 0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{l}</div>' for l in lines[:4])
    footer = f'<a href="{link}" style="font-size:9px; color:{PIXEL["accent"]}; letter-spacing:1px; text-decoration:none;">[ VIEW ALL → ]</a>' if link else ''
    return f'''
    <div style="background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']}; padding:12px 14px; transition:all 0.2s;"
         onmouseover="this.style.borderColor='{PIXEL['accent']}';"
         onmouseout="this.style.borderColor='{PIXEL['border']}';">
        <div style="display:flex; align-items:center; margin-bottom:8px;">
            <span style="color:{PIXEL['accent']}; font-size:8px; margin-right:6px;">◆</span>
            <span style="font-size:10px; color:{PIXEL['text_secondary']}; letter-spacing:2px; font-weight:600;">{title}</span>
            {badge_html}
        </div>
        {rows}
        <div style="margin-top:6px;">{footer}</div>
    </div>
    '''


def data_row(label: str, value: str, change: str = "", trend: str = "") -> str:
    """键值数据行"""
    chg = ""
    if change:
        clr = PIXEL['positive'] if trend == "positive" else PIXEL['negative'] if trend == "negative" else PIXEL['text_secondary']
        chg = f'<span style="color:{clr}; font-size:10px; margin-left:6px;">{change}</span>'
    return f'''
    <div style="display:flex; justify-content:space-between; align-items:center;
                padding:6px 10px; border-bottom:1px solid rgba(26,39,64,0.3); font-size:11px;">
        <span style="color:{PIXEL['text_secondary']};">{label}</span>
        <div><span style="color:{PIXEL['text_primary']}; font-weight:500;">{value}</span>{chg}</div>
    </div>
    '''


def section_header(title: str, link: str = "", badge_text: str = "") -> str:
    """段落标题 + View All 链接"""
    badge_html = f'<span style="border:1px solid {PIXEL["border"]};padding:2px 6px;font-size:8px;color:{PIXEL["accent"]};letter-spacing:1px;margin-left:8px;">{badge_text}</span>' if badge_text else ''
    link_html = f'<a href="{link}" style="font-size:9px; color:{PIXEL["accent"]}; letter-spacing:1px; text-decoration:none; margin-left:auto;">[ ALL → ]</a>' if link else ''
    return f'''
    <div style="display:flex; align-items:center; margin-bottom:10px;">
        <span style="color:{PIXEL["accent"]}; font-size:8px; margin-right:6px;">◆</span>
        <span style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px; font-weight:600;">{title}</span>
        {badge_html}
        {link_html}
    </div>
    '''


def hline() -> str:
    return '<div style="height:1px; background:linear-gradient(90deg,transparent,' + PIXEL['border'] + ' 20%,' + PIXEL['border'] + ' 80%,transparent); margin:16px 0;"></div>'


def badge(text: str, style: str = "accent") -> str:
    clr = {"accent": PIXEL['accent'], "positive": PIXEL['positive'], "negative": PIXEL['negative']}.get(style, PIXEL['accent'])
    dim = {"accent": PIXEL['accent_dim'], "positive": PIXEL['positive_dim'], "negative": PIXEL['negative_dim']}.get(style, PIXEL['accent_dim'])
    return f'<span style="border:1px solid {clr}; background:{dim}; padding:2px 6px; font-size:8px; color:{clr}; letter-spacing:1px;">{text}</span>'


def breath_dot(color: str = "") -> str:
    c = color or PIXEL['positive']
    return f'<span style="display:inline-block;width:5px;height:5px;background:{c};margin-right:5px;animation:breathe 2.5s ease-in-out infinite;"></span>'


def metric_block(label: str, value: str, change: str = "", trend: str = "neutral") -> str:
    clr = PIXEL['positive'] if trend == "positive" else PIXEL['negative'] if trend == "negative" else PIXEL['text_secondary']
    chg_html = f'<div style="font-size:10px; color:{clr}; margin-top:3px;">{change}</div>' if change else ''
    return f'''
    <div style="background:{PIXEL['bg_card']}; border:1px solid {PIXEL['border']};
                padding:12px; text-align:center; transition:all 0.2s;"
         onmouseover="this.style.borderColor='{PIXEL['accent']}';"
         onmouseout="this.style.borderColor='{PIXEL['border']}';">
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-bottom:4px;">{label}</div>
        <div style="font-size:18px; color:{PIXEL['text_primary']}; font-weight:700;">{value}</div>
        {chg_html}
    </div>
    '''


# === BACKWARD COMPATIBILITY ===
section_title = section_header
breath_indicator = breath_dot
