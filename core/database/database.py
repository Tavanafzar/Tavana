"""لایه‌ی دسترسی به داده‌ها؛ تنها نقطه‌ی ورود به دیتابیس SQLite برنامه."""

import json
import os
import shutil
import sqlite3
import threading
import time
from contextlib import contextmanager
from core.paths.paths import app_path, resource_path

DB_PATH = app_path("data", "app.db")
_LEGACY_DB_PATH = resource_path("data", "app.db")
LEGACY_JSON_PATH = app_path("data", "data.json")
DEFAULT_HISTORY_LIMIT = 2000

DEFAULT_ANIMATION_SPEEDS = [200, 150]

_DEFAULT_LIGHT_ICON = resource_path("assets", "icons", "recently.png")
_DEFAULT_DARK_ICON = resource_path("assets", "icons", "recently.png")

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
          CREATE INDEX IF NOT EXISTS idx_type_history_created_at ON type_history(created_at DESC);

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
    """دیتابیس را یک‌بار مقداردهی اولیه می‌کند: پیداکردن/کپی‌کردن فایل app.db، ساخت جدول‌های گمشده و مهاجرت از data.json قدیمی."""
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
                    "فایل app.db باید همراه برنامه نصب شده باشد."
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
        _migrate_from_legacy_json()


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


def _migrate_from_legacy_json() -> None:
    """در صورت وجود data.json قدیمی و خالی‌بودن دیتابیس، یک‌بار داده‌ها را منتقل می‌کند."""
    if not os.path.exists(LEGACY_JSON_PATH):
        return

    with _get_conn() as conn:
        if conn.execute("SELECT 1 FROM app_info LIMIT 1").fetchone():
            return

        try:
            with open(LEGACY_JSON_PATH, "r", encoding="utf-8") as f:
                legacy = json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            print(f"Error reading legacy data.json during migration: {e}")
            return

        conn.executemany(
            "INSERT OR REPLACE INTO app_info (key, value) VALUES (?, ?)",
            list(legacy.get("App info", {}).items()),
        )
        conn.executemany(
            "INSERT OR REPLACE INTO windows_command (keyword, action) VALUES (?, ?)",
            list(legacy.get("Commands", {}).items()),
        )
        conn.executemany(
            "INSERT OR REPLACE INTO directories (filename, path) VALUES (?, ?)",
            list(legacy.get("Directories", {}).items()),
        )

        now = time.time()
        history_rows = []
        for index, item in enumerate(legacy.get("TypeHistories", [])):
            if not isinstance(item, list) or not item:
                continue
            text = item[0]
            light_icon = item[1] if len(item) > 1 else _DEFAULT_LIGHT_ICON
            dark_icon = item[2] if len(item) > 2 else _DEFAULT_DARK_ICON
            history_rows.append((text, light_icon, dark_icon, now - index))
        conn.executemany(
            "INSERT OR IGNORE INTO type_history (text, light_icon, dark_icon, created_at) "
            "VALUES (?, ?, ?, ?)",
            history_rows,
        )

        shortcut_rows = []
        for order, item in enumerate(legacy.get("Shortcuts", [])):
            shortcut_rows.append((
                order,
                item[0],
                item[1],
                item[2],
                item[3] if len(item) > 3 else "",
                item[4] if len(item) > 4 else "",
            ))
        conn.executemany(
            "INSERT OR REPLACE INTO shortcuts "
            "(sort_order, id_name, width, height, text, tooltip) VALUES (?, ?, ?, ?, ?, ?)",
            shortcut_rows,
        )

        conn.commit()
        print("✅ داده‌ها از data.json به data.db منتقل شدند")


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


def get_directories() -> dict[str, str]:
    """کش نام‌فایل → مسیر کامل را برمی‌گرداند."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT filename, path FROM directories").fetchall()
    return {row["filename"]: row["path"] for row in rows}


def save_directories(directories: dict[str, str]) -> None:
    """درج/به‌روزرسانی گروهی مسیرها (upsert) — فقط ردیف‌های داده‌شده نوشته می‌شوند."""
    if not directories:
        return
    with _get_conn() as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO directories (filename, path) VALUES (?, ?)",
            list(directories.items()),
        )
        conn.commit()


def get_type_history(limit: int = DEFAULT_HISTORY_LIMIT) -> list[tuple[str, str, str]]:
    """جدیدترین آیتم‌های تایپ‌شده را به ترتیب نزولی زمان برمی‌گرداند."""
    with _get_conn() as conn:
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
    """یک متن را به تاریخچه اضافه می‌کند؛ اگر تکراری باشد فقط زمانش را به‌روز می‌کند.

    در پایان، قدیمی‌ترین ردیف‌های بیش از سقف مجاز حذف می‌شوند.
    """
    with _get_conn() as conn:
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
    """کل تاریخچه‌ی تایپ را پاک می‌کند."""
    with _get_conn() as conn:
        conn.execute("DELETE FROM type_history")
        conn.commit()


def clear_directory_history() -> None:
    """کش مسیر همه‌ی فایل‌ها/برنامه‌های پیداشده را پاک می‌کند."""
    with _get_conn() as conn:
        conn.execute("DELETE FROM directories")
        conn.commit()


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
