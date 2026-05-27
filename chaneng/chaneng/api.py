"""
Chaneng AI 引擎 — 亿信 API 封装
===============================
内部调用亿信 OpenAPI，对外统一展示为 Chaneng 品牌。
所有错误处理和限流提示均使用 Chaneng 口径。

实际 API 响应格式（实测）：
- search: result 是 list，每组有 query/content/status/source，content 是 [{"title","link","snippet","date","extra"},...]
- fin_db: result 是 list，每组有 query/content，content 是 markdown table 字符串
- 有效 source: web, academic, image, video, announcement（无 report/expert）
"""

import json
import time
import urllib.request
import urllib.error
from typing import Any, Optional
from dataclasses import dataclass, field

from .config import SEARCH_API_URL, FIN_DB_API_URL, APIConfig


# --- 有效数据源 ---
VALID_SOURCES = ["web", "academic", "image", "video", "announcement"]
SOURCE_LABELS = {
    "web": "网页",
    "academic": "学术",
    "image": "图片",
    "video": "视频",
    "announcement": "公告",
}


class ChanengAPIError(Exception):
    pass


class ChanengQuotaExceeded(ChanengAPIError):
    pass


class ChanengAuthError(ChanengAPIError):
    pass


@dataclass
class SearchItem:
    title: str
    link: str = ""
    snippet: str = ""
    date: str = ""
    extra: dict = field(default_factory=dict)


@dataclass
class SearchResponse:
    query: str
    items: list[SearchItem] = field(default_factory=list)
    source: str = ""
    status: str = ""


@dataclass
class FinDBResponse:
    query: str
    content: str = ""  # markdown table


class ChanengClient:
    """Chaneng AI 客户端"""

    def __init__(self, config: Optional[APIConfig] = None):
        self.config = config or APIConfig.load()

    def _call_api(self, url: str, payload: dict, timeout: int = 120, max_retries: int = 2) -> dict:
        api_key = None
        if "search" in url:
            api_key = self.config.search_key
        elif "fin_db" in url:
            api_key = self.config.fin_db_key

        if not api_key:
            raise ChanengAuthError("API Key 未配置，请检查 Chaneng 配置")

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        for attempt in range(max_retries + 1):
            try:
                req = urllib.request.Request(
                    url, data=body, method="POST",
                    headers={"Content-Type": "application/json", "Accept": "application/json", "X-API-KEY": api_key},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return json.loads(resp.read().decode("utf-8", errors="replace"))

            except urllib.error.HTTPError as exc:
                error_body = ""
                try:
                    error_body = exc.read().decode("utf-8", errors="replace")
                except Exception:
                    pass

                if exc.code == 429:
                    raise ChanengQuotaExceeded("查询额度已用完，请联系 Chaneng 管理员升级服务")
                elif exc.code in (401, 403):
                    raise ChanengAuthError(f"API 认证失败 (HTTP {exc.code})")
                elif exc.code >= 500 and attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                else:
                    raise ChanengAPIError(f"API 请求失败 (HTTP {exc.code}): {error_body[:200]}")

            except (urllib.error.URLError, TimeoutError) as e:
                if attempt < max_retries:
                    time.sleep(2 ** attempt)
                    continue
                raise ChanengAPIError(f"网络连接失败: {str(e)}")

        raise ChanengAPIError("API 调用失败：已达最大重试次数")

    def search(
        self,
        query: str,
        source: str = "announcement",
        search_mode: str = "advanced",
        count: int = 10,
        time_range: str = "past 3 months",
    ) -> SearchResponse:
        """
        搜索公告/资讯/学术/网页等。
        有效 source: web, academic, image, video, announcement
        """
        if source not in VALID_SOURCES:
            source = "announcement"

        payload = {
            "query": query,
            "source": source,
            "search_mode": search_mode,
            "count": min(count, 50),
            "time_range": time_range,
        }

        raw = self._call_api(SEARCH_API_URL, payload, timeout=120)
        result_list = raw.get("result", [])

        all_items = []
        src_name = ""
        status = ""

        if isinstance(result_list, list):
            for group in result_list:
                src_name = group.get("source", src_name)
                status = group.get("status", status)
                content = group.get("content", [])
                if isinstance(content, list):
                    for item in content:
                        all_items.append(SearchItem(
                            title=item.get("title", ""),
                            link=item.get("link", ""),
                            snippet=item.get("snippet", ""),
                            date=item.get("date", ""),
                            extra=item.get("extra", {}),
                        ))

        return SearchResponse(
            query=query,
            items=all_items,
            source=src_name,
            status=status,
        )

    def fin_db(self, query: str, data_sources: Optional[list[str]] = None) -> FinDBResponse:
        """
        查询金融数据库（财务数据/行情/宏观）。
        """
        payload = {"query": query, "data_sources": data_sources or ["auto"]}
        raw = self._call_api(FIN_DB_API_URL, payload, timeout=60)

        result_list = raw.get("result", [])
        all_content = []

        if isinstance(result_list, list):
            for group in result_list:
                content = group.get("content", "")
                if content:
                    all_content.append(content)

        return FinDBResponse(
            query=query,
            content="\n\n".join(all_content),
        )


# --- 便捷函数 ---
_default_client: Optional[ChanengClient] = None


def get_client() -> ChanengClient:
    global _default_client
    if _default_client is None:
        _default_client = ChanengClient()
    return _default_client


def search(query: str, source: str = "announcement", search_mode: str = "advanced",
           count: int = 10, time_range: str = "past 3 months") -> SearchResponse:
    return get_client().search(query, source, search_mode, count, time_range)


def fin_db(query: str, data_sources: Optional[list[str]] = None) -> FinDBResponse:
    return get_client().fin_db(query, data_sources)
