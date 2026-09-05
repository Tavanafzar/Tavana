"""انیمیشن‌های محو، سرشدن و لغزش برای عناصر رابط کاربری."""

import shiboken6
from PySide6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
)
from PySide6.QtWidgets import QGraphicsOpacityEffect

from core.database import database
from core.database.database import DEFAULT_ANIMATION_SPEEDS


_animation_speeds = None


def _get_speeds():
    """مدت‌زمان انیمیشن‌های ورود/خروج را از دیتابیس می‌خواند و در حافظه کش می‌کند."""
    global _animation_speeds

    if _animation_speeds is None:
        try:
            speeds = database.get_animations()

            _animation_speeds = (
                speeds
                if len(speeds) >= 2
                else list(DEFAULT_ANIMATION_SPEEDS)
            )

        except Exception as e:
            print(
                f"خطا در خواندن سرعت انیمیشن، "
                f"استفاده از مقدار پیش‌فرض: {e}"
            )

            _animation_speeds = list(DEFAULT_ANIMATION_SPEEDS)

    return _animation_speeds


def _track_animation(window, anim: QPropertyAnimation) -> None:
    """رفرنس انیمیشن را تا پایانش زنده نگه می‌دارد."""
    if not hasattr(window, "_animations"):
        window._animations = []

    window._animations.append(anim)

    anim.finished.connect(
        lambda: (
            window._animations.remove(anim)
            if anim in window._animations
            else None
        )
    )


def window_fade_in(window):
    """کل پنجره را با محوشدن از شفاف به کاملاً نمایان می‌کند."""
    speeds = _get_speeds()

    anim = QPropertyAnimation(window, b"windowOpacity")

    anim.setDuration(speeds[0])
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutQuart)

    _track_animation(window, anim)
    anim.start()


def window_fade_out(window, callback=None):
    """کل پنجره را با محوشدن به‌تدریج ناپدید می‌کند و در پایان callback را صدا می‌زند."""
    speeds = _get_speeds()

    anim = QPropertyAnimation(window, b"windowOpacity")

    anim.setDuration(speeds[1])
    anim.setStartValue(1.0)
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.InQuart)

    if callback:
        anim.finished.connect(callback)

    _track_animation(window, anim)
    anim.start()


def _get_opacity_effect(widget):
    """افکت شفافیت ویجت را برمی‌گرداند؛ در صورت نبود یا نامعتبربودن، یکی می‌سازد."""
    existing = getattr(widget, "_animation_opacity_effect", None)

    if existing is None or not shiboken6.isValid(existing):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        widget._animation_opacity_effect = effect

    return widget._animation_opacity_effect


def widget_fade_in(widget):
    """یک ویجت را با محوشدن از شفاف به نمایان می‌کند."""
    effect = _get_opacity_effect(widget)
    speeds = _get_speeds()

    old_animation = getattr(widget, "_fade_animation", None)
    if old_animation:
        old_animation.stop()

    anim = QPropertyAnimation(effect, b"opacity")

    anim.setDuration(int(speeds[0] * 0.85))
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    widget._fade_animation = anim
    anim.start()


def widget_fade_out(widget):
    """یک ویجت را با محوشدن به‌تدریج ناپدید می‌کند."""
    effect = _get_opacity_effect(widget)
    speeds = _get_speeds()

    old_animation = getattr(widget, "_fade_animation", None)
    if old_animation:
        old_animation.stop()

    anim = QPropertyAnimation(effect, b"opacity")

    anim.setDuration(int(speeds[1] * 0.75))
    anim.setStartValue(1.0)
    anim.setEndValue(0.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)

    widget._fade_animation = anim
    anim.start()


def _get_base_pos(widget):
    """موقعیت اصلی ویجت را فقط یک بار ذخیره می‌کند."""
    if not hasattr(widget, "_animation_base_pos"):
        widget._animation_base_pos = widget.pos()

    return widget._animation_base_pos


def _get_offset(direction, distance=18):
    """مقدار جابه‌جایی بر اساس جهت (مقدار ۱۵ الی ۲۰ پیکسل بهترین حس حرکتی را می‌دهد)."""
    directions = {
        "left": QPoint(-distance, 0),
        "right": QPoint(distance, 0),
        "top": QPoint(0, -distance),
        "bottom": QPoint(0, distance),
    }

    return directions.get(direction, QPoint(0, distance))


def _stop_widget_animation(widget):
    """متوقف کردن و آزادسازی انیمیشن قبلی ویجت."""
    animation = getattr(widget, "_slide_fade_animation", None)
    if animation is not None:
        animation.stop()
        animation.setParent(None)
        animation.deleteLater()
        widget._slide_fade_animation = None


def widget_slide_fade_in(
    widget,
    direction="bottom",
    distance=10,
):
    """ورود بسیار نرم و کره ای (Butter Smooth) ویجت با ترکیب Fade + Slide."""

    _stop_widget_animation(widget)
    
    base_pos = _get_base_pos(widget)
    offset = _get_offset(direction, distance)
    effect = _get_opacity_effect(widget)
    speeds = _get_speeds()

    duration = int(speeds[0] * 0.9)

    easing = QEasingCurve.Type.OutCubic

    fade = QPropertyAnimation(effect, b"opacity")
    fade.setDuration(duration)
    fade.setStartValue(0.0)
    fade.setEndValue(1.0)
    fade.setEasingCurve(easing)

    move = QPropertyAnimation(widget, b"pos")
    move.setDuration(duration)
    move.setStartValue(base_pos + offset)
    move.setEndValue(base_pos)
    move.setEasingCurve(easing)

    group = QParallelAnimationGroup()
    group.addAnimation(fade)
    group.addAnimation(move)

    widget._slide_fade_animation = group

    effect.setOpacity(0.0)
    widget.move(base_pos + offset)

    group.start()


def widget_slide_fade_out(
    widget,
    direction="bottom",
    distance=10,
):
    """خروج سریع، طبیعی و بدون گیر کردن ویجت."""

    _stop_widget_animation(widget)

    base_pos = _get_base_pos(widget)
    offset = _get_offset(direction, distance)
    effect = _get_opacity_effect(widget)
    speeds = _get_speeds()

    duration = int(speeds[1] * 0.8)

    easing = QEasingCurve.Type.InCubic

    fade = QPropertyAnimation(effect, b"opacity")
    fade.setDuration(duration)
    fade.setStartValue(1.0)
    fade.setEndValue(0.0)
    fade.setEasingCurve(easing)

    move = QPropertyAnimation(widget, b"pos")
    move.setDuration(duration)
    move.setStartValue(base_pos)
    move.setEndValue(base_pos + offset)
    move.setEasingCurve(easing)

    group = QParallelAnimationGroup(widget)
    group.addAnimation(fade)
    group.addAnimation(move)

    widget._slide_fade_animation = group

    effect.setOpacity(1.0)
    widget.move(base_pos)

    group.start()
