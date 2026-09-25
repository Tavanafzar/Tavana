"""لایه‌ی دسترسی به داده‌ها؛ تنها نقطه‌ی ورود به دیتابیس SQLite برنامه."""

import json
import os
import shutil
import sqlite3
import threading
import time
from contextlib import contextmanager
from core.paths.paths import app_path, resource_path

DB_PATH = app_path("data", "configuration.db")
_LEGACY_DB_PATH = resource_path("data", "configuration.db")
#LEGACY_JSON_PATH = app_path("data", "data.json")

DEFAULT_ANIMATION_SPEEDS = [200, 150]

_init_lock = threading.Lock()
_initialized = False

_SCHEMA = """
          CREATE TABLE IF NOT EXISTS app_info
          (
              key
              TEXT
              PRIMARY
              KEY,
              value
              TEXT
              NOT
              NULL
          );

          CREATE TABLE IF NOT EXISTS windows_command
          (
              keyword
              TEXT
              PRIMARY
              KEY,
              action
              TEXT
              NOT
              NULL
          );

          CREATE TABLE IF NOT EXISTS tavana_command
          (
              keyword
              TEXT
              PRIMARY
              KEY,
              action
              TEXT
              NOT
              NULL
          );

          CREATE TABLE IF NOT EXISTS tavana_settings
          (
              id
              INTEGER
              PRIMARY
              KEY
              CHECK
              (
                  id
                  =
                  0
              ),
              fade_in_ms
              INTEGER
              NOT
              NULL,
              fade_out_ms
              INTEGER
              NOT
              NULL
          );

          CREATE TABLE IF NOT EXISTS shortcuts
          (
              sort_order
              INTEGER
              PRIMARY
              KEY,
              id_name
              TEXT
              NOT
              NULL,
              width
              INTEGER
              NOT
              NULL,
              height
              INTEGER
              NOT
              NULL,
              text
              TEXT
              NOT
              NULL
              DEFAULT
              '',
              tooltip
              TEXT
              NOT
              NULL
              DEFAULT
              ''
          ); \
          """


@contextmanager
def _get_conn():
    """یک اتصال SQLite جدید باز می‌کند و در پایان بلوک with آن را می‌بندد."""
    if not _initialized:
        raise RuntimeError(
            "دیتابیس هنوز init نشده — ابتدا init_db() را در main.py صدا بزنید."
        )

    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """دیتابیس را یک‌بار مقداردهی اولیه می‌کند: پیداکردن/کپی‌کردن فایل configuration.db، ساخت جدول‌های گمشده و مهاجرت از data.json قدیمی."""
    global _initialized

    with _init_lock:
        if _initialized:
            return

        if not os.path.isfile(DB_PATH):
            if os.path.isfile(_LEGACY_DB_PATH):
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                shutil.copy2(_LEGACY_DB_PATH, DB_PATH)
            else:
                raise FileNotFoundError(
                    f"دیتابیس اصلی پیدا نشد:\n{DB_PATH}\n\n"
                    "فایل configuration.db باید همراه برنامه نصب شده باشد."
                )

        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.row_factory = sqlite3.Row

        try:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(_SCHEMA)
            _ensure_tavana_settings_schema(conn)
            conn.commit()
        finally:
            conn.close()

        _initialized = True
        # _migrate_from_legacy_json()


def _ensure_tavana_settings_schema(conn) -> None:
    """اگر جدول tavana_settings با ستون‌های قدیمی/ناقص روی دیسک باشد، آن را با نسخه‌ی درست از نو می‌سازد."""
    columns = {row["name"]
               for row in conn.execute("PRAGMA table_info(tavana_settings)")}
    required = {"id", "fade_in_ms", "fade_out_ms"}
    if not required.issubset(columns):
        conn.execute("DROP TABLE IF EXISTS tavana_settings")
        conn.execute(
            "CREATE TABLE tavana_settings ("
            "id INTEGER PRIMARY KEY CHECK (id = 0), "
            "fade_in_ms INTEGER NOT NULL, "
            "fade_out_ms INTEGER NOT NULL"
            ")"
        )


def get_app_info() -> dict[str, str]:
    """اطلاعات برنامه (نام فارسی، نام انگلیسی، نسخه) را برمی‌گرداند."""
    with _get_conn() as conn:
        rows = conn.execute("SELECT key, value FROM app_info").fetchall()
    return {row["key"]: row["value"] for row in rows}

def write_app_info(current_theme: str):
    with _get_conn() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO app_info (key, value, id) VALUES (?, ?, ?)",
            ("theme", current_theme, 6)
        )
        conn.commit()
def get_windows_commands() -> dict[str, dict[str, str]]:
    """نگاشت کلیدواژه‌های دستوری به نام تابع و نوع دستور را برمی‌گرداند."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT keyword, action, type FROM windows_command"
        ).fetchall()

    return {
        row["keyword"]: {
            "action": row["action"],
            "type": row["type"],
        }
        for row in rows
    }


def get_tavana_commands() -> dict[str, str]:
    """نگاشت کلیدواژه‌های دستوری به نام تابع مربوطه را برمی‌گرداند."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT keyword, action FROM tavana_command").fetchall()
    return {row["keyword"]: row["action"] for row in rows}


def get_shortcuts() -> list[tuple[str, int, int, str, str]]:
    """میانبرهای پایین پنجره را به همان ترتیب اصلی برمی‌گرداند."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT id_name, width, height, text, tooltip FROM shortcuts "
            "ORDER BY sort_order ASC"
        ).fetchall()

        conn.commit()
    return [(r["id_name"], r["width"], r["height"], r["text"], r["tooltip"]) for r in rows]

def get_animations() -> list[int]:
    """مدت‌زمان انیمیشن [fade_in_ms, fade_out_ms] را برمی‌گرداند؛ در نبود ردیف، مقادیر پیش‌فرض را می‌دهد."""
    try:
        with _get_conn() as conn:
            row = conn.execute(
                "SELECT fade_in_ms, fade_out_ms FROM tavana_settings WHERE id = 0"
            ).fetchone()
        if row:
            return [row["fade_in_ms"], row["fade_out_ms"]]
    except sqlite3.Error as e:
        print(f"خطا در خواندن تنظیمات انیمیشن: {e}")
    return list(DEFAULT_ANIMATION_SPEEDS)