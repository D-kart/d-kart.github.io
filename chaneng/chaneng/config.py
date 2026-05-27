"""
Chaneng 配置管理
===============
管理 API Key 加载、品牌常量、系统参数。
内部使用，不对外暴露数据源品牌。
"""

import json
import os
from pathlib import Path
from dataclasses import dataclass, field

# --- 路径常量 ---
CONFIG_DIR = Path.home() / ".config" / "chaneng"
API_KEYS_FILE = CONFIG_DIR / "api_keys.json"
PROJECT_ROOT = Path(__file__).parent.parent

# --- 品牌常量 ---
BRAND = {
    "name": "Chaneng",
    "tagline": "AI-Powered Investment Research",
    "subtitle": "智能投研 · 数据驱动 · 洞察先行",
    "primary_color": "#1A1F2E",
    "accent_color": "#C9A84C",  # 金色点缀
    "text_primary": "#EAEAEA",
    "text_secondary": "#8B8FA3",
    "card_bg": "#222839",
    "border_color": "#2D3348",
    "positive": "#4ECDC4",
    "negative": "#FF6B6B",
    "warning": "#F9CA24",
}

# --- 亿信 API 配置（内部使用，不对外暴露） ---
# 注意：外部展示统一使用 Chaneng 品牌，不出现 yixin/亿信 字样
API_BASE = "https://openapi.billionsintelligence.com"
SEARCH_API_URL = f"{API_BASE}/api/v2/search"
FIN_DB_API_URL = f"{API_BASE}/api/v1/fin_db"


@dataclass
class APIConfig:
    """API 配置，运行时加载"""
    search_key: str = ""
    fin_db_key: str = ""

    @classmethod
    def load(cls) -> "APIConfig":
        """从本地配置加载 API Keys"""
        config = cls()
        # 优先从环境变量加载
        config.search_key = os.environ.get("CHANENG_SEARCH_KEY", "")
        config.fin_db_key = os.environ.get("CHANENG_FIN_DB_KEY", "")
        # 回退到配置文件
        if API_KEYS_FILE.exists():
            try:
                keys = json.loads(API_KEYS_FILE.read_text())
                if not config.search_key:
                    config.search_key = keys.get("search", "")
                if not config.fin_db_key:
                    config.fin_db_key = keys.get("fin_db", "")
            except (json.JSONDecodeError, KeyError):
                pass
        return config

    @property
    def is_ready(self) -> bool:
        return bool(self.search_key and self.fin_db_key)
