"""ویجت پاپ‌آپ نمایش اعلان‌های کوتاه به کاربر."""

from PySide6.QtCore import Qt, QPropertyAnimation, QTimer
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from theme.theme_loader import ThemeLoader


class PopupWidget(QWidget):
    """پاپ‌آپ بدون‌فریم و شفاف برای نمایش پیام‌های اعلان."""

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # تنظیمات پایه‌ای پنجره
        self.setWindowFlags(
            Qt.WindowType.Popup | 
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Showing a tooltip-like popup must not steal focus from the radio button.
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setContentsMargins(0, 0, 0, 0) # حذف حاشیه‌های پیش‌فرض ویجت

        # ساخت لیبل و چیدمان (یکپارچه و بدون توابع اضافی)
        self.notification = QLabel(self)
        #self.notification.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.notification)

        # تنظیم انیمیشن Fade-in برای روانی اجرا
        self._fade_animation = QPropertyAnimation(self, b"windowOpacity")
        self._fade_animation.setDuration(150) # 150 میلی‌ثانیه بسیار روان است
        self._fade_animation.setStartValue(0.0)
        self._fade_animation.setEndValue(1.0)

        # تایمر برای بسته شدن خودکار پاپ‌آپ
        self._auto_hide_timer = QTimer(self)
        self._auto_hide_timer.setSingleShot(True)
        self._auto_hide_timer.timeout.connect(self.close)

    def set_text(self, text: str) -> None:
        """متن پاپ‌آپ را تنظیم و اندازه‌ی آن را دقیق محاسبه می‌کند."""
        self.notification.setText(text)
        self.adjustSize()  # کلید روانی: جلوگیری از پرش سایز هنگام اولین نمایش

    def show_popup(self, position: Qt.GlobalPosition, duration_ms: int = 1500) -> None: # type: ignore
        """
        پاپ‌آپ را در موقعیت مکان‌نما با انیمیشن نمایش داده و بعد از مدتی می‌بندد.
        """
        # محاسبه موقعیت دقیق زیر مکان‌نما
        cursor_pos = self.cursor().pos()
        self.move(cursor_pos.x(), cursor_pos.y() + 20)
        
        self._fade_animation.start()
        self.show()
        self._auto_hide_timer.start(duration_ms)

    def update_theme(self) -> None:
        """استایل و سایه‌ی پاپ‌آپ را متناسب با تم فعلی به‌روزرسانی می‌کند."""
        ThemeLoader.graphic_shadow([self.notification])
        notif_qss, widget_qss = ThemeLoader.popup_style()
        
        # اعمال استایل فقط در صورت تغییر (جلوگیری از رندر مجدد بی‌دلیل)
        if self.notification.styleSheet() != notif_qss:
            self.notification.setStyleSheet(notif_qss)
        if self.styleSheet() != widget_qss:
            self.setStyleSheet(widget_qss)