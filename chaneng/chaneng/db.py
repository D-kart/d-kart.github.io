"""
Chaneng SQLite 数据库
=====================
自选股池持久化存储。
"""

import sqlite3
import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

DB_DIR = Path(__file__).parent.parent / "data"
DB_PATH = DB_DIR / "chaneng.db"


@dataclass
class WatchItem:
    symbol: str       # e.g. "600519"
    name: str         # "贵州茅台"
    market: str       # "A-SHARE" or "HK"
    added_at: str = ""
    notes: str = ""
    id: Optional[int] = None

    def __post_init__(self):
        if not self.added_at:
            self.added_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def _get_conn() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT NOT NULL,
            market TEXT NOT NULL DEFAULT 'A-SHARE',
            added_at TEXT NOT NULL,
            notes TEXT DEFAULT '',
            UNIQUE(symbol, market)
        )
    """)
    conn.commit()
    conn.close()


def add_watch(item: WatchItem) -> bool:
    """添加自选，返回是否新增（False=已存在）"""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO watchlist (symbol, name, market, added_at, notes) VALUES (?,?,?,?,?)",
            (item.symbol, item.name, item.market, item.added_at, item.notes),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def remove_watch(symbol: str, market: str = "A-SHARE") -> bool:
    conn = _get_conn()
    cur = conn.execute("DELETE FROM watchlist WHERE symbol=? AND market=?", (symbol, market))
    conn.commit()
    conn.close()
    return cur.rowcount > 0


def get_all_watch() -> list[WatchItem]:
    conn = _get_conn()
    rows = conn.execute("SELECT * FROM watchlist ORDER BY added_at DESC").fetchall()
    conn.close()
    return [WatchItem(
        id=r["id"], symbol=r["symbol"], name=r["name"],
        market=r["market"], added_at=r["added_at"], notes=r["notes"],
    ) for r in rows]


def is_watched(symbol: str, market: str = "A-SHARE") -> bool:
    conn = _get_conn()
    row = conn.execute(
        "SELECT 1 FROM watchlist WHERE symbol=? AND market=?", (symbol, market)
    ).fetchone()
    conn.close()
    return row is not None


def update_notes(symbol: str, market: str, notes: str):
    conn = _get_conn()
    conn.execute(
        "UPDATE watchlist SET notes=? WHERE symbol=? AND market=?", (notes, symbol, market)
    )
    conn.commit()
    conn.close()


# 初始化
init_db()
