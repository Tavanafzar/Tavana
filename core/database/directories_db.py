"""لایه‌ی دسترسی به داده‌ها برای تیبل‌های directories و type_history؛ دیتابیس مستقل UIH.db."""

import os
import sqlite3
import threading
import time
from contextlib import contextmanager
from core.paths.paths import app_path, resource_path

UIH_DB_PATH = app_path("data", "UIH.db")

DEFAULT_HISTORY_LIMIT = 2000

_DEFAULT_LIGHT_ICON = resource_path("assets", "icons", "recently.png")
_DEFAULT_DARK_ICON = resource_path("assets", "icons", "recently.png")

_uih_init_lock = threading.Lock()
_uih_initialized = False

_UIH_SCHEMA = """
              CREATE TABLE IF NOT EXISTS directories
              (
                  filename
                  TEXT
                  PRIMARY
                  KEY,
                  path
                  TEXT
                  NOT
                  NULL
              );

              CREATE TABLE IF NOT EXISTS type_history
              (
                  id
                  INTEGER
                  PRIMARY
                  KEY
                  AUTOINCREMENT,
                  text
                  TEXT
                  NOT
                  NULL
                  UNIQUE,
                  light_icon
                  TEXT
                  NOT
                  NULL,
                  dark_icon
                  TEXT
                  NOT
                  NULL,
                  created_at
                  REAL
                  NOT
                  NULL
              );
              CREATE INDEX IF NOT EXISTS idx_type_history_created_at ON type_history(created_at DESC); \
              """


@contextmanager
def _get_uih_conn():
    """یک اتصال SQLite جدید به UIH.db باز می‌کند و در پایان بلوک with آن را می‌بندد."""
    if not _uih_initialized:
        raise RuntimeError(
            "دیتابیس UIH هنوز init نشده — ابتدا init_uih_db() را در main.py صدا بزنید."
        )

    conn = sqlite3.connect(UIH_DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_uih_db() -> None:
    """دیتابیس UIH.db را یک‌بار مقداردهی اولیه می‌کند: ساخت فایل (در صورت نبود) و ساخت جدول‌های directories و type_history."""
    global _uih_initialized

    with _uih_init_lock:
        if _uih_initialized:
            return

        os.makedirs(os.path.dirname(UIH_DB_PATH), exist_ok=True)

        conn = sqlite3.connect(UIH_DB_PATH, timeout=10)
        conn.row_factory = sqlite3.Row

        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(_UIH_SCHEMA)
            conn.commit()
        finally:
            conn.close()

        _uih_initialized = True


# ---------- directories ----------

def get_directories() -> dict[str, str]:
    """کش نام‌فایل → مسیر کامل را از UIH.db برمی‌گرداند."""
    with _get_uih_conn() as conn:
        rows = conn.execute(
            "SELECT filename, path FROM directories").fetchall()
    return {row["filename"]: row["path"] for row in rows}


def save_directories(directories: dict[str, str]) -> None:
    """درج/به‌روزرسانی گروهی مسیرها (upsert) در UIH.db — فقط ردیف‌های داده‌شده نوشته می‌شوند."""
    if not directories:
        return
    with _get_uih_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO directories (filename, path) VALUES (?, ?)",
            list(directories.items()),
        )
        conn.commit()


def clear_directory_history() -> None:
    """کش مسیر همه‌ی فایل‌ها/برنامه‌های پیداشده را در UIH.db پاک می‌کند."""
    with _get_uih_conn() as conn:
        conn.execute("DELETE FROM directories")
        conn.commit()


# ---------- type_history ----------

def get_type_history(limit: int = DEFAULT_HISTORY_LIMIT) -> list[tuple[str, str, str]]:
    """جدیدترین آیتم‌های تایپ‌شده را از UIH.db به ترتیب نزولی زمان برمی‌گرداند."""
    with _get_uih_conn() as conn:
        rows = conn.execute(
            "SELECT text, light_icon, dark_icon FROM type_history "
            "ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [(row["text"], row["light_icon"], row["dark_icon"]) for row in rows]


def add_type_history(
        text: str,
        light_icon: str = _DEFAULT_LIGHT_ICON,
        dark_icon: str = _DEFAULT_DARK_ICON,
        max_items: int = DEFAULT_HISTORY_LIMIT,
) -> None:
    """یک متن را به تاریخچه‌ی UIH.db اضافه می‌کند؛ اگر تکراری باشد فقط زمانش را به‌روز می‌کند.

    در پایان، قدیمی‌ترین ردیف‌های بیش از سقف مجاز حذف می‌شوند.
    """
    with _get_uih_conn() as conn:
        conn.execute(
            "INSERT INTO type_history (text, light_icon, dark_icon, created_at) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(text) DO UPDATE SET created_at = excluded.created_at",
            (text, light_icon, dark_icon, time.time()),
        )
        conn.execute(
            "DELETE FROM type_history WHERE id NOT IN ("
            "  SELECT id FROM type_history ORDER BY created_at DESC LIMIT ?"
            ")",
            (max_items,),
        )
        conn.commit()


def clear_type_history() -> None:
    """کل تاریخچه‌ی تایپ را در UIH.db پاک می‌کند."""
    with _get_uih_conn() as conn:
        conn.execute("DELETE FROM type_history")
        conn.commit()