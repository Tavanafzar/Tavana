

"""پنجره‌ی اصلی برنامه: نوار جستجو، تشخیص نوع ورودی، دستورات و تم."""

import ctypes
import os
import subprocess
import sys
import threading
import webbrowser

from PySide6.QtCore import QFileInfo, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QCompleter, QFileIconProvider, QListView, QMainWindow

from core.calculations.math_engine import evaluate_math_expression, is_math_expression
from core.commands.commands import load_tavana_commands, load_windows_commands
from core.database import database
from core.paths.paths import PROGRAM_ICONS_DIR, resource_path
from core.utils.search_providers import handle_search_prefix
from core.utils.text_utils import normalize_text
from gui.animation.animations import widget_slide_fade_in, widget_slide_fade_out, window_fade_in, window_fade_out
from gui.pages.design import Ui_MainWindow
from gui.pages.popup import PopupWidget
from gui.pages.ui_hooks import setup_ui_hooks
from handlers.exec_handler import (
    is_executable,
    run_executable,
    update_installed_programs,
)
from handlers.font_handler import set_font
from handlers.history_handler import HistoryManager
from handlers.hotkeys import register_hotkeys
from handlers.url_handler import is_url, open_url
from theme.blur_window import enable_blur
from theme.theme_loader import ThemeLoader


class MainWindow(QMainWindow):
    """پنجره‌ی اصلی توانا؛ نوار جستجو را مدیریت و ورودی کاربر را به دستور/جستجو/محاسبه تبدیل می‌کند."""

    toggle_signal = Signal()
    submit_signal = Signal()
    icons_ready = Signal()
    programs_updated = Signal()

    PROGRAM_ICONS_DIR = PROGRAM_ICONS_DIR
    DEFAULT_PROGRAM_ICON = resource_path(
        "assets", "icons", "light", "searchInDir.png")

    def __init__(self, is_dark_theme: bool):
        """رابط کاربری، دستورات، انیمیشن‌ها و داده‌های اولیه را می‌سازد و اسکن پس‌زمینه‌ی برنامه‌ها را شروع می‌کند."""
        super().__init__()

        self.is_dark_theme = is_dark_theme
        self._suggestions_cache = None
        self._icon_cache = {}
        self._program_display_map = {}
        self._auto_complete_model = None
        self._animations = []
        self.after_command_hide_delay = 40
        self._icon_provider = QFileIconProvider()

        self.history_manager = HistoryManager()

        self._setup_ui()
        self._setup_window_properties()
        self._setup_commands()
        self._setup_animations()
        self._setup_signals()
        self.radio_button_direct_to_web_service()
        self._load_initial_data()

        self.icons_ready.connect(
            lambda: self._setup_autocomplete(force_reload=True))
        self.programs_updated.connect(
            lambda: self._setup_autocomplete(force_reload=True)
        )
        QTimer.singleShot(0, self._scan_installed_programs_async)

        QTimer.singleShot(0, self._backfill_program_icons_async)

    def _scan_installed_programs_async(self):
        """اسکن منوی Start برای برنامه‌های نصب‌شده را در یک ترد جداگانه اجرا می‌کند."""
        def worker():
            """اسکن برنامه‌های نصب‌شده را اجرا و رویداد به‌روزرسانی را ارسال می‌کند."""
            update_installed_programs()
            self.programs_updated.emit()

        threading.Thread(target=worker, daemon=True).start()

    def _program_icon_path(self, filename: str):
        """اگر آیکون اختصاصیِ از قبل استخراج‌شده‌ی این برنامه وجود داشته باشد، مسیرش را برمی‌گرداند."""
        icon_file = os.path.join(
            self.PROGRAM_ICONS_DIR, os.path.splitext(filename)[0] + ".png")
        return icon_file if os.path.isfile(icon_file) else None

    def _backfill_program_icons_async(self):
        """به‌جای اجرا در threading.Thread، روی خود ترد GUI ولی chunk‌شده اجرا می‌شود
        چون QIcon/QPixmap thread-safe نیستند و اجرای آن‌ها در ترد جدا باعث
        رقابت با رندر UI (از جمله پاپ‌آپ‌ها) در همان بازه‌ی زمانی می‌شود."""
        try:
            os.makedirs(self.PROGRAM_ICONS_DIR, exist_ok=True)
            self._icon_backfill_queue = list(
                database.get_directories().items())
        except Exception as e:
            print(f"خطا در آماده‌سازی صف بک‌فیل آیکون‌ها: {e}")
            return
        QTimer.singleShot(50, self._backfill_next_icon_chunk)

    def _backfill_next_icon_chunk(self, chunk_size: int = 15):
        """یک دسته از آیکون‌های استخراج‌نشده را پردازش می‌کند و ادامه‌ی صف را در فراخوانی بعدی زمان‌بندی می‌کند."""
        extracted_any = False
        for _ in range(chunk_size):
            if not self._icon_backfill_queue:
                if extracted_any:
                    self.icons_ready.emit()
                return
            filename, filepath = self._icon_backfill_queue.pop(0)
            icon_file = os.path.join(
                self.PROGRAM_ICONS_DIR, os.path.splitext(filename)[0] + ".png")
            if os.path.isfile(icon_file) or not os.path.isfile(filepath):
                continue
            try:
                icon = self._icon_provider.icon(QFileInfo(filepath))
                if not icon.isNull() and icon.pixmap(256, 256).save(icon_file):
                    extracted_any = True
            except Exception as e:
                print(f"خطا در استخراج آیکون '{filepath}': {e}")

        if extracted_any:
            self.icons_ready.emit()
        QTimer.singleShot(0, self._backfill_next_icon_chunk)

    def _setup_ui(self):
        """فایل طراحی رابط کاربری را بارگذاری می‌کند و بلور، پاپ‌آپ و هوک‌های رابط کاربری را راه‌اندازی می‌کند."""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        hwnd = int(self.winId())
        enable_blur(hwnd)

        self.popup = PopupWidget(self)

        setup_ui_hooks(self)

    def _setup_window_properties(self):
        """پرچم‌های پنجره (بدون‌فریم، همیشه‌بالا، شفاف) را تنظیم می‌کند."""
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysStackOnTop)

    def _setup_commands(self):
        """نگاشت دستورات ویندوز و دستورات اختصاصی توانا را از دیتابیس بارگذاری می‌کند."""
        self.windows_command = load_windows_commands()
        self.tavana_command = load_tavana_commands()

    def _setup_animations(self):
        """تم فعلی را روی رابط کاربری اعمال می‌کند."""
        ThemeLoader.apply_theme(self, self.ui)
        self.popup.update_theme() 
        
    def _setup_signals(self):
        """سیگنال‌های نمایش/ارسال/تغییر تم/تغییر متن را به متدهای مربوطه متصل می‌کند."""
        self.toggle_signal.connect(self.toggle_visibility)
        self.submit_signal.connect(self.process_input)
        
        self.ui.logoButton.clicked.connect(self.refresh_theme)

        self.ui.searchBox.textChanged.connect(self.custom_text_changed)

    def _load_initial_data(self):
        """میان‌برهای صفحه‌کلید را ثبت و لیست پیشنهادهای خودکار را بارگذاری می‌کند."""
        register_hotkeys(self)
        self._setup_autocomplete()

    def _setup_autocomplete(self, force_reload: bool = False):
        """مدل پیشنهادهای خودکار (دستورات، برنامه‌ها و تاریخچه) را می‌سازد یا در صورت نیاز از نو بارگذاری می‌کند."""
        if self._suggestions_cache is None or force_reload:
            self._suggestions_cache = []
            self._program_display_map.clear()

            suggestions_data = self._load_suggestions()
            history_items = self.history_manager.get_history_items()

            self._suggestions_cache.extend(suggestions_data)
            self._suggestions_cache.extend(history_items[:600])

        if self._auto_complete_model is not None:
            self._auto_complete_model.clear()
        else:
            self._auto_complete_model = QStandardItemModel()

        for suggestion in self._suggestions_cache:
            text = suggestion[0]
            dark_icon = suggestion[1]
            light_icon = suggestion[2]

            icon_path = dark_icon if self.is_dark_theme else light_icon

            if icon_path not in self._icon_cache:
                try:
                    self._icon_cache[icon_path] = QIcon(icon_path)
                except Exception:
                    self._icon_cache[icon_path] = QIcon()

            item = QStandardItem(text)
            item.setIcon(self._icon_cache[icon_path])
            self._auto_complete_model.appendRow(item)

        self.list_view = QListView()
        self.list_view.setIconSize(QSize(22, 22))
        self.list_view.setObjectName("list_view")

        self.list_view.setModel(self._auto_complete_model)
        self.list_view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.list_view.setStyleSheet(self._get_autocomplete_style())

        completer = QCompleter()
        completer.setModel(self._auto_complete_model)
        completer.setPopup(self.list_view)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseSensitive)
        completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.ui.searchBox.setCompleter(completer)

    def _load_suggestions(self) -> list:
        """دستورات ویندوز، دستورات توانا و برنامه‌های شناخته‌شده را
        برای نمایش در پیشنهادهای خودکار آماده می‌کند.
        """
        suggestions = []

        try:
            windows_cmd_dark = resource_path(
                "assets", "icons", "shared_icons", "run-command.png"
            )
            windows_cmd_light = resource_path(
                "assets", "icons", "shared_icons", "run-command.png"
            )

            tavana_cmd_dark = resource_path(
                "assets", "icons", "shared_icons", "tavana.png"
            )
            tavana_cmd_light = resource_path(
                "assets", "icons", "shared_icons", "tavana.png"
            )

            # Windows commands
            windows_commands = database.get_windows_commands()

            for cmd_key, command_data in windows_commands.items():
                command_type = command_data["type"]
                if command_type == "human":
                    suggestions.append([
                        cmd_key,
                        windows_cmd_dark,
                        windows_cmd_light,
                        command_type,
                    ])

            # Tavana commands
            for cmd_key in database.get_tavana_commands().keys():
                suggestions.append([
                    cmd_key,
                    tavana_cmd_dark,
                    tavana_cmd_light,
                    "tavana",
                ])

                # Programs / directories
            for dir_key in database.get_directories().keys():
                display_name = dir_key

                # Hide only executable extensions in the UI.
                # Keep the original database key for execution.
                if dir_key.lower().endswith((".lnk", ".exe")):
                    display_name = os.path.splitext(dir_key)[0]

                self._program_display_map[display_name.lower()] = dir_key

                program_icon = self._program_icon_path(dir_key)
                icon_path = program_icon or self.DEFAULT_PROGRAM_ICON

                suggestions.append([
                    display_name,
                    icon_path,
                    icon_path,
                    "program",
                ])

            return suggestions[:600]

        except Exception as e:
            print(f"Error loading suggestions from database: {e}")
            return []

    def _get_autocomplete_style(self) -> str:
        """استایل‌شیت لیست پیشنهادهای خودکار را متناسب با تم فعلی برمی‌گرداند."""
        return ThemeLoader.autocomplete_style()

    def toggle_visibility(self):
        """پنجره را با انیمیشن نمایش می‌دهد یا پنهان می‌کند و آن را در حالت نمایش، بالاترین پنجره قرار می‌دهد."""
        try:
            if self.isVisible():

                window_fade_out(self, self.hide)

                widget_slide_fade_out(self.ui.searchFrame, "bottom")
                widget_slide_fade_out(self.ui.logoButton, "bottom")

                self.ui.animate_shortcut_buttons_slide_fade_out()
            else:
                self.showFullScreen()
                self.raise_()
                self.activateWindow()

                hwnd = int(self.winId())

                HWND_TOPMOST = -1
                SWP_NOSIZE = 0x0001
                SWP_NOMOVE = 0x0002
                SWP_SHOWWINDOW = 0x0040

                ctypes.windll.user32.SetWindowPos(
                    hwnd,
                    HWND_TOPMOST,
                    0, 0, 0, 0,
                    SWP_NOMOVE |
                    SWP_NOSIZE |
                    SWP_SHOWWINDOW
                )
                window_fade_in(self)

                widget_slide_fade_in(self.ui.searchFrame, "bottom")
                widget_slide_fade_in(self.ui.logoButton, "bottom")

                self.ui.animate_shortcut_buttons_slide_fade_in()

        except Exception as e:
            print(f"Error in toggle_visibility: {e}")
            self.setVisible(not self.isVisible())

    def process_input(self):
        """متن نوار جستجو را می‌خواند و بسته به نوعش (دستور، پیشوند جستجو، فایل اجرایی، URL، عبارت ریاضی یا جستجوی وب) پردازش می‌کند."""
        text = self.ui.searchBox.text().strip()

        if not self.isVisible() or not text:
            return
        command_key = text.lower()
        if command_key in self.windows_command:
            result = self.windows_command[command_key]()
            QTimer.singleShot(self.after_command_hide_delay, self.reset_box)

            return

        if command_key in self.tavana_command:
            result = self.tavana_command[command_key]()
            QTimer.singleShot(self.after_command_hide_delay, self.reset_box)
            return

        # Program suggestions are shown without .exe/.lnk,
        # but the original database value is kept for execution.
        if command_key in self._program_display_map:
            executable = self._program_display_map[command_key]

            if run_executable(executable):
                QTimer.singleShot(
                    self.after_command_hide_delay, self.reset_box
                )
            return

        if handle_search_prefix(text):
            QTimer.singleShot(self.after_command_hide_delay, self.reset_box)

            return

        if is_executable(text):

            if run_executable(text):

                QTimer.singleShot(
                    self.after_command_hide_delay, self.reset_box)
            return

        if is_url(text):
            text = text.replace(
                "https://", "").replace("http://", "").replace("www.", "")
            QTimer.singleShot(self.after_command_hide_delay, self.reset_box)
            open_url(text)
            self.backup_history(text)
            return

        if is_math_expression(text):
            result = evaluate_math_expression(text)

            if isinstance(result, (int, float)) and not isinstance(result, bool):
                self.ui.searchBox.setText(f"{result:,}")
                self.backup_history(text)
            elif isinstance(result, str):
                self.ui.searchBox.setText(result)
            return

        try:
            self.search_on_web(text)
        except Exception as e:
            print(f"Error opening browser: {e}")

    def backup_history(self, text):
        """متن را با کمی تأخیر به تاریخچه اضافه می‌کند و لیست پیشنهادها را به‌روزرسانی می‌کند."""
        def _persist_and_refresh():
            """متن را در دیتابیس تاریخچه ذخیره و لیست پیشنهادها را به‌روزرسانی می‌کند."""
            self.history_manager.add_to_history(text)
            self.update_suggestions(text)

        QTimer.singleShot(200, _persist_and_refresh)

    def radio_button_direct_to_web_service(self):
        """کلیک روی هر دکمه‌ی رادیویی سرویس وب را به بازکردن آدرس همان سرویس متصل می‌کند."""
        urls = [
            "https://www.youtube.com/",
            "https://gemini.google.com/",
            "https://mail.google.com/",
            "https://translate.google.com/?sl=fa&tl=en&op=translate",
            "https://drive.google.com/"
        ]
        self.ui.youtubeRadioButton.clicked.connect(
            lambda: self.open_links(urls[0]))
        self.ui.gptRadioButton.clicked.connect(
            lambda: self.open_links(urls[1]))
        self.ui.gmailRadioButton.clicked.connect(
            lambda: self.open_links(urls[2]))
        self.ui.translateRadioButton.clicked.connect(
            lambda: self.open_links(urls[3]))
        self.ui.driveRadioButton.clicked.connect(
            lambda: self.open_links(urls[4]))

    def open_links(self, url):
        """پنجره را می‌بندد و آدرس داده‌شده را در مرورگر پیش‌فرض باز می‌کند."""
        try:
            self.reset_box()
            webbrowser.open(url)
        except Exception as e:
            print(f"Error opening URL: {e}")

    def search_on_web(self, text):
        webbrowser.open(f"https://google.com/search?q={text}")
        self.backup_history(text)
        QTimer.singleShot(self.after_command_hide_delay, self.reset_box)

    def custom_text_changed(self):
        """متن نوار جستجو را نرمال‌سازی می‌کند و نمایش/عدم‌نمایش نشانگر نوع ورودی را به‌روزرسانی می‌کند."""

        text = self.ui.searchBox.text()
        normalized = normalize_text(text)

        if text != normalized:
            self.ui.searchBox.blockSignals(True)
            self.ui.searchBox.setText(normalized)
            self.ui.searchBox.blockSignals(False)
            return

        if text:
            self.ui.searchAreaLayout.setContentsMargins(12, 0, 8, 0)
            self.ui.input_mode_frame.setVisible(True)
            self.ui.input_mode.setVisible(True)
            self.ui.input_mode_text.setVisible(True)
            self.ui.submitBtn.setVisible(False)

        else:
            self.ui.searchAreaLayout.setContentsMargins(12, 0, 12, 0)
            
            self.ui.input_mode_frame.setVisible(False)
            self.ui.input_mode.setVisible(False)
            self.ui.input_mode_text.setVisible(False)
            self.ui.submitBtn.setVisible(True)
            


        self.rapidly_recognition_input_type_changed(normalized)

    def rapidly_recognition_input_type_changed(self, text):
        """بر اساس نوع متن ورودی (دستور، فایل اجرایی، URL، عبارت ریاضی یا جستجو)، آیکون و برچسب نشانگر نوع ورودی را تنظیم می‌کند."""

        if not text:
            return

        text_lower = text.lower()

        # Windows commands
        if text_lower in self.windows_command:
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "run-command.png"
                ))
            )
            self.ui.input_mode_text.setText("فرمان سیستمی")

        # Tavana commands
        elif text_lower in self.tavana_command:
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "tavana.png"
                ))
            )
            self.ui.input_mode_text.setText("فرمان توانا")

        # Programs
        elif text_lower in self._program_display_map:
            original_name = self._program_display_map[text_lower]

            program_icon = self._program_icon_path(original_name)

            self.ui.input_mode.setIcon(
                QIcon(program_icon or self.DEFAULT_PROGRAM_ICON)
            )
            self.ui.input_mode_text.setText("اجرای برنامه")
        # Executable files
        elif is_executable(text):
            clean_text = text.replace(".lnk", "").replace(".exe", "").strip()

            program_icon = self._program_icon_path(clean_text)

            self.ui.input_mode.setIcon(
                QIcon(program_icon or self.DEFAULT_PROGRAM_ICON)
            )
            self.ui.input_mode_text.setText("یافتن فایل اجرایی")
        # URL
        elif is_url(text):
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "google.png"
                ))
            )
            self.ui.input_mode_text.setText("آدرس اینترنتی")
        # Math
        elif is_math_expression(text):
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "calculator.png"
                ))
            )
            self.ui.input_mode_text.setText("ماشین حساب")  
        # First character is uppercase → Google
        elif text[0].isupper():
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "google.png"
                ))
            )
            self.ui.input_mode_text.setText("جست وجو در اینترنت")

        # Default → Google
        else:
            self.ui.input_mode.setIcon(
                QIcon(resource_path(
                    "assets", "icons", "shared_icons", "google.png"
                ))
            )
            self.ui.input_mode_text.setText("جست وجو در اینترنت")
       

    def reset_box(self):
        """نوار جستجو را خالی می‌کند، عناصر را با انیمیشن پنهان و سپس پنجره را می‌بندد."""
        self.ui.searchBox.setText("")
        widget_slide_fade_out(self.ui.searchFrame, "bottom")
        widget_slide_fade_out(self.ui.logoButton, "bottom")

        self.toggle_visibility()

    def refresh_theme(self):
        """تم را بین روشن و تیره جابه‌جا می‌کند و با انیمیشن محو، رابط کاربری را با تم جدید بازسازی می‌کند."""
        self.is_dark_theme = not self.is_dark_theme
        print(f"Theme changed: {'Dark' if self.is_dark_theme else 'Light'}")
        database.write_app_info(f"{'Dark' if self.is_dark_theme else 'Light'}")
        QApplication.quit()
        open_app = sys.executable
        subprocess.Popen([open_app] + sys.argv)

        sys.exit(0)    


    def update_suggestions(self, new_text: str | None = None):
        """در صورت وجود new_text، آن را در بالای لیست پیشنهادها قرار می‌دهد؛ در غیر این صورت آیتم‌های جدید تاریخچه را به لیست اضافه می‌کند."""
        if self._auto_complete_model is None:
            return

        if new_text:
            icon_path = resource_path("assets", "icons", "recently.png")

            for row in range(self._auto_complete_model.rowCount()):
                if self._auto_complete_model.item(row).text() == new_text:
                    self._auto_complete_model.takeRow(row)
                    break
            self._suggestions_cache = [
                item for item in self._suggestions_cache if item[0] != new_text
            ]

            if icon_path not in self._icon_cache:
                try:
                    self._icon_cache[icon_path] = QIcon(icon_path)
                except Exception:
                    self._icon_cache[icon_path] = QIcon()

            item = QStandardItem(new_text)
            item.setIcon(self._icon_cache[icon_path])
            self._auto_complete_model.insertRow(0, item)

            self._suggestions_cache.insert(
                0,
                [new_text, icon_path, icon_path, "history"]
            )

            return

        new_history = self.history_manager.get_history_items()[:1000]
        existing = {item[0]
                    for item in self._suggestions_cache}

        added = 0
        for item in new_history:
            if item[0] not in existing:
                self._suggestions_cache.append(item)
                text = item[0]
                dark = item[1]
                light = item[2]
                icon_path = dark if self.is_dark_theme else light
                if icon_path not in self._icon_cache:
                    self._icon_cache[icon_path] = QIcon(icon_path)
                it = QStandardItem(text)
                it.setIcon(self._icon_cache[icon_path])
                self._auto_complete_model.appendRow(it)
                added += 1
                if added > 50:
                    break

    def clear_searchbox(self):
        """متن نوار جستجو را پاک می‌کند."""
        self.ui.searchBox.clear()
