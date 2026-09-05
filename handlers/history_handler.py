"""مدیریت تاریخچه‌ی متن‌های تایپ‌شده در نوار جستجو."""

from typing import Optional

from core.database import database


class HistoryManager:
    """خوانش/نوشتن تاریخچه‌ی تایپ‌شده در نوار جستجو با یک کش درون‌حافظه‌ای."""

    MAX_ITEMS = 2000

    def __init__(self):
        """کش داخلی تاریخچه را خالی مقداردهی می‌کند."""
        self._cache: Optional[list[tuple[str, str, str]]] = None

    def get_history_items(self) -> list[tuple[str, str, str]]:
        """آیتم‌های تاریخچه را به ترتیب جدیدترین تا قدیمی‌ترین برمی‌گرداند."""
        if self._cache is None:
            self._cache = database.get_type_history(self.MAX_ITEMS)
        return self._cache

    def add_to_history(self, text: str) -> None:
        """یک متن جدید را به تاریخچه اضافه می‌کند (آیتم تکراری فقط به بالا منتقل می‌شود)."""
        text = text.strip()
        if not text or len(text) < 2:
            return

        database.add_type_history(text, max_items=self.MAX_ITEMS)
        self._cache = None

    def clear_history(self) -> None:
        """کل تاریخچه را پاک می‌کند."""
        database.clear_type_history()
        self._cache = []
