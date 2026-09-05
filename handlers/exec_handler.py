"""اجرای فایل‌های اجرایی/میانبر با استفاده از FileFinder."""
from core.file_search.file_finder import FileFinder

finder = FileFinder()

finder.file_found.connect(finder.open_that_path)
finder.file_not_found.connect(lambda: print("پیدا نشد"))


def update_installed_programs() -> None:
    """منوی Start ویندوز را دوباره اسکن می‌کند تا برنامه‌های نصب‌شده‌ی جدید به کش اضافه شوند."""
    finder.scan_start_menu_programs()


def is_executable(text: str) -> bool:
    """تشخیص می‌دهد آیا متن به یک فایل اجرایی/میانبر (exe، lnk، url) اشاره دارد یا نه."""

    return text.lower().endswith((".exe", ".lnk", ".url"))


def run_executable(filename: str) -> bool:
    """جستجوی ناهمگام فایل اجرایی/میانبر را شروع می‌کند؛ اگر جستجوی دیگری در حال اجرا باشد، نادیده گرفته و False برمی‌گرداند."""
    return finder.find_file_async(filename)
