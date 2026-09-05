"""نقطه‌ی مرکزی resolve کردن مسیرهای برنامه (به‌جای هاردکدکردن مسیر نسبی در هر ماژول)."""

import os
import sys


def _detect_app_dir() -> str:
    """پوشه‌ی فایل‌های قابل‌نوشتن (دیتابیس، کش آیکون‌ها) را تشخیص می‌دهد: کنار exe یا ریشه‌ی پروژه."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _detect_resource_dir() -> str:
    """پوشه‌ی دارایی‌های فقط-خواندنیِ باندل‌شده را تشخیص می‌دهد (در حالت onefile، پوشه‌ی موقت PyInstaller)."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return meipass
    return APP_DIR


APP_DIR = _detect_app_dir()
RESOURCE_DIR = _detect_resource_dir()


def app_path(*parts: str) -> str:
    """مسیر مطلق برای فایل‌های قابل‌نوشتن (دیتابیس، کش آیکون‌های برنامه‌ها)."""
    return os.path.join(APP_DIR, *parts)


def resource_path(*parts: str) -> str:
    """مسیر مطلق برای دارایی‌های فقط-خواندنی (آیکون‌ها، فونت‌ها، es.exe)."""
    return os.path.join(RESOURCE_DIR, *parts)


PROGRAM_ICONS_DIR = app_path("data", "program_icons")
