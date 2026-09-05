"""مدیریت پاپ‌آپ‌های راهنما و اتصال آن‌ها به رابط کاربری."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from PySide6.QtCore import QEasingCurve, QPoint, QPropertyAnimation, QTimer
from PySide6.QtWidgets import QApplication


class PopupPosition(Enum):
    """موقعیت‌های ممکن برای نمایش پاپ‌آپ نسبت به ویجت هدف."""
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    CURSOR = "cursor"


@dataclass
class PopupConfig:
    """تنظیمات یک پاپ‌آپ: متن، موقعیت، مدت نمایش و مدت انیمیشن."""
    text: str
    position: PopupPosition = PopupPosition.BOTTOM_CENTER
    duration: int = 3500
    offset_x: int = 0
    offset_y: int = 8
    animation_duration: int = 200


class PopupManager:
    """نمایش، جای‌گذاری و پنهان‌کردن پاپ‌آپ با انیمیشن محو تدریجی."""

    def __init__(self, main_window):
        """مدیر پاپ‌آپ را با ارجاع به پنجره‌ی اصلی و تایمر مخفی‌سازی مقداردهی اولیه می‌کند."""
        self.main_window = main_window
        self.current_animation: Optional[QPropertyAnimation] = None
        self.hide_timer = QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(
            self._animate_hide)
        self.is_showing = False

    def calculate_position(self, widget, popup_width: int, popup_height: int,
                           config: PopupConfig) -> QPoint:
        """موقعیت نمایش پاپ‌آپ را متناسب با ویجت هدف و مرزهای صفحه‌نمایش محاسبه می‌کند."""
        if config.position == PopupPosition.CURSOR:
            cursor_pos = self.main_window.mapFromGlobal(
                QApplication.primaryScreen().cursor().pos()
            )
            return QPoint(
                cursor_pos.x() - popup_width // 2,
                cursor_pos.y() + 20
            )

        widget_rect = widget.rect()
        widget_top_left = widget.mapToGlobal(widget_rect.topLeft())

        position_configs = {
            PopupPosition.BOTTOM_CENTER: (
                widget_top_left.x() + widget.width() // 2 - popup_width // 2,
                widget_top_left.y() + widget.height()
            ),
            PopupPosition.BOTTOM_LEFT: (
                widget_top_left.x(),
                widget_top_left.y() + widget.height()
            ),
            PopupPosition.BOTTOM_RIGHT: (
                widget_top_left.x() + widget.width() - popup_width,
                widget_top_left.y() + widget.height()
            ),
            PopupPosition.TOP_CENTER: (
                widget_top_left.x() + widget.width() // 2 - popup_width // 2,
                widget_top_left.y() - popup_height
            ),
            PopupPosition.TOP_LEFT: (
                widget_top_left.x(),
                widget_top_left.y() - popup_height
            ),
            PopupPosition.TOP_RIGHT: (
                widget_top_left.x() + widget.width() - popup_width,
                widget_top_left.y() - popup_height
            ),
        }

        x, y = position_configs.get(
            config.position, (widget_top_left.x(), widget_top_left.y() + widget.height()))

        x += config.offset_x
        y += config.offset_y

        screen = self.main_window.screen().availableGeometry()
        x = max(5, min(x, screen.width() - popup_width - 5))
        y = max(5, min(y, screen.height() - popup_height - 5))

        return QPoint(x, y)

    def show_popup(self, widget, text: str, config: Optional[PopupConfig] = None):
        """پاپ‌آپ را با متن و تنظیمات داده‌شده، همراه با انیمیشن ظاهرشدن، نمایش می‌دهد."""
        if not widget or not widget.isVisible():
            return

        if config is None:
            config = PopupConfig(text=text)
        else:
            config = PopupConfig(
                text=text,
                position=config.position,
                duration=config.duration,
                offset_x=config.offset_x,
                offset_y=config.offset_y,
                animation_duration=config.animation_duration
            )

        self._stop_current_animations()

        self.main_window.popup.set_text(config.text)
        self.main_window.popup.adjustSize()

        popup_pos = self.calculate_position(
            widget,
            self.main_window.popup.width(),
            self.main_window.popup.height(),
            config
        )

        if self.main_window.popup.isVisible():
            self.main_window.popup.hide()

        self.main_window.popup.move(popup_pos)
        self.main_window.popup.setWindowOpacity(0.0)
        self.main_window.popup.show()

        self._animate_show(config.animation_duration)
        self.is_showing = True

        total_duration = config.duration + config.animation_duration
        self.hide_timer.start(total_duration)

    def _animate_show(self, duration: int = 200):
        """پاپ‌آپ را با انیمیشن محو تدریجی (fade-in) نمایان می‌کند."""
        if self.current_animation:
            self.current_animation.stop()

        self.current_animation = QPropertyAnimation(
            self.main_window.popup, b"windowOpacity")
        self.current_animation.setDuration(duration)
        self.current_animation.setStartValue(0.0)
        self.current_animation.setEndValue(1.0)
        self.current_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.current_animation.start()

    def _animate_hide(self, duration: int = 150):
        """پاپ‌آپ را با انیمیشن محو تدریجی (fade-out) پنهان می‌کند."""
        if self.current_animation:
            self.current_animation.stop()

        self.current_animation = QPropertyAnimation(
            self.main_window.popup, b"windowOpacity")
        self.current_animation.setDuration(duration)
        self.current_animation.setStartValue(1.0)
        self.current_animation.setEndValue(0.0)
        self.current_animation.setEasingCurve(QEasingCurve.Type.InCubic)
        self.current_animation.finished.connect(self._on_hide_finished)
        self.current_animation.start()

    def _on_hide_finished(self):
        """پس از پایان انیمیشن پنهان‌سازی، پاپ‌آپ را واقعاً مخفی و وضعیت را بازنشانی می‌کند."""
        self.main_window.popup.hide()
        self.main_window.popup.setWindowOpacity(1.0)
        self.is_showing = False
        self.current_animation = None

    def _stop_current_animations(self):
        """انیمیشن و تایمر فعلیِ در حال اجرا را متوقف می‌کند."""
        if self.current_animation:
            self.current_animation.stop()
            self.current_animation = None
        if self.hide_timer and self.hide_timer.isActive():
            self.hide_timer.stop()

    def hide_immediately(self):
        """پاپ‌آپ را بدون انیمیشن و بلافاصله پنهان می‌کند."""
        self._stop_current_animations()
        self.main_window.popup.hide()
        self.is_showing = False


def setup_ui_hooks(main_window):
    """مدیر پاپ‌آپ را می‌سازد، پاپ‌آپ‌های راهنما را متصل می‌کند و پاپ‌آپ را برای اولین نمایش گرم می‌کند."""
    main_window.popup_manager = PopupManager(main_window)
    setup_advanced_popups(main_window)
    _warm_up_popup(main_window)


def _warm_up_popup(main_window):
    """پاپ‌آپ را یک‌بار نامرئی نمایش/مخفی می‌کند تا هزینه‌ی اولین رندر واقعی حذف شود."""
    popup = main_window.popup
    popup.set_text(" ")
    popup.setWindowOpacity(0.0)
    popup.show()
    QTimer.singleShot(0, popup.hide)


def setup_advanced_popups(main_window):
    """متن راهنمای هر دکمه‌ی رادیویی را تعریف و کلیک آن را به نمایش پاپ‌آپ متصل می‌کند."""
    popup_configs = {

        main_window.ui.cmdRadioButton: PopupConfig(
            text="""💻 فرمان های ویندوز و خط فرمان

✨ قابلیت‌ها:
• اجرای فرمان های منوی اجرایی (Run)
• اجرای فرمان های خط فرمان (CMD)
• دسترسی سریع به ابزارهای سیستمی

📝 مثال‌ها:
• ncpa.cpl یا تنظیمات شبکه
• control یا کنترل پنل
• taskmgr یا مدیریت وظایف
• cmd یا خط فرمان
• calc یا ماشین حساب
""",
            position=PopupPosition.BOTTOM_CENTER,
            duration=8000
        ),

        main_window.ui.runProgramRadioButton: PopupConfig(
            text="""🚀 اجرای و پیدا کردن سریع برنامه ها

✨ قابلیت‌ها:
• جستجوی هوشمند فایل‌های .exe و .lnk و .url
• اجرای برنامه‌های نصب شده روی سیستم
• حافظه کش برای اجرای سریع‌تر دفعات بعد

📝 روش استفاده:
نام دقیق فایل برنامه را با رعایت حروف بزرگ و کوچک بنویسید

✅ مثال‌های موفق:
• "PowerISO.exe" - اجرای پاورایزو
• "Telegram.exe" - اجرای تلگرام

💡 نکات مهم:
• برنامه باید در مسیرهای سیستمی یا دسکتاپ باشد
• از نوشتن مسیر کامل خودداری کنید
""",
            position=PopupPosition.BOTTOM_CENTER,
            duration=20000,
            offset_y=10
        ),
        main_window.ui.mathRadioButton: PopupConfig(
            text="""🧮 ماشین حساب پیشرفته

➕➖ جمع و تفریق:
 45 = 15+30
 55 = 45-100

✖️➗ ضرب و تقسیم:
 100 = 25x4
100÷4 = 25

🔢 توان و رادیکال:
• 8 = 3^2 (2 به توان 3)
• sqrt(16) = 4 (جذر 16)

📐 توابع مثلثاتی:
• sin(30) = 0.5 و ...
""",
            position=PopupPosition.BOTTOM_CENTER,
            duration=9000
        ),
        main_window.ui.webRadioButton: PopupConfig(
            text="""🌐 جستجوی در گوگل

✨ قابلیت‌ها:
• جستجوی هوشمند در موتور جستجوی گوگل
• باز کردن مستقیم وب‌سایت‌ها
• پشتیبانی از آدرس‌های اینترنتی

📝 روش استفاده:

✅ جستجوی ساده:
• "طراحی وب"
• "آموزش پایتون"
• "اخبار روز دنیا"

✅ باز کردن مستقیم وب‌سایت:
• youtube.com یا
• www.youtube.com یا
• https://www.youtube.com
""",
            position=PopupPosition.BOTTOM_CENTER,
            duration=6000
        ),
        main_window.ui.voiceBtn: PopupConfig(
            text="توانایی گفتار به متن در دست توسعه است.",
            position=PopupPosition.BOTTOM_CENTER,
            duration=8000
        ),
    }
    for button, config in popup_configs.items():
        if button:
            button.clicked.connect(
                lambda checked, btn=button, cfg=config:
                show_popup_safe(main_window, btn, cfg)
            )


def show_popup_safe(main_window, widget, config: PopupConfig):
    """پاپ‌آپ را با مدیریت خطا نمایش می‌دهد تا خطای احتمالی برنامه را متوقف نکند."""

    try:
        if hasattr(main_window, 'popup_manager') and main_window.popup_manager:
            main_window.popup_manager.show_popup(widget, config.text, config)
    except Exception as e:
        print(f"Error showing popup: {e}")
