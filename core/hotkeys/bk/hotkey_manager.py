"""ثبت و مدیریت میان‌برهای صفحه‌کلید سراسری ویندوز (global hotkey)."""

import ctypes
from ctypes import wintypes

import win32con
from PySide6.QtCore import QAbstractNativeEventFilter, QObject


class HotkeyEventFilter(QAbstractNativeEventFilter):
    """پیام‌های خام ویندوز را رهگیری می‌کند و رویداد WM_HOTKEY را به اکشن ثبت‌شده‌ی مربوطه می‌رساند."""

    def __init__(self, manager):
        """فیلتر رویداد را با مدیر میان‌برها (HotkeyManager) مرتبط می‌کند."""
        super().__init__()
        self.manager = manager

    def nativeEventFilter(self, eventType, message):
        """هر پیام خام ویندوز را بررسی می‌کند و در صورت تطبیق با WM_HOTKEY، کال‌بک مربوطه را اجرا می‌کند."""

        if eventType == "windows_generic_MSG":

            msg = wintypes.MSG.from_address(
                int(message)
            )

            if msg.message == win32con.WM_HOTKEY:

                callback = self.manager.actions.get(
                    msg.wParam
                )

                if callback:
                    callback()

        return False, 0


class HotkeyManager(QObject):
    """ثبت، نصب و لغو میان‌برهای صفحه‌کلید سراسری ویندوز از طریق RegisterHotKey."""

    def __init__(self):
        """نگاشت میان‌برها/اکشن‌ها و فیلتر رویداد را مقداردهی اولیه می‌کند."""
        super().__init__()

        self.user32 = ctypes.windll.user32

        self.hotkeys = {}
        self.actions = {}

        self.event_filter = HotkeyEventFilter(self)

    def add_hotkey(
            self,
            hotkey_id,
            key,
            modifiers,
            callback
    ):
        """یک میان‌بر سراسری جدید را نزد ویندوز ثبت و کال‌بک اجرای آن را ذخیره می‌کند."""

        result = self.user32.RegisterHotKey(
            None,
            hotkey_id,
            modifiers,
            key
        )

        if not result:
            raise RuntimeError(
                f"Cannot register hotkey {hotkey_id}"
            )

        self.hotkeys[hotkey_id] = True
        self.actions[hotkey_id] = callback

    def install(self, app):
        """فیلتر رویداد را روی نمونه‌ی QApplication نصب می‌کند تا پیام‌های ویندوز رهگیری شوند."""

        app.installNativeEventFilter(
            self.event_filter
        )

    def remove_all(self):
        """تمام میان‌برهای ثبت‌شده را نزد ویندوز لغو و نگاشت داخلی را پاک می‌کند."""

        for hotkey_id in self.hotkeys:
            self.user32.UnregisterHotKey(
                None,
                hotkey_id
            )

        self.hotkeys.clear()
        self.actions.clear()
