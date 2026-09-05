from core.paths.paths import resource_path
from PySide6.QtGui import QFont, QFontDatabase


_FONT_IDS = {}


def set_font(widget, weight, size=11):
    """بارگذاری فونت Sahel فقط یک‌بار و اعمال آن روی ویجت."""
    key = weight
    font_id = _FONT_IDS.get(key)

    if font_id is None:
        font_path = resource_path(
            "fonts",
            "Sahel",
            f"Sahel-{weight}-FD.ttf"
        )
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id == -1:
            print(f"فونت Sahel-{weight}-FD بارگذاری نشد! از فونت پیش‌فرض سیستم استفاده می‌شود.")
            font = widget.font()
        else:
            _FONT_IDS[key] = font_id
            families = QFontDatabase.applicationFontFamilies(font_id)
            family = families[0] if families else widget.font().family()
            font = QFont(family)
    else:
        families = QFontDatabase.applicationFontFamilies(font_id)
        family = families[0] if families else widget.font().family()
        font = QFont(family)

    font.setPointSize(size)
    widget.setFont(font)
