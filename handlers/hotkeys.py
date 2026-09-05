import win32con
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import QApplication

from core.hotkeys.hotkey_manager import HotkeyManager

hotkey_manager = None


def register_hotkeys(window):
    """میان‌بر سراسری Ctrl+Space (نمایش/پنهان‌کردن پنجره) و کلید Enter (ارسال) را برای پنجره‌ی اصلی ثبت می‌کند."""
    global hotkey_manager

    hotkey_manager = HotkeyManager()

    hotkey_manager.add_hotkey(
        1,
        win32con.VK_SPACE,
        win32con.MOD_CONTROL,
        lambda: window.toggle_signal.emit()
    )

    submit_answer = QShortcut(QKeySequence("Return"), window)
    submit_answer.activated.connect(window.submit_signal.emit)

    window.ui.submitBtn.clicked.connect(window.submit_signal.emit)

    hotkey_manager.install(
        QApplication.instance()
    )
