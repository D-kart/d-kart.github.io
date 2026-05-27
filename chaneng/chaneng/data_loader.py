"""
Chaneng 数据加载器
==================
封装亿信 API + 模拟数据，返回结构化 dict/list。
"""

from .api import get_client


def get_financial_snapshot(symbol: str, name: str = "") -> dict:
    """个股财务快照 — 返回 raw_table + 尽力提取的关键指标"""
    client = get_client()
    query = f"{name} {symbol}"
    try:
        resp = client.fin_db(query)
    except Exception:
        return {"error": "数据查询失败", "raw": "", "metrics": {}}

    if not resp.content:
        return {"error": "未找到数据", "raw": "", "metrics": {}}

    # 尽力提取数值指标
    metrics = {}
    for line in resp.content.split("\n"):
        if "---" in line or not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 13:
            continue
        name_col = parts[11]
        val_col = parts[12]
        unit_col = parts[13] if len(parts) > 13 else ""

        # 识别关键指标
        key_words = {
            "营业总收入": "revenue", "tot_oper_rev": "revenue",
            "净利润": "net_profit", "net_profit_incl_min_int_inc": "net_profit",
            "销售毛利率": "gross_margin", "gross_profit_margin": "gross_margin",
            "销售净利率": "net_margin", "net_profit_margin": "net_margin",
            "净资产收益率": "roe", "roe": "roe",
            "营业利润": "oper_profit", "oper_profit": "oper_profit",
            "市盈率": "pe_ttm", "pe_ttm": "pe_ttm",
            "市净率": "pb_lf", "pb_lf": "pb_lf",
            "总市值": "total_mv", "员工总数": "employees",
        }
        for kw, field in key_words.items():
            if kw in name_col:
                try:
                    v = float(val_col.replace(",", ""))
                    if "%" in unit_col or "percent" in unit_col.lower():
                        v = round(v, 2)
                    elif abs(v) > 1e8:
                        v = round(v / 1e8, 2)
                    metrics[field] = v
                except (ValueError, AttributeError):
                    metrics[field] = f"{val_col} {unit_col}".strip()
                break

    return {"raw": resp.content, "metrics": metrics, "error": None}


def get_recent_events(symbol: str, name: str = "", limit: int = 8) -> list[dict]:
    client = get_client()
    try:
        resp = client.search(f"{name} {symbol}", source="announcement", count=limit, time_range="past 3 months")
    except Exception:
        return []
    return [{"title": r.title, "date": r.date, "snippet": (r.snippet or "")[:150], "link": r.link} for r in resp.items]


def get_top_movers() -> list[dict]:
    from .mock_data import get_top_stocks
    stocks = get_top_stocks()
    stocks.sort(key=lambda x: abs(x["change_pct"]), reverse=True)
    return stocks


def get_earnings_calendar() -> list[dict]:
    client = get_client()
    try:
        resp = client.search("业绩预告", source="announcement", count=20, time_range="past 1 month")
    except Exception:
        return []
    return [{"title": r.title, "date": r.date, "snippet": (r.snippet or "")[:120]} for r in resp.items]


def get_institution_visits(limit: int = 15) -> list[dict]:
    client = get_client()
    try:
        resp = client.search("投资者关系活动 调研", source="announcement", count=limit, time_range="past 1 month")
    except Exception:
        return []
    return [{"title": r.title, "date": r.date, "snippet": (r.snippet or "")[:150]} for r in resp.items]


def search_announcements(keyword: str, time_range: str = "past 3 months", limit: int = 15) -> list[dict]:
    client = get_client()
    try:
        resp = client.search(keyword, source="announcement", count=limit, time_range=time_range)
    except Exception:
        return []
    return [{"title": r.title, "date": r.date, "snippet": (r.snippet or "")[:200], "link": r.link} for r in resp.items]


def generate_brief(symbol: str, name: str = "") -> str:
    """AI 简报 — 走 fin_db 拿数据后拼接"""
    snap = get_financial_snapshot(symbol, name)
    if snap["error"]:
        return "数据获取失败"

    m = snap["metrics"]
    parts = [f"## {name or symbol} ({symbol}) 简报\n"]

    if "revenue" in m:
        parts.append(f"**营收**: {m['revenue']}{'亿' if isinstance(m['revenue'], float) else ''}")
    if "net_profit" in m:
        parts.append(f"**净利**: {m['net_profit']}{'亿' if isinstance(m['net_profit'], float) else ''}")
    if "gross_margin" in m:
        parts.append(f"**毛利率**: {m['gross_margin']}%")
    if "net_margin" in m:
        parts.append(f"**净利率**: {m['net_margin']}%")
    if "roe" in m:
        parts.append(f"**ROE**: {m['roe']}%")
    if "pe_ttm" in m:
        parts.append(f"**PE**: {m['pe_ttm']}x")
    parts.append("\n*数据来源: Chaneng AI Engine*")
    return "\n".join(parts)
