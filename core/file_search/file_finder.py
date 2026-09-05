"""جستجوی فایل روی دیسک و کش‌کردن مسیرهای پیداشده."""

import os
import shutil
import subprocess
import threading
from typing import Optional

import psutil
from PySide6.QtCore import QFileInfo, QObject, QThread, Signal
from PySide6.QtWidgets import QFileIconProvider

from core.database import database
from core.paths.paths import PROGRAM_ICONS_DIR, resource_path


ES_PATH = shutil.which("es.exe") or shutil.which(
    "es") or resource_path("es.exe")

BLOCKED_DIRS = {
    "windows", "system32", "syswow64", "winsxs", "winside",
    "$recycle.bin", "system volume information", "perflogs",
    "recovery", "$windows.~ws", "$windows.~bt", "msocache",
    "programdata\\microsoft\\windows\\wer",
}

PRIORITY_SEARCH_PATHS = [
    "Users", "Program Files", "Program Files (x86)",
    "Games", "SteamLibrary", "GOG Games", "Epic Games",
]


class FileSearchWorker(QObject):
    """جستجو را در QThread اجرا می‌کند و نتیجه را با Signal می‌فرستد."""

    found = Signal(str)
    not_found = Signal()
    started = Signal()

    def __init__(self, finder: "FileFinder", filename: str, update_cache: bool = True):
        """کارگر جستجو را با فایندر مادر، نام فایل هدف و پرچم به‌روزرسانی کش می‌سازد."""
        super().__init__()
        self._finder = finder
        self._filename = filename
        self._update_cache = update_cache

    def run(self) -> None:
        """جستجوی واقعی را انجام می‌دهد و بسته به نتیجه، سیگنال found یا not_found را می‌فرستد."""
        self.started.emit()
        result = self._finder._do_search(self._filename, self._update_cache)
        if result:
            self.found.emit(result)
        else:
            self.not_found.emit()


class FileFinder(QObject):
    """جستجوگر فایل با کش دیتابیسی؛ جستجو را ناهمگام (async) در QThread اجرا می‌کند."""

    file_found = Signal(str)
    file_not_found = Signal()
    search_started = Signal()

    def __init__(self, parent=None):
        """کش، قفل هم‌زمانی و آبجکت‌های Qt لازم برای جستجو را مقداردهی اولیه می‌کند."""
        super().__init__(parent)
        self._cache: Optional[dict] = None
        self._searching: bool = False
        self._lock = threading.Lock()
        self._thread: Optional[QThread] = None
        self._worker: Optional[FileSearchWorker] = None
        self._icon_provider = QFileIconProvider()

    def _extract_icon(self, filepath: str) -> Optional[str]:
        """آیکون برنامه را استخراج و در data/program_icons ذخیره می‌کند."""

        if not os.path.isfile(filepath):
            return None

        icon_dir = PROGRAM_ICONS_DIR
        os.makedirs(icon_dir, exist_ok=True)

        filename = os.path.splitext(os.path.basename(filepath))[0]
        icon_path = os.path.join(icon_dir, filename + ".png")

        if os.path.exists(icon_path):
            return icon_path

        try:
            icon = self._icon_provider.icon(QFileInfo(filepath))

            if icon.isNull():
                return None

            if icon.pixmap(256, 256).save(icon_path):
                return icon_path
        except Exception as e:
            print(f"خطا در استخراج آیکون '{filepath}': {e}")

        return None

    def load_existing_directories(self) -> dict:
        """کش مسیرهای فایل را برمی‌گرداند؛ در صورت نبود، از دیتابیس بار می‌کند."""
        if self._cache is None:
            self._cache = database.get_directories()
        return self._cache

    def save_directories(self, directories: dict) -> None:
        """مسیرهای داده‌شده را در دیتابیس ذخیره می‌کند.

        برای بهینه‌سازی، لازم نیست کل کش اینجا پاس داده شود — فقط ردیف‌های
        جدید/تغییریافته کافی است؛ کش حافظه (self._cache) از قبل توسط فراخوان
        به‌روزرسانی شده است.
        """
        database.save_directories(directories)

    def _search_with_everything(self, filename: str) -> Optional[str]:
        """با استفاده از ابزار es.exe (رابط خط‌فرمان Everything) فایل را جستجو می‌کند."""
        es_path = (
            shutil.which("es")
            or shutil.which("es.exe")
            or (ES_PATH if os.path.isfile(ES_PATH) else None)
        )
        if not es_path:
            return None
        try:
            result = subprocess.run(
                [es_path, "-n", "1", filename],
                capture_output=True, text=True, timeout=10, check=False,
            )
            line = result.stdout.strip()
            if line and os.path.isfile(line):
                return line
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        return None

    def _search_with_where(self, filename: str, drives: list) -> Optional[str]:
        """با فرمان `where /r` ویندوز، فایل را در هر یک از درایوهای داده‌شده جستجو می‌کند."""
        for drive in drives:
            try:
                result = subprocess.run(
                    ["where", "/r", drive, filename],
                    capture_output=True, text=True, timeout=30, shell=False, check=False,
                )
                for line in result.stdout.strip().splitlines():
                    line = line.strip()
                    if line and os.path.isfile(line):
                        return line
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue
        return None

    def _is_blocked_dir(self, path: str) -> bool:
        """تشخیص می‌دهد آیا مسیر داده‌شده جزو پوشه‌های سیستمیِ مسدود (BLOCKED_DIRS) است یا نه."""
        lower = path.lower()
        return any(blocked in lower for blocked in BLOCKED_DIRS)

    def _smart_walk(self, filename: str, drives: list) -> Optional[str]:
        """در نبود es.exe و where، با پیمایش هوشمند پوشه‌ها (اول مسیرهای پراحتمال) فایل را پیدا می‌کند."""
        for drive in drives:
            priority_roots = [
                os.path.join(drive, p)
                for p in PRIORITY_SEARCH_PATHS
                if os.path.isdir(os.path.join(drive, p))
            ]
            search_roots = priority_roots if priority_roots else [drive]
            for root_path in search_roots:
                try:
                    for root, dirs, files in os.walk(root_path, topdown=True):
                        dirs[:] = [
                            d for d in dirs
                            if not self._is_blocked_dir(os.path.join(root, d))
                            and self._is_accessible(os.path.join(root, d))
                        ]
                        if filename in files:
                            return os.path.join(root, filename)
                except (OSError, IOError):
                    continue
        return None

    def _is_accessible(self, path: str) -> bool:
        """بررسی می‌کند که آیا مسیر داده‌شده قابل خواندن و اجراست یا نه."""
        try:
            return os.access(path, os.R_OK | os.X_OK)
        except (OSError, IOError):
            return False

    def _do_search(self, filename: str, update_cache: bool) -> Optional[str]:
        """ابتدا کش را چک می‌کند، سپس به‌ترتیب با Everything، where و پیمایش پوشه‌ها جستجو می‌کند."""
        directories_data = self.load_existing_directories()

        if filename in directories_data:
            path = directories_data[filename]
            if os.path.exists(path):
                self._extract_icon(path)
                return path

        drives = [
            d.device for d in psutil.disk_partitions()
            if "fixed" in d.opts.lower()
        ]

        found_path = (
            self._search_with_everything(filename)
            or self._search_with_where(filename, drives)
            or self._smart_walk(filename, drives)
        )

        if found_path:
            self._extract_icon(found_path)
            if update_cache:
                directories_data[filename] = found_path
                self.save_directories({filename: found_path})

        return found_path

    def _cleanup_thread(self) -> None:
        """بعد از اتمام جستجو thread را پاک می‌کند."""
        with self._lock:
            self._searching = False
        self._thread = None
        self._worker = None


    def find_file_async(self, filename: str, update_cache: bool = True) -> bool:
        """جستجو را در یک QThread جدا شروع می‌کند (بدون فریزشدن رابط کاربری) و نتیجه را از طریق سیگنال‌ها اعلام می‌کند."""
        if self._searching:
            print("جستجو در حال انجام است...")
            return False

        with self._lock:
            self._searching = True

        self._thread = QThread()
        self._worker = FileSearchWorker(self, filename, update_cache)
        self._worker.moveToThread(self._thread)

        self._worker.started.connect(self.search_started)
        self._worker.found.connect(self.file_found)
        self._worker.not_found.connect(self.file_not_found)

        self._thread.started.connect(self._worker.run)
        self._worker.found.connect(self._thread.quit)
        self._worker.not_found.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup_thread)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        self._thread.start()
        return True

    def open_that_path(self, filepath: str) -> bool:
        """باز کردن هر نوع فایلی با برنامه‌ی پیش‌فرض ویندوز."""
        try:
            os.startfile(filepath)
            return True
        except OSError as e:
            print(f"خطا در اجرای فایل: {e}")
            return False

    def scan_start_menu_programs(self) -> bool:
        """منوی Start ویندوز را برای میانبرهای جدید اسکن می‌کند و کش را به‌روز می‌کند."""
        start_menu_path = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
        directories_data = self.load_existing_directories()
        if not os.path.exists(start_menu_path):
            return False
        try:
            new_entries: dict = {}
            for root, _dirs, files in os.walk(start_menu_path):
                for file in files:
                    if file.lower().endswith((".lnk", ".exe", ".url")) and file not in directories_data:
                        full_path = os.path.join(root, file)
                        directories_data[file] = full_path
                        new_entries[file] = full_path
                        self._extract_icon(full_path)

            if new_entries:
                self.save_directories(new_entries)
                print(f"{len(new_entries)} برنامه جدید پیدا شد")

            return True
        except Exception as e:
            print(f"خطا در اسکن: {e}")
            return False
