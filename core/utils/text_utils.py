"""ابزارهای نرمال‌سازی متن ورودی."""


def normalize_text(text: str) -> str:
    """نشانه‌های نمایشی/فارسی (./، *، «رادیکال»، «رند») را به نویسه‌ی ریاضی معادل تبدیل می‌کند."""
    return (
        text.replace("*", "x")
        .replace("xx", "÷")
        .replace("رادیکال", "√")
        .replace("sqrt(", "√")
        .replace("رند", "~")
    )
