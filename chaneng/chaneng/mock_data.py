"""
Chaneng 模拟行情数据
===================
第一期 Demo 使用模拟数据。
后续对接 AKShare 等行情源替换本模块。
"""

import random
import datetime
from typing import Any
from dataclasses import dataclass


@dataclass
class IndexData:
    symbol: str
    name: str
    price: float
    change_pct: float
    change_amt: float
    volume: str

    @property
    def trend(self) -> str:
        return "positive" if self.change_pct >= 0 else "negative"


def get_market_indices() -> list[IndexData]:
    """获取主要市场指数（模拟数据）"""
    indices = [
        IndexData("000001.SH", "上证指数", 3368.82, 1.23, 40.91, "4,823亿"),
        IndexData("399001.SZ", "深证成指", 10876.54, 0.87, 93.75, "6,241亿"),
        IndexData("399006.SZ", "创业板指", 2156.34, 2.15, 45.37, "2,847亿"),
        IndexData("000688.SH", "科创50", 968.72, -0.34, -3.31, "781亿"),
        IndexData("HSI", "恒生指数", 19234.56, 0.58, 111.02, "1,256亿港币"),
        IndexData("HSCEI", "国企指数", 6876.12, 0.92, 62.58, "487亿港币"),
    ]
    # 轻微随机扰动
    for idx in indices:
        noise = random.uniform(-0.3, 0.3)
        idx.price = round(idx.price + noise, 2)
        idx.change_pct = round(idx.change_pct + noise * 0.1, 2)
        idx.change_amt = round(idx.change_amt + noise * 10, 2)
    return indices


def get_macro_indicators() -> list[dict[str, Any]]:
    """获取关键宏观指标（模拟）"""
    return [
        {"label": "GDP增速(Q1)", "value": "5.3%", "change": "+0.1pct", "trend": "positive"},
        {"label": "CPI 同比", "value": "0.3%", "change": "+0.1pct", "trend": "neutral"},
        {"label": "PMI 制造业", "value": "50.8", "change": "+0.4", "trend": "positive"},
        {"label": "社融增量", "value": "4.87万亿", "change": "-0.3万亿", "trend": "negative"},
        {"label": "M2 同比", "value": "8.3%", "change": "+0.2pct", "trend": "positive"},
        {"label": "LPR 1年期", "value": "3.45%", "change": "持平", "trend": "neutral"},
        {"label": "美元/人民币", "value": "7.24", "change": "-0.03", "trend": "positive"},
        {"label": "10Y国债收益率", "value": "2.28%", "change": "-0.05pct", "trend": "positive"},
    ]


def get_sector_heatmap() -> list[dict[str, Any]]:
    """获取行业板块热力图数据（模拟）"""
    sectors = [
        ("AI/人工智能", 4.2), ("半导体", 3.8), ("新能源", -1.5), ("光伏", -2.1),
        ("消费电子", 2.3), ("创新药", 5.1), ("白酒", -0.8), ("银行", 0.3),
        ("券商", 1.8), ("保险", -0.5), ("房地产", -3.2), ("基建", 0.7),
        ("电力", 1.2), ("煤炭", -1.8), ("汽车", 2.9), ("军工", 3.5),
        ("通信", 1.6), ("传媒", -2.4), ("食品饮料", -0.3), ("家电", 1.1),
    ]
    result = []
    for name, change in sectors:
        # 加噪声
        adj = round(change + random.uniform(-0.5, 0.5), 2)
        result.append({
            "sector": name,
            "change_pct": adj,
            "trend": "positive" if adj >= 0 else "negative",
        })
    random.shuffle(result)
    return result


def get_top_stocks() -> list[dict[str, Any]]:
    """获取热门标的（模拟）"""
    stocks = [
        {"code": "300750", "name": "宁德时代", "price": 218.50, "change_pct": 3.21, "pe": 22.5, "market": "A股"},
        {"code": "600519", "name": "贵州茅台", "price": 1672.00, "change_pct": -0.45, "pe": 28.3, "market": "A股"},
        {"code": "002594", "name": "比亚迪", "price": 286.30, "change_pct": 4.56, "pe": 35.8, "market": "A股"},
        {"code": "688981", "name": "中芯国际", "price": 56.80, "change_pct": 6.78, "pe": 42.1, "market": "A股"},
        {"code": "00700", "name": "腾讯控股", "price": 385.60, "change_pct": 1.87, "pe": 18.2, "market": "港股"},
        {"code": "09988", "name": "阿里巴巴", "price": 79.35, "change_pct": -1.23, "pe": 12.6, "market": "港股"},
        {"code": "03690", "name": "美团", "price": 112.40, "change_pct": 2.45, "pe": 25.9, "market": "港股"},
        {"code": "01810", "name": "小米集团", "price": 28.60, "change_pct": 5.12, "pe": 32.4, "market": "港股"},
    ]
    for s in stocks:
        s["change_pct"] = round(s["change_pct"] + random.uniform(-2, 2), 2)
        s["trend"] = "positive" if s["change_pct"] >= 0 else "negative"
    return stocks


def get_recent_events() -> list[dict[str, Any]]:
    """获取近期市场事件（模拟）"""
    return [
        {"date": "2026-05-26", "event": "央行开展2000亿MLF操作，利率持平", "impact": "neutral", "category": "货币政策"},
        {"date": "2026-05-25", "event": "国务院常务会议：加大对科技企业融资支持", "impact": "positive", "category": "政策"},
        {"date": "2026-05-24", "event": "美国4月PCE数据超预期，降息预期降温", "impact": "negative", "category": "海外宏观"},
        {"date": "2026-05-23", "event": "国家大基金三期成立，注册资本3440亿", "impact": "positive", "category": "产业政策"},
        {"date": "2026-05-22", "event": "证监会：进一步规范量化交易监管", "impact": "neutral", "category": "监管"},
    ]


def price_chart_data(symbol: str = "000001.SH", days: int = 60) -> list[dict]:
    """生成模拟 K 线数据"""
    data = []
    now = datetime.date.today()
    base = 3300 if "SH" in symbol else 10500
    price = base + random.uniform(-200, 200)

    for i in range(days, 0, -1):
        date = now - datetime.timedelta(days=i)
        change = random.uniform(-1.5, 1.5)
        price = max(price + change, base * 0.7)
        open_p = round(price + random.uniform(-20, 20), 2)
        close_p = round(price, 2)
        high_p = round(max(open_p, close_p) + random.uniform(0, 30), 2)
        low_p = round(min(open_p, close_p) - random.uniform(0, 30), 2)
        data.append({
            "date": date.isoformat(),
            "open": open_p,
            "high": high_p,
            "low": low_p,
            "close": close_p,
            "volume": random.randint(1000000, 5000000),
        })
    return data
