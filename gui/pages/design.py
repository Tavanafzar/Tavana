"""طراحی و چیدمان رابط کاربری پنجره‌ی اصلی (نوار جستجو، دکمه‌های حالت و ناحیه‌ی میانبرها)."""

from PySide6.QtCore import QPoint, QSize, Qt, QTimer
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QGraphicsBlurEffect,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QStackedWidget,
    QStyleFactory,
    QVBoxLayout,
    QWidget,
    QCheckBox
)

from core.database import database
from gui.animation.animations import widget_slide_fade_in, widget_slide_fade_out
from theme.theme_loader import ThemeLoader
from handlers.font_handler import set_font


class Ui_MainWindow:
    """ساخت و چیدمان تمام ویجت‌های پنجره‌ی اصلی."""

    def __init__(self):
        """فیلدهای اصلی رابط کاربری را با مقدار اولیه‌ی خالی تعریف می‌کند."""
        self.mainFrame = None
        self.stackedWidget = None
        self.button_group = None
        self.appStyle = QStyleFactory.create("Fusion")

    def setupUi(self, MainWindow):
        """تمام نواحی رابط کاربری (لوگو، جستجو، پایین صفحه و ...) را می‌سازد و در پنجره‌ی اصلی قرار می‌دهد."""
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.set_version()
        self._setup_main_layout()
        self._setup_logo_area()
        self._setup_search_area()
        self._setup_bottom_area()

        MainWindow.setCentralWidget(self.centralwidget)

    def set_version(self):
        """نسخه‌ی برنامه را از دیتابیس می‌خواند و متن نمایشی آن را برمی‌گرداند."""
        info = database.get_app_info()
        version = info.get("version", "")
        return f"نسخه {version}"

    def _setup_main_layout(self):
        """چیدمان اصلی را می‌سازد و mainFrame را مستقیم درون centralwidget جای می‌دهد."""
        self.mainLayout = QVBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setObjectName("verticalLayout")
        self.mainLayout.setContentsMargins(0, 150, 0, 0)

        self.mainFrame = QFrame()
        self.mainFrame.setObjectName("mainFrame")
        self.mainFrame.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.mainFrame.setFrameShape(QFrame.Shape.NoFrame)

        self.topAreaLayout = QGridLayout(self.mainFrame)
        self.topAreaLayout.setSpacing(0)
        self.topAreaLayout.setObjectName("gridLayout_2")
        self.topAreaLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.mainFrame)

    def _setup_logo_area(self):
        """ناحیه‌ی لوگوی برنامه را می‌سازد."""

        self.logoFrame = QFrame(self.mainFrame)
        self.logoFrame.setObjectName("logoFrame")
        self.logoFrame.setFrameShape(QFrame.Shape.NoFrame)

        self.logoFrameLayout = QVBoxLayout(self.logoFrame)
        self.logoFrameLayout.setSpacing(0)
        self.logoFrameLayout.setObjectName("verticalLayout_3")
        self.logoFrameLayout.setContentsMargins(0, 0, 0, 0)

        self.logoButton = QPushButton(self.logoFrame)
        self.logoButton.setObjectName("logoButton")
        self.logoButton.setMinimumSize(QSize(210, 100))
        self.logoButton.setMaximumSize(QSize(210, 100))
        self.logoButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.logoButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.logoFrameLayout.addWidget(
            self.logoButton, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        )

        self.topAreaLayout.addWidget(
            self.logoFrame, 1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.topAreaLayout.setRowStretch(1, 2)

    def _setup_search_area(self):
        """قاب و چیدمان نوار جستجو را می‌سازد."""
        self.searchArea = QFrame(self.mainFrame)
        self.searchArea.setObjectName("searchArea")
        self.searchArea.setMinimumSize(QSize(0, 78))
        self.searchArea.setMaximumSize(QSize(16777215, 78))
        self.searchArea.setFrameShape(QFrame.Shape.NoFrame)

        self.searchFrameLayout = QHBoxLayout(self.searchArea)
        self.searchFrameLayout.setSpacing(0)
        self.searchFrameLayout.setObjectName("horizontalLayout")

        self.searchFrame = QFrame(self.searchArea)
        self.searchFrame.setObjectName("searchFrame")
        self.searchFrame.setMinimumSize(QSize(800, 52))
        self.searchFrame.setMaximumSize(QSize(800, 52))
        self.searchFrame.setFrameShape(QFrame.Shape.NoFrame)

        self.searchAreaLayout = QGridLayout(self.searchFrame)
        self.searchAreaLayout.setSpacing(0)
        self.searchAreaLayout.setObjectName("horizontalLayout_2")
        self.searchAreaLayout.setContentsMargins(10, 0, 10, 0)
        self.searchAreaLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._setup_search_buttons()

        self.searchFrameLayout.addWidget(self.searchFrame)

        self.topAreaLayout.addWidget(self.searchArea, 2, 0)
        self.topAreaLayout.setRowStretch(2, 2)

    def _setup_search_buttons(self):
        """فیلد ورودی جستجو و دکمه‌های اطراف آن (صدا، ارسال، حالت ورودی) را می‌سازد."""
        self.voiceBtn = QPushButton(self.searchFrame)
        self.voiceBtn.setObjectName("searchMode")
        self.voiceBtn.setMinimumSize(QSize(40, 40))
        self.voiceBtn.setMaximumSize(QSize(40, 40))
        self.voiceBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.voiceBtn.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.voiceBtn.setIconSize(QSize(30, 30))
        self.voiceBtn.setVisible(True)

        self.input_mode_frame = QFrame(self.searchFrame)
        self.input_mode_frame.setObjectName("input_mode")
        self.input_mode_frame.setVisible(False)
        self.input_mode_frame.setMaximumHeight(40)

        self.input_mode = QPushButton()
        self.input_mode.setFixedSize(37, 37)
        self.input_mode.setObjectName("input_mode_fr")
        self.input_mode.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.input_mode.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.input_mode.setVisible(False)
        self.input_mode.setIconSize(QSize(18, 18))

        self.input_mode_text = QLabel()
        self.input_mode_text.setObjectName("input_mode_text")
        self.input_mode_text.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        #self.input_mode_text.setVisible(False)
        
        self.submitBtn = QPushButton()
        self.submitBtn.setObjectName("submitBtn")
        self.submitBtn.setMinimumSize(QSize(40, 40))
        self.submitBtn.setMaximumSize(QSize(40, 40))
        self.submitBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.submitBtn.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.submitBtn.setIconSize(QSize(20, 20))

        self.input_mode_frame_layout = QHBoxLayout(self.input_mode_frame)
        self.input_mode_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.input_mode_frame_layout.setSpacing(0)

        self.input_mode_frame_layout.addWidget(
            self.input_mode_text)

        self.input_mode_frame_layout.addWidget(
            self.input_mode)

        self.searchBox = QLineEdit(self.searchFrame)
        self.searchBox.setObjectName("searchBox")
        self.searchBox.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.searchBox.setPlaceholderText("با توانا هر کاری می تونی بکنی!")
        self.searchBox.setFixedSize(QSize(700, 58))

        set_font(self.searchBox, "Bold")

        self.searchBox.setAcceptDrops(True)
        self.searchBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.searchBox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.searchBox.setDragEnabled(False)

        self.searchAreaLayout.addWidget(self.voiceBtn, 0, 0)
        self.searchAreaLayout.addWidget(self.searchBox, 0, 2)
        self.searchAreaLayout.addWidget(self.submitBtn, 0, 4)
        self.searchAreaLayout.addWidget(self.input_mode_frame, 0, 3)

    def _setup_bottom_area(self):
        """ناحیه‌ی پایین پنجره شامل دکمه‌های حالت جستجو و برچسب نسخه را می‌سازد."""
        self.bottomArea = QFrame(self.mainFrame)
        self.bottomArea.setObjectName("bottomArea")
        self.bottomArea.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomArea.setMinimumSize(QSize(1900, 300))

        self.verticalLayout_4 = QVBoxLayout(self.bottomArea)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 1, 0, 1)

        self.modeFrame = QFrame(self.bottomArea)
        self.modeFrame.setObjectName("modeFrame")
        self.modeFrame.setMinimumSize(QSize(605, 40))

        self.modeFrame.setContentsMargins(0, 0, 0, 20)
        self.modeFrame.setFrameShape(QFrame.Shape.NoFrame)

        self.horizontalLayout_3 = QHBoxLayout(self.modeFrame)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.button_group = QButtonGroup(self.modeFrame)
        self.button_group.setExclusive(True)

        self._add_buttons()

        self.show_version = QLabel(self.bottomArea)
        self.show_version.setObjectName("show_version")
        self.show_version.setText(self.set_version())
        self.show_version.setMargin(10)

        self.verticalLayout_4.addWidget(
            self.modeFrame, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop
        )
        self.verticalLayout_4.addWidget(
            self.show_version, 0,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom
        )

        self.topAreaLayout.addWidget(
            self.bottomArea, 3, 0, Qt.AlignmentFlag.AlignHCenter)
        self.topAreaLayout.setRowStretch(3, 3)

    def _add_buttons(self):
        """دکمه‌های میانبر پایین پنجره را بر اساس داده‌ی جدول shortcuts می‌سازد."""
        try:
            shortcuts = database.get_shortcuts()
        except Exception as e:
            print(f"Error loading shortcuts: {e}")
            return

        self._shortcut_widgets = []

        for id_name, width, height, text, tooltip in shortcuts:
            if "separator" in id_name:
                separator = QFrame(self.modeFrame)
                separator.setObjectName("sep")
                separator.setFrameShape(QFrame.Shape.VLine)
                separator.setFrameShadow(QFrame.Shadow.Sunken)
                separator.setFixedSize(width, height)

                self.horizontalLayout_3.addWidget(separator)
                setattr(self, id_name, separator)

                self._shortcut_widgets.append(separator)

            else:
                btn = QRadioButton(text, self.modeFrame)
                btn.setObjectName(id_name)
                btn.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
                btn.setFixedSize(width, height)
                btn.setCheckable(True)
                btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
                set_font(btn, "SemiBold")
                if tooltip:
                    btn.setToolTip(tooltip)

                self.horizontalLayout_3.addWidget(btn)
                self.button_group.addButton(btn)

                setattr(self, id_name, btn)

                self._shortcut_widgets.append(btn)

    def animate_shortcut_buttons_slide_fade_in(self):
        """دکمه‌های میانبر پایین پنجره را با انیمیشن لغزش و محو، یکی‌یکی نمایان می‌کند."""
        delay = 0
        stagger_step = 0

        for widget in getattr(self, "_shortcut_widgets", []):
            QTimer.singleShot(
                delay, lambda w=widget: widget_slide_fade_in(w, "bottom"))
            delay += stagger_step

    def animate_shortcut_buttons_slide_fade_out(self):
        """دکمه‌های میانبر پایین پنجره را با انیمیشن لغزش و محو، یکی‌یکی پنهان می‌کند."""
        delay = 0
        stagger_step = 0

        for widget in getattr(self, "_shortcut_widgets", []):
            QTimer.singleShot(
                delay, lambda w=widget: widget_slide_fade_out(w, "bottom"))
            delay += stagger_step
