"""فعال‌سازی افکت بلور (Acrylic) پس‌زمینه‌ی پنجره در ویندوز."""
import ctypes
from ctypes import wintypes


def enable_blur(hwnd):
    """افکت بلور شیشه‌ای را روی هندل پنجره‌ی داده‌شده با فراخوانی مستقیم API ویندوز فعال می‌کند."""
    class ACCENTPOLICY(ctypes.Structure):
        """ساختار سیاست شفافیت مورد نیاز SetWindowCompositionAttribute."""
        _fields_ = [
            ("AccentState", ctypes.c_int),
            ("AccentFlags", ctypes.c_int),
            ("GradientColor", ctypes.c_int),
            ("AnimationId", ctypes.c_int),
        ]

    class WINCOMPATTRDATA(ctypes.Structure):
        """ساختار دادهٔ ورودی تابع SetWindowCompositionAttribute ویندوز."""
        _fields_ = [
            ("Attribute", ctypes.c_int),
            ("Data", ctypes.POINTER(ACCENTPOLICY)),
            ("SizeOfData", ctypes.c_size_t),
        ]

    accent = ACCENTPOLICY()
    accent.AccentState = 3
    accent.GradientColor = 0xFF000000

    data = WINCOMPATTRDATA()
    data.Attribute = 19
    data.Data = ctypes.pointer(accent)
    data.SizeOfData = ctypes.sizeof(accent)

    ctypes.windll.user32.SetWindowCompositionAttribute(hwnd, ctypes.pointer(data))

