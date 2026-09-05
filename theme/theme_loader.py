"""ساخت و اعمال استایل‌شیت (QSS) پنجره‌ی اصلی بر اساس تم روشن/تیره."""

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QImage, QPixmap
from PySide6.QtWidgets import QGraphicsDropShadowEffect
from theme.system_theme import ThemeManager
from core.paths.paths import resource_path
from gui.animation.animations import widget_slide_fade_in, widget_slide_fade_out

icon_size = QSize(185, 185)
sub_voice_icon_size = QSize(19, 19)
small_icon_size = QSize(-60, -60)
nav_icon_size = QSize(15, 15)
button_icon_size = QSize(20, 20)

search_frame_corner_radius = 25
theme_manager = ThemeManager()
theme_state = theme_manager.get_system_theme()


DARK_COLORS = {
    "central_bg": "rgba(120,120,120,0.45)",

    "search_frame_grad_start": "#18181b",
    "search_frame_grad_stop": "#000000",
    "quick_access_bg": "(18,18,18,0.8)",
    "search_box_text": "#F2F2F2",
    "search_box_placeholder": "#9CA3AF",

    "input_mode_bg": "#202124",
    "input_mode_text": "white",
    "input_mode_fr": "#202124",

    "radio_grad_start": "#18181b",
    "radio_grad_stop": "#000000",
    "radio_text": "#F8F7FF",

    "tooltip_grad_start": "#18181b",
    "tooltip_grad_stop": "#000000",
    "tooltip_text": "white",

    "tray_text": "white",
    "popup_text": "white",
    "popup_border": "none",

    "autocomplete_bg": "#000000",
    "autocomplete_border": "1px solid black",
    "autocomplete_text": "White",
    "autocomplete_item_hover_bg": "#161616",
    "autocomplete_item_selected_bg": "#18181b",
    "autocomplete_item_selected_text": "white",
}

LIGHT_COLORS = {
    "central_bg": "rgba(0,0,0,0.45)",

    "search_frame_grad_start": "#ECEEF2",
    "search_frame_grad_stop": "#D1D3E0",
    "quick_access_bg": "(238,238,238,0.8)",

    "search_box_text": "rgb(36, 36, 37)",
    "search_box_placeholder": "#6B7280",

    "input_mode_bg": "#f5f6fa",
    "input_mode_text": "black",
    "input_mode_fr": "#f5f6fa",

    "radio_grad_start": "#ECEEF2",
    "radio_grad_stop": "#D1D3E0",
    "radio_text": "black",

    "tooltip_grad_start": "#ECEEF2",
    "tooltip_grad_stop": "#D1D3E0",
    "tooltip_text": "black",

    "tray_text": "black",
    "popup_text": "black",
    "popup_border": "1px solid darkgray",

    "autocomplete_bg": "#D1D3E0",
    "autocomplete_border": "none",
    "autocomplete_text": "black",
    "autocomplete_item_hover_bg": "rgba(255,255,255,1)",
    "autocomplete_item_selected_bg": "rgba(255,255,255,0.55)",
    "autocomplete_item_selected_text": "black",
}


@staticmethod
def radio_buttons(ui):
    """لیست دکمه‌های رادیویی حالت‌های جستجو را برمی‌گرداند."""
    return [
        ui.runProgramRadioButton,
        ui.gptRadioButton,
        ui.gmailRadioButton,
        ui.cmdRadioButton,
        ui.webRadioButton,
        ui.youtubeRadioButton,
        ui.translateRadioButton,
        ui.driveRadioButton,
        ui.mathRadioButton,
    ]


class ThemeLoader:
    """اعمال رنگ‌ها، آیکون‌ها و استایل‌شیت متناسب با تم فعلی روی ویجت‌های رابط کاربری."""

    _ui = None

    _dark = theme_state
    _checkbox = False

    @staticmethod
    def graphic_shadow(widgets):
        """افکت سایه‌ی نرم را روی هر یک از ویجت‌های داده‌شده اعمال می‌کند."""
        for widget in widgets:
            shadow = QGraphicsDropShadowEffect(widget)
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 2)
            shadow.setColor(QColor(0, 0, 0, 90))
            widget.setGraphicsEffect(shadow)

    @staticmethod
    def apply_theme(window, ui):
        """تم روشن یا تیره را بر اساس window.is_dark_theme روی کل رابط کاربری اعمال می‌کند."""
        ThemeLoader._ui = ui

        ThemeLoader._dark = getattr(window, "is_dark_theme", ThemeLoader._dark)

        widget = [ui.searchFrame]
        if ThemeLoader._dark:
            ThemeLoader._apply_dark_theme(window, ui)
        else:
            ThemeLoader._apply_light_theme(window, ui)

        ThemeLoader.graphic_shadow(widget)
        rbtn = radio_buttons(ui)

        ThemeLoader.graphic_shadow(rbtn)

        return ui

    @staticmethod
    def _quick_access_icon_name() -> str:
        """نام فایل آیکون فلش دسترسی سریع را بر اساس جهت و تم فعلی می‌سازد."""
        direction = "right" if ThemeLoader._checkbox else "left"
        variant = "dark" if ThemeLoader._dark else "light"
        return f"arrow_{direction}_{variant}.png"

    @staticmethod
    def _apply_quick_access_icon(ui):
        """آیکون دکمه‌ی دسترسی سریع را متناسب با وضعیت فعلی تنظیم می‌کند."""
        ThemeLoader._set_icon(
            ui.quick_access_btn,
            resource_path("assets", "icons",
                          ThemeLoader._quick_access_icon_name()),
            small_icon_size,
        )

    @staticmethod
    def _apply_dark_theme(window, ui):
        """استایل‌شیت و آیکون‌های تم تیره را روی رابط کاربری اعمال می‌کند."""
        c = DARK_COLORS
        window.setStyleSheet(f"""
        * {{
            border: none;
        }}

        #centralwidget {{
            background: {c['central_bg']};
        }}


    #searchFrame {{
        background-color: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 {c['search_frame_grad_start']},
            stop:1 {c['search_frame_grad_stop']}
        );
        border-radius:{search_frame_corner_radius}px;
        }}


        #logoButton{{
            background:transparent;
        }}

        #searchBox {{
            background:transparent;
            color:{c['search_box_text']};
            font-weight:700;
            font-size:13pt;
            padding-bottom:5px;
        }}

        #searchBox::placeholder {{
            color:{c['search_box_placeholder']};
        }}

        #searchBox:focus{{
            border:none;
        }}
        #input_mode {{
            background:{c['input_mode_bg']};
            border-radius: 20px;
            
            padding-left:15px;
                

        }}
        #input_mode_text{{
            color:{c['input_mode_text']};
        }}

        #submitBtn{{
            background:transparent;
            border-radius:20px;
        }}

        #modeFrame{{
            background:transparent;
            border-radius:21px;
        }}

        #searchMode{{
            background:transparent;
            border-radius:20px;
        }}

QRadioButton{{

        background-color: qlineargradient(
            spread:pad,
            x1:0, y1:0,
            x2:1, y2:1,
            stop:0 {c['radio_grad_start']},
            stop:1 {c['radio_grad_stop']}
        );


    color:{c['radio_text']};
    font-weight:600;
    font-size:11pt;
    border-radius:17px;
    outline:None;
    padding:0px;
    spacing:8px;
}}

        QRadioButton::indicator{{
            width:0px;
            height:0px;
            image:none;
        }}

        QToolTip{{

            background-color:qlineargradient(
                spread:pad,
                x1:0.716,
                y1:0.000636364,
                x2:0.516818,
                y2:1,
                stop:0 {c['tooltip_grad_start']},
                stop:1 {c['tooltip_grad_stop']}
            );
            font-size:10pt;
            color:{c['tooltip_text']};

        }}

    #sep{{border:none;background-color:transparent;}}
    
    
    #show_version{{
        color:{c['search_frame_grad_stop']}
    }}

        """)
        btns = radio_buttons(ui)

        ThemeLoader._set_icon(ui.logoButton, resource_path(
            "assets", "icons", "dark", "brand.png"), icon_size)
        ThemeLoader._set_icon(ui.submitBtn, resource_path(
            "assets", "icons", "dark", "Search Icon2.png"), sub_voice_icon_size)
        ThemeLoader._set_icon(ui.voiceBtn, resource_path(
            "assets", "icons", "dark", "voice_icon.png"), sub_voice_icon_size)
        ThemeLoader._set_icon(btns[2], resource_path(
            "assets", "icons", "dark", "chatGPT.png"), sub_voice_icon_size)
        
        btn = radio_buttons(ui)[1]

        ThemeLoader._set_icon(btn, resource_path(
            "assets", "icons", "dark", "chatGPT.png"), sub_voice_icon_size)           
        
        for btn in radio_buttons(ui):
            ThemeLoader._set_icon(btn, resource_path(
                "assets", "icons", "shared_icons", f"{ThemeLoader._get_icon_name(btn)}.png"), button_icon_size)

    @staticmethod
    def _apply_light_theme(window, ui):
        """استایل‌شیت و آیکون‌های تم روشن را روی رابط کاربری اعمال می‌کند."""
        c = LIGHT_COLORS
        window.setStyleSheet(f"""
            * {{
                border: none;
            }}
            #centralwidget {{
                background: {c['central_bg']};
            }}



            #searchFrame {{
                background-color: qlineargradient(spread:pad, x1: 0.716, y1: 0.000636364,
                x2: 0.516818, y2: 1,
                stop:0 {c['search_frame_grad_start']},
                stop:1 {c['search_frame_grad_stop']}
                );
                border-radius: {search_frame_corner_radius}px;

            }}
                QCheckBox{{
                    spacing:6px;
                    background:rgba{c['quick_access_bg']};
                    border-radius:16px;
                }}
                QCheckBox::indicator{{
                     background: transparent;
            width:0px;
            height:0px;
        }}


            #logoButton{{
            background:transparent;
            }}
            #searchBox {{
                background-color: transparent;
                color: {c['search_box_text']};
                font-weight: 700;
                font-size: 13pt;
                padding-bottom: 5px;
            }}
            #searchBox::placeholder {{
                color: {c['search_box_placeholder']};
            }}
            #searchBox:focus {{ border: none; }}
            
            #input_mode {{
                background:{c['input_mode_bg']};
                border-radius: 20px;
                padding-left:15px;
            }}
        #input_mode_text{{
            color:{c['input_mode_text']};
        }}

            #modeFrame {{
                background-color: transparent;
                border-radius: 21px;
            }}
            QRadioButton {{
                background-color: qlineargradient(spread:pad, x1: 0.716, y1: 0.000636364,
                x2: 0.516818, y2: 1,
                stop:0 {c['radio_grad_start']},
                stop:1 {c['radio_grad_stop']}
                );
                color: {c['radio_text']};
                font-weight: 600;
                font-size: 11pt;
                border-radius: 17px;
                outline:None;
                padding: 0px;
                spacing:8px;
            }}
            QRadioButton::indicator {{
        width: 0px;
        height: 0px;
        image: none;
    }}

            #submitBtn{{
            background-color: transparent;
             border-radius:20px;
            }}

             QToolTip{{
                background-color: qlineargradient(spread:pad, x1: 0.716, y1: 0.000636364,
                    x2: 0.516818, y2: 1, stop: 0 {c['tooltip_grad_start']},
                    stop: 1 {c['tooltip_grad_stop']});
                color:{c['tooltip_text']};

                font-size:10pt;

            }}
                   #sep{{border:none;background-color:transparent;}}

                    
                    #show_version{{
                    color:{c['search_frame_grad_stop']}
                                    }}
        """)

        
        ThemeLoader._set_icon(ui.logoButton, resource_path(
            "assets", "icons", "light", "brand.png"), icon_size)
        ThemeLoader._set_icon(ui.submitBtn, resource_path(
            "assets", "icons", "light", "search.png"), sub_voice_icon_size)
        ThemeLoader._set_icon(ui.voiceBtn, resource_path(
            "assets", "icons", "light", "vts.png"), sub_voice_icon_size)

        btn = radio_buttons(ui)[1]

        ThemeLoader._set_icon(btn, resource_path(
            "assets", "icons", "light", "chatGPT.png"), sub_voice_icon_size)      
        
        for btn in radio_buttons(ui):
            ThemeLoader._set_icon(btn, resource_path(
                "assets", "icons", "shared_icons", f"{ThemeLoader._get_icon_name(btn)}.png"), button_icon_size)
           

    @staticmethod
    def tray_menu_style() -> str:
        """استایل‌شیت منوی تری سیستم را متناسب با تم فعلی برمی‌گرداند."""
        c = ThemeLoader._colors()
        gradient = ThemeLoader._gradient(
            c["search_frame_grad_start"], c["search_frame_grad_stop"])

        return f"""
            QMenu {{
                background-color: {gradient};
                color: {c['tray_text']};
                min-width: 120px;
                min-height: 60px;
                font-size: 10pt;
                border-radius:10px;
                padding:10px;
            }}
        """

    @staticmethod
    def popup_style() -> tuple:
        """استایل‌شیت اعلان پاپ‌آپ را متناسب با تم فعلی برمی‌گرداند (بک‌گراند و ویجت جدا)."""
        c = ThemeLoader._colors()
        gradient = ThemeLoader._gradient(
            c["search_frame_grad_start"], c["search_frame_grad_stop"])
        border = f"border:{c['popup_border']};" if c["popup_border"] != "none" else ""

        notification_qss = f"""
            background-color: {gradient};
            margin:12px;
            padding: 15px;
            {border}
        """
        widget_qss = f"""
            QWidget {{
                background-color:transparent;
                color: {c['popup_text']};
                border-radius: 20px;
                font-size: 13px;
                font-weight: 600;
            }}
        """

        return notification_qss, widget_qss

    @staticmethod
    def autocomplete_style() -> str:
        """استایل‌شیت لیست پیشنهادهای خودکار (autocomplete) را متناسب با تم فعلی برمی‌گرداند."""
        c = ThemeLoader._colors()
        border = f"border:{c['autocomplete_border']};" if c["autocomplete_border"] != "none" else ""
        text_color = f"color: {c['autocomplete_text']};" if c["autocomplete_text"] else ""

        return f"""
            QListView {{
                outline: None;
                {border}
                background-color: {c['autocomplete_bg']};
                font-size: 11pt;
                font-weight: 500;
                {text_color}
            }}
            QListView::item {{
                padding: 9px;
                background: rgba(0,0,0,0);
            }}
            QListView::item:selected {{
                background: {c['autocomplete_item_selected_bg']};
                color: {c['autocomplete_item_selected_text']};
                outline: None;
            }}
            QListView::item:hover {{
                background: {c['autocomplete_item_hover_bg']};
            }}
        """

    @staticmethod
    def quick_access_state(checked):
        """وقتی چک‌باکس quick_access_btn تغییر حالت میده صدا زده میشه."""
        ui = ThemeLoader._ui
        if ui is None:
            return

        ThemeLoader._checkbox = checked

        if checked:
            widget_slide_fade_in(ui.switch_theme, "right")
            widget_slide_fade_in(ui.settings, "right")
        else:
            widget_slide_fade_out(ui.switch_theme, "right")
            widget_slide_fade_out(ui.settings, "right")

        ui.settings.show()
        ui.switch_theme.show()

        ThemeLoader._apply_quick_access_icon(ui)

    @staticmethod
    def _colors() -> dict:
        """دیکشنری رنگ مناسب تم را برمی‌گرداند."""
        return DARK_COLORS if ThemeLoader._dark else LIGHT_COLORS

    @staticmethod
    def _gradient(start: str, stop: str) -> str:
        """رشته‌ی گرادیان QSS متناسب با تم فعلی را می‌سازد."""
        if ThemeLoader._dark:
            return (
                f"qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
                f"stop:0 {start}, stop:1 {stop})"
            )
        return (
            f"qlineargradient(spread:pad, x1: 0.716, y1: 0.000636364, "
            f"x2: 0.516818, y2: 1, stop:0 {start}, stop:1 {stop})"
        )

    @staticmethod
    def _set_icon(button, path: str, size: QSize) -> None:
        """آیکون دکمه را با کیفیت بالا (تبدیل فرمت و مقیاس‌دهی نرم) تنظیم می‌کند."""
        image = QImage(path)
        if not image.isNull():
            if image.format() != QImage.Format_ARGB32:
                image = image.convertToFormat(QImage.Format_ARGB32)

            scaled_image = image.scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            pixmap = QPixmap.fromImage(scaled_image)
            button.setIcon(QIcon(pixmap))
            button.setIconSize(size)

    @staticmethod
    def _get_icon_name(button) -> str:
        """نام فایل آیکون متناظر با نام آبجکت دکمه‌ی رادیویی را برمی‌گرداند."""
        name_mapping = {

            "runProgramRadioButton": "searchInDir",
            "gptRadioButton": "chatGPT",
            "gmailRadioButton": "gmail",
            "cmdRadioButton": "run-command",
            "webRadioButton": "Google",
            "separatorBeetwinGoogleAndYoutube": "sep",
            "youtubeRadioButton": "youtube",
            "translateRadioButton": "translate",
            "driveRadioButton": "drive",

            "mathRadioButton": "calculator"
        }
        return name_mapping.get(button.objectName(), "")
