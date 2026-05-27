"""
Chaneng // AI CHAT
==================
AI 投研对话 · 亿信 API 驱动
"""
import streamlit as st
from chaneng.styles import (inject_pixel_theme, brand_header, breath_indicator, hline, PIXEL)
from chaneng.api import get_client, ChanengAPIError, ChanengQuotaExceeded, ChanengAuthError, VALID_SOURCES, SOURCE_LABELS

st.set_page_config(page_title="CHANENG // AI CHAT", page_icon="💬", layout="wide", initial_sidebar_state="expanded")
inject_pixel_theme()

with st.sidebar:
    brand_header()
    st.markdown(f'<div style="font-size:10px; color:{PIXEL["text_secondary"]}; letter-spacing:2px;">◆ CONFIG</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="height:1px; background:{PIXEL["border"]}; margin:6px 0 12px 0;"></div>', unsafe_allow_html=True)

    data_mode = st.radio(
        "MODE",
        ["FIN_DB", "SEARCH", "HYBRID"],
        index=2,
        format_func=lambda x: {"FIN_DB": "[DB] 财务数据库", "SEARCH": "[SRC] 公告搜索", "HYBRID": "[HYB] 智能综合"}.get(x, x),
        label_visibility="collapsed",
    )
    st.markdown(f'<div style="height:6px;"></div>', unsafe_allow_html=True)

    src_labels = [f"[{s.upper()}] {SOURCE_LABELS.get(s,s)}" for s in VALID_SOURCES]
    default_src_idx = 4
    source_choice = st.selectbox("SOURCE", src_labels, index=default_src_idx,
                                 disabled=(data_mode != "SEARCH"), label_visibility="collapsed")
    source = VALID_SOURCES[src_labels.index(source_choice)] if data_mode == "SEARCH" else "announcement"

    search_mode = st.selectbox("PRECISION", ["advanced", "fast", "expert"], index=0,
                               format_func=lambda x: x.upper(), disabled=(data_mode == "FIN_DB"), label_visibility="collapsed")
    time_presets = {"1W": "past 1 week", "1M": "past 1 month", "3M": "past 3 months", "6M": "past 6 months", "1Y": "past 1 year"}
    time_choice = st.selectbox("TIMEFRAME", list(time_presets.keys()), index=2,
                               format_func=lambda x: f"[{x}]", label_visibility="collapsed")
    time_range = time_presets[time_choice]

    st.markdown(f'<div style="margin-top:16px; font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:1px; line-height:1.8;">'
                f'EXAMPLES<br>├─ 宁德时代业绩<br>├─ 半导体行业趋势<br>└─ 茅台估值分析</div>', unsafe_allow_html=True)

# ==== HEADER ====
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
    <div>
        <div style="font-size:16px; color:{PIXEL['text_primary']}; letter-spacing:3px; font-weight:600;">◆ AI CHAT ENGINE</div>
        <div style="font-size:9px; color:{PIXEL['text_dim']}; letter-spacing:2px; margin-top:2px;">NATURAL LANGUAGE → CHANENG AI → STRUCTURED OUTPUT</div>
    </div>
    <div>{breath_indicator('live')} <span style="font-size:9px; color:{PIXEL['positive']}; letter-spacing:2px;">ENGINE ONLINE</span></div>
</div>
""", unsafe_allow_html=True)

st.markdown(hline(), unsafe_allow_html=True)

# ==== MESSAGES ====
if "px_msgs" not in st.session_state:
    st.session_state.px_msgs = [{
        "role": "assistant",
        "content": "> CHANENG AI ENGINE READY.\n\nCOMMANDS:\n  [DB]  FIN_DB    — 查询财务数据\n  [SRC] SEARCH    — 搜索公告资讯\n  [HYB] HYBRID    — 智能综合分析\n\nINPUT YOUR QUERY BELOW."
    }]

for msg in st.session_state.px_msgs:
    role_cls = "user" if msg["role"] == "user" else "assistant"
    st.markdown(f'<div class="chat-msg {role_cls}">{msg["content"]}</div>', unsafe_allow_html=True)

# ==== QUICK ACTIONS ====
st.markdown(f'<div style="font-size:9px; color:{PIXEL["text_dim"]}; letter-spacing:2px; margin-bottom:4px;">◆ QUICK ACTIONS</div>', unsafe_allow_html=True)
qa_col1, qa_col2, qa_col3 = st.columns(3)
with qa_col1:
    brief_btn = st.button("[ BRIEF ] 生成个股简报", key="qa_brief", use_container_width=True)
with qa_col2:
    summary_btn = st.button("[ SUMMARY ] 研报摘要", key="qa_summary", use_container_width=True)
with qa_col3:
    compare_btn = st.button("[ COMPARE ] 同业对比", key="qa_compare", use_container_width=True)

# ==== INPUT ====
col_in, col_btn = st.columns([5, 1])
with col_in:
    user_query = st.text_input("", key="px_input", placeholder="> ENTER RESEARCH QUERY...", label_visibility="collapsed")
with col_btn:
    send_btn = st.button("[ RUN ]", use_container_width=True)

# ==== PROCESS ====
# 快速动作
quick_action = None
quick_query = ""
if brief_btn:
    quick_action = "brief"
    quick_query = st.session_state.get("px_input", "").strip()
elif summary_btn:
    quick_action = "summary"
    quick_query = st.session_state.get("px_input", "").strip()
elif compare_btn:
    quick_action = "compare"
    quick_query = st.session_state.get("px_input", "").strip()

if send_btn and user_query and user_query.strip():
    query = user_query.strip()
elif quick_action and quick_query:
    query = quick_query
    if quick_action == "brief":
        query = f"生成{query}的个股简报：基本面、估值、风险"
    elif quick_action == "summary":
        query = f"搜索{query}的最新研报并给出摘要"
    elif quick_action == "compare":
        query = f"对比{query}与同行业公司的财务指标"
else:
    query = ""

if query:
    st.session_state.px_msgs.append({"role": "user", "content": f"> {query}"})

    with st.spinner("> PROCESSING..."):
        try:
            client = get_client()

            if quick_action == "summary":
                # 研报摘要模式：搜索多源研报并聚合
                resp1 = client.search(query, source="announcement", search_mode="advanced", time_range="past 6 months")
                resp2 = client.search(query, source="web", search_mode="advanced", time_range="past 6 months")
                all_items = list(resp1.items) + list(resp2.items)

                if all_items:
                    parts = [f"## ◆ RESEARCH SUMMARY: {query}\n"]
                    parts.append(f"> // AGGREGATED FROM {len(all_items)} SOURCES\n")
                    parts.append("### KEY FINDINGS\n")
                    # 聚合摘要
                    snippets = [r.snippet for r in all_items if r.snippet]
                    combined = " ".join(snippets[:5])[:800]
                    parts.append(combined if combined else "暂无详细摘要")
                    parts.append("\n### SOURCE LIST")
                    for i, r in enumerate(all_items[:8], 1):
                        parts.append(f"{i}. **{r.title}**")
                        if r.date:
                            parts.append(f"   `{r.date}`")
                        parts.append("")
                    answer = "\n".join(parts)
                else:
                    answer = "> NO RESEARCH REPORTS FOUND."

            elif data_mode == "FIN_DB":
                result = client.fin_db(query)
                if result.content:
                    lines = result.content.split("\n")
                    header = "## ◆ FIN_DB RESULT\n"
                    body = "\n".join(lines[:60])
                    trailer = f"\n\n> // {len(lines)} ROWS TOTAL" if len(lines) > 60 else ""
                    answer = header + body + trailer
                else:
                    answer = "> NO DATA FOUND. TRY MORE SPECIFIC COMPANY NAME."

            elif data_mode == "SEARCH":
                resp = client.search(query, source=source, search_mode=search_mode, time_range=time_range)
                if resp.items:
                    parts = [f"## ◆ SEARCH RESULT [{len(resp.items)} ITEMS]\n"]
                    for i, r in enumerate(resp.items[:10], 1):
                        parts.append(f"### {i}. {r.title}")
                        if r.date:
                            parts.append(f"`{r.date}` · `{SOURCE_LABELS.get(resp.source, resp.source).upper()}`")
                        if r.snippet:
                            parts.append(r.snippet[:200])
                        parts.append("")
                    answer = "\n".join(parts)
                else:
                    answer = "> NO RESULTS. TRY DIFFERENT KEYWORDS."

            else:  # HYBRID
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor(max_workers=2) as executor:
                    f1 = executor.submit(client.search, query, source="announcement", search_mode="advanced", time_range="past 3 months")
                    f2 = executor.submit(client.fin_db, query)
                    try:
                        sr = f1.result(timeout=120)
                    except Exception:
                        sr = None
                    try:
                        fr = f2.result(timeout=60)
                    except Exception:
                        fr = None

                parts = [f"## ◆ HYBRID ANALYSIS: {query}\n"]

                if fr and fr.content:
                    parts.append("### ══ FIN_DB ══")
                    flines = fr.content.split("\n")
                    parts.append("\n".join(flines[:50]))
                    if len(flines) > 50:
                        parts.append(f"\n> // {len(flines)} TOTAL ROWS, TRUNCATED")
                    parts.append("")

                if sr and sr.items:
                    parts.append("### ══ SEARCH ══")
                    for i, r in enumerate(sr.items[:5], 1):
                        parts.append(f"**{i}. {r.title}**")
                        if r.date:
                            parts.append(f"`{r.date}`")
                        if r.snippet:
                            parts.append(r.snippet[:150])
                        parts.append("")

                if (not fr or not fr.content) and (not sr or not sr.items):
                    parts.append("> // NO DATA. TRY [DB] OR [SRC] MODE SEPARATELY.")

                answer = "\n".join(parts)

        except ChanengQuotaExceeded:
            answer = "> // ERROR: QUOTA EXCEEDED. CONTACT ADMIN."
        except ChanengAuthError:
            answer = "> // ERROR: AUTH FAILED. CHECK API KEY."
        except ChanengAPIError as e:
            answer = f"> // ERROR: {str(e)[:200]}"
        except Exception as e:
            answer = f"> // FATAL: {str(e)[:200]}"

    st.session_state.px_msgs.append({"role": "assistant", "content": answer})
    st.rerun()

st.markdown(f'<div class="footer">CHANENG AI ENGINE · PUBLIC DATA ONLY</div>', unsafe_allow_html=True)
