"""نقطه‌ی ورود اصلی برنامه‌ی توانا."""

import sys

from PySide6.QtGui import QActionGroup, QIcon, Qt
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from core.database import database
from core.paths.paths import resource_path
from theme.system_theme import ThemeManager
from gui.pages.main_window import MainWindow
from gui.pages.popup import PopupWidget
from handlers.font_handler import set_font
from theme.theme_loader import ThemeLoader


def main() -> None:
    """دیتابیس، تم سیستم، پنجره‌ی اصلی و آیکون تری سیستم را راه‌اندازی و برنامه را اجرا می‌کند."""

    database.init_db()

    theme_manager = ThemeManager()
    appearance = theme_manager.set_application_appearance()

    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

    set_font(app, "Bold")
    window = MainWindow(appearance)
    window.setWindowTitle("توانا")

    icon_path = theme_manager.get_icon_path(appearance)
    window.setWindowIcon(QIcon(icon_path))

    tray_icon = setup_tray_icon(app, window, icon_path, appearance)

    sys.exit(app.exec())


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
