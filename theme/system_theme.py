"""خواندن تم روشن/تیره‌ی سیستم‌عامل و آیکون متناظر برنامه."""
import winreg
from core.database.database import get_app_info
from core.paths.paths import resource_path


class ThemeManager:
    """تعیین تم فعلی ویندوز و آیکون مناسب برای نمایش در پنجره/تری."""
  
    def check_application_appearance_mode(self):
        get_info =get_app_info()
        current_theme = get_info.get("theme")
        
        return current_theme

    def set_application_appearance(self) -> bool:
        current_theme = self.check_application_appearance_mode()

        if current_theme == "Auto":
            return self.get_system_theme()

        elif current_theme == "Dark":
            return True

        elif current_theme == "Light":
            return False

        else:
            print(f"Invalid theme value in database: {current_theme}")
            return False
     
    def get_system_theme(self) -> bool:
        """تم سیستم‌عامل ویندوز را از رجیستری می‌خواند: True برای تیره، False برای روشن."""
        try:
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            ) as key:
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        
            return value == 0
        except (FileNotFoundError, OSError):
            return False

    @staticmethod
    def get_icon_path(is_dark: bool) -> str:
        """مسیر آیکون برنامه را برمی‌گرداند (فعلاً برای هر دو تم یکسان است)."""
        return resource_path("assets", "icons", "tavana.png")
     