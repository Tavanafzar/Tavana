"""تشخیص و بازکردن آدرس‌های اینترنتی."""
import re
import webbrowser


def is_url(text: str) -> bool:
    """تشخیص می‌دهد آیا متن یک آدرس اینترنتی معتبر است یا نه."""
    pattern = r"^(https?://)?[A-Za-z0-9\-]+\.[A-Za-z]{2,}"
    return bool(re.match(pattern, text))


def open_url(text: str) -> None:
    """آدرس داده‌شده را در مرورگر پیش‌فرض سیستم باز می‌کند."""
    if not text.startswith("http"):
        text = "https://" + text
    webbrowser.open_new(text)
