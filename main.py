"""نقطه‌ی ورود اصلی برنامه‌ی توانا."""

import sys

from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from core.database import database
from core.paths.paths import resource_path
from core.single_instance.single_instance_manager import SingleInstanceGuard
from theme.system_theme import ThemeManager
from gui.pages.main_window import MainWindow
from handlers.font_handler import set_font
from theme.theme_loader import ThemeLoader
from core.hotkeys.hotkey_manager import HotkeyManager


def main() -> None:
    """دیتابیس، تم سیستم، پنجره‌ی اصلی و آیکون تری سیستم را راه‌اندازی و برنامه را اجرا می‌کند."""

    # QLocalSocket/QLocalServer برای کار درست نیاز به یک QCoreApplication دارند، پس
    # باید همین ابتدا ساخته شود؛ اما پیش از هر مقداردهی سنگین (دیتابیس، تم و ...)
    # بررسی می‌کنیم که آیا نمونه‌ی دیگری از برنامه در حال اجراست.
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    instance_guard = SingleInstanceGuard()
    if instance_guard.try_acquire():
        # نمونه‌ای از قبل در حال اجراست؛ به آن پیام دادیم که خودش را نشان دهد،
        # این نمونه‌ی جدید همین‌جا و بدون هیچ مقداردهی اضافه‌ای خارج می‌شود.
        sys.exit(0)

    database.init_db()

    theme_manager = ThemeManager()
    appearance = theme_manager.set_application_appearance()

    set_font(app, "Bold")
    window = MainWindow(appearance)
    window.setWindowTitle("توانا")

    instance_guard.show_requested.connect(window.toggle_visibility)

    icon_path = theme_manager.get_icon_path(appearance)
    window.setWindowIcon(QIcon(icon_path))

    tray_icon = setup_tray_icon(app, window, icon_path, appearance)
    register_hotkeys = HotkeyManager(window)
    register_hotkeys.hotkey_listener.start()
    
    register_hotkeys.return_the_answer_hotkey()
    
    exit_code = app.exec()
    register_hotkeys.hotkey_listener.stop()
    sys.exit(exit_code)


def setup_tray_icon(app, window, icon_path, is_dark):
    """آیکون و منوی تری سیستم (نمایش/خروج) را می‌سازد و برمی‌گرداند."""

    tray_icon = QSystemTrayIcon(
        QIcon(resource_path("assets", "icons", "shared_icons", "tavana.png")))
    tray_icon.setToolTip("Tavana")

    tray_menu = QMenu()
    # tray_menu.setWindowFlags(
    #     Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    # tray_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    # اکشن های منوی اصلی

    show_action = tray_menu.addAction("نمایش")
    show_action.setShortcut("Ctrl+Space")
    show_action.triggered.connect(window.toggle_visibility)

    exit_action = tray_menu.addAction("خروج")
    exit_action.triggered.connect(app.quit)

    tray_icon.setContextMenu(tray_menu)

    tray_menu.setStyleSheet(ThemeLoader.tray_menu_style())

    tray_icon.show()

    return tray_icon, tray_menu


if __name__ == "__main__":
    main()