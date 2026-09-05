"""اجرای دستورات سیستمی ویندوز و دستورات اختصاصی توانا."""
import logging
import os
import subprocess
import sys
from collections.abc import Callable
from shutil import rmtree
from PySide6.QtWidgets import QApplication

from core.database import database
from core.paths.paths import PROGRAM_ICONS_DIR, resource_path

logger = logging.getLogger(__name__)


class WindowsCommands:
    """دستورات ویندوز، هرکدام از طریق اجرای یک فرمان سیستمی (_run) اجرا می‌شوند."""

    @staticmethod
    def _run(command: str) -> bool:
        """فرمان سیستمی داده‌شده را در پس‌زمینه اجرا می‌کند."""
        try:
            subprocess.Popen(command, shell=True)
            return True
        except Exception as e:
            print(f"Error executing command: {e}")
            return False

    @classmethod
    def control_panel(cls) -> None:
        """پنل کنترل را باز می‌کند."""
        cls._run('control')

    @classmethod
    def calculator(cls) -> None:
        """ماشین‌حساب را باز می‌کند."""
        cls._run('calc')

    @classmethod
    def notepad(cls) -> None:
        """نوت‌پد را باز می‌کند."""
        cls._run('notepad')

    @classmethod
    def command_prompt(cls) -> None:
        """خط فرمان را باز می‌کند."""
        cls._run('start cmd')

    @classmethod
    def task_manager(cls) -> None:
        """مدیریت وظایف را باز می‌کند."""
        cls._run('taskmgr')

    @classmethod
    def registry_editor(cls) -> None:
        """ویرایشگر رجیستری را باز می‌کند."""
        cls._run('regedit')

    @classmethod
    def system_configuration(cls) -> None:
        """پیکربندی سیستم را باز می‌کند."""
        cls._run('msconfig')

    @classmethod
    def device_manager(cls) -> None:
        """مدیریت دستگاه‌ها را باز می‌کند."""
        cls._run('devmgmt.msc')

    @classmethod
    def services(cls) -> None:
        """سرویس‌ها را باز می‌کند."""
        cls._run('services.msc')

    @classmethod
    def network_connections(cls) -> None:
        """اتصالات شبکه را باز می‌کند."""
        cls._run('ncpa.cpl')

    @classmethod
    def programs_and_features(cls) -> None:
        """برنامه‌ها و ویژگی‌ها را باز می‌کند."""
        cls._run('appwiz.cpl')

    @classmethod
    def firewall(cls) -> None:
        """فایروال ویندوز را باز می‌کند."""
        cls._run('firewall.cpl')

    @classmethod
    def system_properties(cls) -> None:
        """ویژگی‌های سیستم را باز می‌کند."""
        cls._run('sysdm.cpl')

    @classmethod
    def my_computer(cls) -> None:
        """این کامپیوتر را باز می‌کند."""
        cls._run('explorer')

    @classmethod
    def paint(cls) -> None:
        """برنامه‌ی Paint را باز می‌کند."""
        cls._run('mspaint')

    @classmethod
    def powershell(cls) -> None:
        """پاورشل را باز می‌کند."""
        cls._run('start powershell')

    @classmethod
    def internet_properties(cls) -> None:
        """ویژگی‌های اینترنت را باز می‌کند."""
        cls._run('inetcpl.cpl')

    @classmethod
    def display_settings(cls) -> None:
        """تنظیمات نمایش را باز می‌کند."""
        cls._run('desk.cpl')

    @classmethod
    def settings_system_display_advanced(cls) -> None:
        """تنظیمات نمایش را باز می‌کند."""
        cls._run('start ms-settings:display-advanced')
        
    @classmethod
    def mouse_properties(cls) -> None:
        """ویژگی‌های ماوس را باز می‌کند."""
        cls._run('main.cpl')

    @classmethod
    def sound_settings(cls) -> None:
        """تنظیمات صدا را باز می‌کند."""
        cls._run('mmsys.cpl')

    @classmethod
    def power_options(cls) -> None:
        """گزینه‌های برق را باز می‌کند."""
        cls._run('powercfg.cpl')

    @classmethod
    def date_and_time(cls) -> None:
        """تنظیمات تاریخ و زمان را باز می‌کند."""
        cls._run('timedate.cpl')

    @classmethod
    def disk_management(cls) -> None:
        """مدیریت دیسک را باز می‌کند."""
        cls._run('diskmgmt.msc')

    @classmethod
    def computer_management(cls) -> None:
        """مدیریت کامپیوتر را باز می‌کند."""
        cls._run('compmgmt.msc')

    @classmethod
    def event_viewer(cls) -> None:
        """نمایشگر رویداد را باز می‌کند."""
        cls._run('eventvwr.msc')

    @classmethod
    def local_security_policy(cls) -> None:
        """سیاست امنیت محلی را باز می‌کند."""
        cls._run('secpol.msc')

    @classmethod
    def local_group_policy(cls) -> None:
        """ویرایشگر خط‌مشی گروه محلی را باز می‌کند."""
        cls._run('gpedit.msc')

    @classmethod
    def local_users_and_groups(cls) -> None:
        """کاربران و گروه‌های محلی را باز می‌کند."""
        cls._run('lusrmgr.msc')

    @classmethod
    def performance_monitor(cls) -> None:
        """نمایشگر کارایی را باز می‌کند."""
        cls._run('perfmon.msc')

    @classmethod
    def resource_monitor(cls) -> None:
        """نمایشگر منابع را باز می‌کند."""
        cls._run('resmon')

    @classmethod
    def task_scheduler(cls) -> None:
        """زمان‌بند وظایف را باز می‌کند."""
        cls._run('taskschd.msc')

    @classmethod
    def certificates(cls) -> None:
        """مدیریت گواهی‌ها را باز می‌کند."""
        cls._run('certmgr.msc')

    @classmethod
    def component_services(cls) -> None:
        """سرویس‌های اجزا را باز می‌کند."""
        cls._run('dcomcnfg')

    @classmethod
    def odbc_data_sources(cls) -> None:
        """منابع داده‌ی ODBC را باز می‌کند."""
        cls._run('odbcad32')

    @classmethod
    def system_information(cls) -> None:
        """اطلاعات سیستم را باز می‌کند."""
        cls._run('msinfo32')

    @classmethod
    def directx_diagnostic(cls) -> None:
        """ابزار تشخیص DirectX را باز می‌کند."""
        cls._run('dxdiag')

    @classmethod
    def disk_cleanup(cls) -> None:
        """پاک‌سازی دیسک را باز می‌کند."""
        cls._run('cleanmgr')

    @classmethod
    def defragment(cls) -> None:
        """یکپارچه‌ساز دیسک را باز می‌کند."""
        cls._run('dfrgui')

    @classmethod
    def character_map(cls) -> None:
        """نقشه‌ی نویسه‌ها را باز می‌کند."""
        cls._run('charmap')

    @classmethod
    def wordpad(cls) -> None:
        """وردپد را باز می‌کند."""
        cls._run('wordpad')

    @classmethod
    def snipping_tool(cls) -> None:
        """ابزار برش را باز می‌کند."""
        cls._run('snippingtool')

    @classmethod
    def on_screen_keyboard(cls) -> None:
        """صفحه‌کلید روی صفحه را باز می‌کند."""
        cls._run('osk')

    @classmethod
    def magnifier(cls) -> None:
        """ذره‌بین را باز می‌کند."""
        cls._run('magnify')

    @classmethod
    def narrator(cls) -> None:
        """روایتگر را باز می‌کند."""
        cls._run('narrator')

    @classmethod
    def remote_desktop(cls) -> None:
        """اتصال دسکتاپ از راه دور را باز می‌کند."""
        cls._run('mstsc')

    @classmethod
    def windows_media_player(cls) -> None:
        """پخش‌کننده‌ی رسانه‌ی ویندوز را باز می‌کند."""
        cls._run('wmplayer')

    @classmethod
    def windows_fax_and_scan(cls) -> None:
        """فکس و اسکن ویندوز را باز می‌کند."""
        cls._run('wfs')

    @classmethod
    def windows_mobility_center(cls) -> None:
        """مرکز تحرک ویندوز را باز می‌کند."""
        cls._run('mblctr')

    @classmethod
    def presentation_settings(cls) -> None:
        """تنظیمات ارائه را باز می‌کند."""
        cls._run('PresentationSettings')

    @classmethod
    def color_management(cls) -> None:
        """مدیریت رنگ را باز می‌کند."""
        cls._run('colorcpl')

    @classmethod
    def credential_manager(cls) -> None:
        """مدیریت اعتبارنامه‌ها را باز می‌کند."""
        cls._run('control /name Microsoft.CredentialManager')

    @classmethod
    def font_viewer(cls) -> None:
        """نمایشگر فونت را باز می‌کند."""
        cls._run('control.exe /name Microsoft.fonts')

    @classmethod
    def windows_update_legacy(cls) -> None:
        """بروزرسانی ویندوز (نسخه‌ی قدیمی) را باز می‌کند."""
        cls._run('wuapp')

    @classmethod
    def action_center(cls) -> None:
        """مرکز اقدام را باز می‌کند."""
        cls._run('wscui.cpl')

    @classmethod
    def ease_of_access_center(cls) -> None:
        """مرکز سهولت دسترسی را باز می‌کند."""
        cls._run('utilman')

    @classmethod
    def troubleshooting(cls) -> None:
        """عیب‌یابی را باز می‌کند."""
        cls._run('control.exe /name Microsoft.Troubleshooting')

    @classmethod
    def sync_center(cls) -> None:
        """مرکز همگام‌سازی را باز می‌کند."""
        cls._run('mobsync')

    @classmethod
    def windows_features(cls) -> None:
        """ویژگی‌های ویندوز را باز می‌کند."""
        cls._run('optionalfeatures')

    @classmethod
    def shared_folders(cls) -> None:
        """پوشه‌های اشتراکی را باز می‌کند."""
        cls._run('fsmgmt.msc')

    @classmethod
    def hyper_v_manager(cls) -> None:
        """مدیریت Hyper-V را باز می‌کند."""
        cls._run('virtmgmt.msc')

    @classmethod
    def windows_sandbox(cls) -> None:
        """جعبه‌شنی ویندوز را باز می‌کند."""
        cls._run('WindowsSandbox')

    @classmethod
    def winver(cls) -> None:
        """پنجره‌ی نسخه‌ی ویندوز (winver) را نمایش می‌دهد."""
        cls._run('winver')

    @classmethod
    def environment_variables(cls) -> None:
        """پنجره‌ی ویرایش متغیرهای محیطی را باز می‌کند."""
        cls._run('rundll32 sysdm.cpl,EditEnvironmentVariables')

    @classmethod
    def network_diagnostics(cls) -> None:
        """ابزار عیب‌یابی شبکه‌ی ویندوز را اجرا می‌کند."""
        cls._run('msdt.exe -id NetworkDiagnosticsNetworkAdapter')

    @classmethod
    def ip_config_cmd(cls) -> None:
        """پیکربندی IP را در پنجره‌ی خط فرمان نمایش می‌دهد."""
        cls._run('start cmd /k ipconfig /all')

    @classmethod
    def set_proxy(cls) -> None:
        """تنظیمات پراکسی را باز می‌کند."""
        cls._run('start ms-settings:network-proxy')

    @classmethod
    def settings_menu(cls) -> None:
        """منوی تنظیمات را باز می‌کند."""
        cls._run('start ms-settings:home')

    @classmethod
    def settings_system(cls) -> None:
        """تنظیمات سیستم را باز می‌کند."""
        cls._run('start ms-settings:system')

    @classmethod
    def settings_system_display(cls) -> None:
        """تنظیمات نمایش را باز می‌کند."""
        cls._run('start ms-settings:display')

    @classmethod
    def settings_system_sound(cls) -> None:
        """تنظیمات صدا را باز می‌کند."""
        cls._run('start ms-settings:sound')

    @classmethod
    def settings_system_sound_devices(cls) -> None:
        """تنظیمات صدا را باز می‌کند."""
        cls._run('start ms-settings:sound-devices')
           
    @classmethod
    def settings_system_notifications(cls) -> None:
        """تنظیمات اعلان‌ها را باز می‌کند."""
        cls._run('start ms-settings:notifications')

    @classmethod
    def settings_system_power(cls) -> None:
        """تنظیمات برق و باتری را باز می‌کند."""
        cls._run('start ms-settings:powersleep')

    @classmethod
    def settings_system_storage(cls) -> None:
        """تنظیمات فضای ذخیره‌سازی را باز می‌کند."""
        cls._run('start ms-settings:storagesense')

    @classmethod
    def settings_system_multitasking(cls) -> None:
        """تنظیمات چندوظیفگی را باز می‌کند."""
        cls._run('start ms-settings:multitasking')

    @classmethod
    def settings_system_activation(cls) -> None:
        """تنظیمات فعال‌سازی را باز می‌کند."""
        cls._run('start ms-settings:activation')

    @classmethod
    def settings_system_troubleshoot(cls) -> None:
        """تنظیمات عیب‌یابی را باز می‌کند."""
        cls._run('start ms-settings:troubleshoot')

    @classmethod
    def settings_system_remote_desktop(cls) -> None:
        """تنظیمات دسکتاپ از راه دور را باز می‌کند."""
        cls._run('start ms-settings:remotedesktop')

    @classmethod
    def settings_system_clipboard(cls) -> None:
        """تنظیمات کلیپ‌بورد را باز می‌کند."""
        cls._run('start ms-settings:clipboard')

    @classmethod
    def settings_system_about(cls) -> None:
        """تنظیمات درباره‌ی سیستم را باز می‌کند."""
        cls._run('start ms-settings:about')

    @classmethod
    def settings_system_recovery(cls) -> None:
        """تنظیمات بازیابی را باز می‌کند."""
        cls._run('start ms-settings:recovery')

    @classmethod
    def settings_system_bluetooth(cls) -> None:
        """تنظیمات بلوتوث را باز می‌کند."""
        cls._run('start ms-settings:bluetooth')

    @classmethod
    def settings_system_printers(cls) -> None:
        """تنظیمات چاپگرها و اسکنرها را باز می‌کند."""
        cls._run('start ms-settings:printers')

    @classmethod
    def settings_mouse(cls) -> None:
        """تنظیمات ماوس را باز می‌کند."""
        cls._run('start ms-settings:mousetouchpad')

    @classmethod
    def settings_touchpad(cls) -> None:
        """تنظیمات تاچ‌پد را باز می‌کند."""
        cls._run('start ms-settings:devices-touchpad')

    @classmethod
    def settings_usb(cls) -> None:
        """تنظیمات USB را باز می‌کند."""
        cls._run('start ms-settings:usb')

    @classmethod
    def settings_system_network(cls) -> None:
        """تنظیمات شبکه و اینترنت را باز می‌کند."""
        cls._run('start ms-settings:network')

    @classmethod
    def settings_network_wifi(cls) -> None:
        """تنظیمات وای‌فای را باز می‌کند."""
        cls._run('start ms-settings:network-wifi')

    @classmethod
    def settings_system_ethernet(cls) -> None:
        """تنظیمات اترنت را باز می‌کند."""
        cls._run('start ms-settings:network-ethernet')

    @classmethod
    def settings_system_vpn(cls) -> None:
        """تنظیمات VPN را باز می‌کند."""
        cls._run('start ms-settings:network-vpn')

    @classmethod
    def settings_network_hotspot(cls) -> None:
        """تنظیمات اشتراک اینترنت موبایل را باز می‌کند."""
        cls._run('start ms-settings:network-mobilehotspot')

    @classmethod
    def settings_system_airplane(cls) -> None:
        """تنظیمات حالت هواپیما را باز می‌کند."""
        cls._run('start ms-settings:network-airplanemode')

    @classmethod
    def settings_system_personalization(cls) -> None:
        """تنظیمات شخصی‌سازی را باز می‌کند."""
        cls._run('start ms-settings:personalization')

    @classmethod
    def settings_personalization_background(cls) -> None:
        """تنظیمات پس‌زمینه را باز می‌کند."""
        cls._run('start ms-settings:personalization-background')

    @classmethod
    def settings_system_colors(cls) -> None:
        """تنظیمات رنگ‌ها را باز می‌کند."""
        cls._run('start ms-settings:colors')

    @classmethod
    def settings_system_themes(cls) -> None:
        """تنظیمات پوسته‌ها را باز می‌کند."""
        cls._run('start ms-settings:themes')

    @classmethod
    def settings_system_lockscreen(cls) -> None:
        """تنظیمات صفحه‌ی قفل را باز می‌کند."""
        cls._run('start ms-settings:lockscreen')

    @classmethod
    def settings_system_taskbar(cls) -> None:
        """تنظیمات نوار وظیفه را باز می‌کند."""
        cls._run('start ms-settings:taskbar')

    @classmethod
    def settings_fonts(cls) -> None:
        """تنظیمات فونت‌ها را باز می‌کند."""
        cls._run('start ms-settings:fonts')

    @classmethod
    def settings_system_appsfeatures(cls) -> None:
        """تنظیمات برنامه‌ها و ویژگی‌ها را باز می‌کند."""
        cls._run('start ms-settings:appsfeatures')

    @classmethod
    def settings_system_defaultapps(cls) -> None:
        """تنظیمات برنامه‌های پیش‌فرض را باز می‌کند."""
        cls._run('start ms-settings:defaultapps')

    @classmethod
    def settings_startup_apps(cls) -> None:
        """تنظیمات برنامه‌های آغازین را باز می‌کند."""
        cls._run('start ms-settings:startupapps')

    @classmethod
    def settings_accounts(cls) -> None:
        """تنظیمات حساب‌ها را باز می‌کند."""
        cls._run('start ms-settings:accounts')

    @classmethod
    def settings_system_yourinfo(cls) -> None:
        """تنظیمات اطلاعات شما را باز می‌کند."""
        cls._run('start ms-settings:yourinfo')

    @classmethod
    def settings_system_signinoptions(cls) -> None:
        """گزینه‌های ورود را باز می‌کند."""
        cls._run('start ms-settings:signinoptions')

    @classmethod
    def settings_system_familygroup(cls) -> None:
        """تنظیمات خانواده و سایر کاربران را باز می‌کند."""
        cls._run('start ms-settings:family-group')

    @classmethod
    def settings_system_backup(cls) -> None:
        """تنظیمات پشتیبان‌گیری ویندوز را باز می‌کند."""
        cls._run('start ms-settings:backup')

    @classmethod
    def settings_system_dateandtime(cls) -> None:
        """تنظیمات تاریخ و زمان را باز می‌کند."""
        cls._run('start ms-settings:dateandtime')

    @classmethod
    def settings_system_regionlanguage(cls) -> None:
        """تنظیمات زبان و منطقه را باز می‌کند."""
        cls._run('start ms-settings:regionlanguage')

    @classmethod
    def settings_system_gamebar(cls) -> None:
        """تنظیمات نوار بازی ایکس‌باکس را باز می‌کند."""
        cls._run('start ms-settings:gaming-gamebar')

    @classmethod
    def settings_system_gamemode(cls) -> None:
        """تنظیمات حالت بازی را باز می‌کند."""
        cls._run('start ms-settings:gaming-gamemode')

    @classmethod
    def settings_system_privacyandsecurity(cls) -> None:
        """تنظیمات حریم خصوصی و امنیت را باز می‌کند."""
        cls._run('start ms-settings:privacy')

    @classmethod
    def settings_face_recognition(cls) -> None:
        """تنظیمات حریم خصوصی و امنیت را باز می‌کند."""
        cls._run('start ms-settings:signinoptions-launchfaceenrollment')
    @classmethod
    def settings_fingerprint_recognition(cls) -> None:
        """تنظیمات حریم خصوصی و امنیت را باز می‌کند."""
        cls._run('start ms-settings:signinoptions-launchfingerprintenrollment')

    @classmethod
    def settings_privacy_location(cls) -> None:
        """تنظیمات حریم خصوصی موقعیت مکانی را باز می‌کند."""
        cls._run('start ms-settings:privacy-location')

    @classmethod
    def settings_privacy_camera(cls) -> None:
        """تنظیمات حریم خصوصی دوربین را باز می‌کند."""
        cls._run('start ms-settings:privacy-webcam')

    @classmethod
    def settings_privacy_microphone(cls) -> None:
        """تنظیمات حریم خصوصی میکروفون را باز می‌کند."""
        cls._run('start ms-settings:privacy-microphone')

    @classmethod
    def settings_system_windowsdefender(cls) -> None:
        """امنیت ویندوز را باز می‌کند."""
        cls._run('start ms-settings:windowsdefender')

    @classmethod
    def settings_system_windowsupdate(cls) -> None:
        """تنظیمات بروزرسانی ویندوز را باز می‌کند."""
        cls._run('start ms-settings:windowsupdate')

    @classmethod
    def settings_system_ease_of_access(cls) -> None:
        """تنظیمات دسترسی‌پذیری را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess')

    @classmethod
    def settings_ease_of_access_narrator(cls) -> None:
        """تنظیمات دسترسی‌پذیری را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-narrator')
    @classmethod
    def shutdown_windows(cls) -> None:
        """ویندوز را خاموش می‌کند."""
        cls._run(['shutdown', '/s', '/t', '0'])

    @classmethod
    def restart_windows(cls) -> None:
        """ویندوز را ری‌استارت می‌کند."""
        cls._run(['shutdown', '/r', '/t', '0'])

    @classmethod
    def app_data(cls) -> None:
        """پوشه‌ی appdata\\roaming را در File Explorer باز می‌کند."""
        os.startfile(os.path.expandvars('%appdata%'))

    @classmethod
    def windows_tmp_files(cls) -> None:
        """پوشه‌ی appdata\\roaming را در File Explorer باز می‌کند."""
        os.startfile(os.path.expandvars('temp'))

    @classmethod
    def user_tmp_files(cls) -> None:
        """پوشه‌ی appdata\\roaming را در File Explorer باز می‌کند."""
        os.startfile(os.path.expandvars('%temp%'))
                
    @classmethod
    def sleep_windows(cls) -> None:
        """ویندوز را به حالت خواب می‌برد."""
        cls._run([
            "powershell", "-command",
            "Add-Type -AssemblyName System.Windows.Forms; "
            "[System.Windows.Forms.Application]::SetSuspendState('Suspend', $false, $false)"
        ])

    @classmethod
    def settings_apps_for_websites(cls) -> None:
        """تنظیم مربوط به appsforwebsites را باز می‌کند."""
        cls._run('start ms-settings:appsforwebsites')


    @classmethod
    def settings_autoplay(cls) -> None:
        """تنظیم مربوط به autoplay را باز می‌کند."""
        cls._run('start ms-settings:autoplay')


    @classmethod
    def settings_camera(cls) -> None:
        """تنظیم مربوط به camera را باز می‌کند."""
        cls._run('start ms-settings:camera')


    @classmethod
    def settings_connected_devices(cls) -> None:
        """تنظیم مربوط به connecteddevices را باز می‌کند."""
        cls._run('start ms-settings:connecteddevices')


    @classmethod
    def settings_ease_of_access_audio(cls) -> None:
        """تنظیم مربوط به easeofaccess-audio را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-audio')


    @classmethod
    def settings_ease_of_access_closedcaptioning(cls) -> None:
        """تنظیم مربوط به easeofaccess-closedcaptioning را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-closedcaptioning')


    @classmethod
    def settings_ease_of_access_colorfilter(cls) -> None:
        """تنظیم مربوط به easeofaccess-colorfilter را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-colorfilter')


    @classmethod
    def settings_ease_of_access_eyecontrol(cls) -> None:
        """تنظیم مربوط به easeofaccess-eyecontrol را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-eyecontrol')


    @classmethod
    def settings_ease_of_access_highcontrast(cls) -> None:
        """تنظیم مربوط به easeofaccess-highcontrast را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-highcontrast')


    @classmethod
    def settings_ease_of_access_mouse(cls) -> None:
        """تنظیم مربوط به easeofaccess-mouse را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-mouse')


    @classmethod
    def settings_game_dvr(cls) -> None:
        """تنظیم مربوط به gaming-gamedvr را باز می‌کند."""
        cls._run('start ms-settings:gaming-gamedvr')


    @classmethod
    def settings_mobile_devices(cls) -> None:
        """تنظیم مربوط به mobile-devices را باز می‌کند."""
        cls._run('start ms-settings:mobile-devices')


    @classmethod
    def settings_network_advanced(cls) -> None:
        """تنظیم مربوط به network-advancedsettings را باز می‌کند."""
        cls._run('start ms-settings:network-advancedsettings')


    @classmethod
    def settings_network_cellular(cls) -> None:
        """تنظیم مربوط به network-cellular را باز می‌کند."""
        cls._run('start ms-settings:network-cellular')


    @classmethod
    def settings_network_dialup(cls) -> None:
        """تنظیم مربوط به network-dialup را باز می‌کند."""
        cls._run('start ms-settings:network-dialup')


    @classmethod
    def settings_offline_maps(cls) -> None:
        """تنظیم مربوط به maps را باز می‌کند."""
        cls._run('start ms-settings:maps')


    @classmethod
    def settings_pen(cls) -> None:
        """تنظیم مربوط به pen را باز می‌کند."""
        cls._run('start ms-settings:pen')


    @classmethod
    def settings_personalization_start(cls) -> None:
        """تنظیم مربوط به personalization-start را باز می‌کند."""
        cls._run('start ms-settings:personalization-start')


    @classmethod
    def settings_privacy_account_info(cls) -> None:
        """تنظیم مربوط به privacy-accountinfo را باز می‌کند."""
        cls._run('start ms-settings:privacy-accountinfo')


    @classmethod
    def settings_privacy_app_diagnostics(cls) -> None:
        """تنظیم مربوط به privacy-appdiagnostics را باز می‌کند."""
        cls._run('start ms-settings:privacy-appdiagnostics')


    @classmethod
    def settings_privacy_background_apps(cls) -> None:
        """تنظیم مربوط به privacy-backgroundapps را باز می‌کند."""
        cls._run('start ms-settings:privacy-backgroundapps')


    @classmethod
    def settings_privacy_calendar(cls) -> None:
        """تنظیم مربوط به privacy-calendar را باز می‌کند."""
        cls._run('start ms-settings:privacy-calendar')


    @classmethod
    def settings_privacy_call_history(cls) -> None:
        """تنظیم مربوط به privacy-callhistory را باز می‌کند."""
        cls._run('start ms-settings:privacy-callhistory')


    @classmethod
    def settings_privacy_contacts(cls) -> None:
        """تنظیم مربوط به privacy-contacts را باز می‌کند."""
        cls._run('start ms-settings:privacy-contacts')


    @classmethod
    def settings_privacy_diagnostics(cls) -> None:
        """تنظیم مربوط به privacy-feedback را باز می‌کند."""
        cls._run('start ms-settings:privacy-feedback')


    @classmethod
    def settings_privacy_documents(cls) -> None:
        """تنظیم مربوط به privacy-documents را باز می‌کند."""
        cls._run('start ms-settings:privacy-documents')


    @classmethod
    def settings_privacy_email(cls) -> None:
        """تنظیم مربوط به privacy-email را باز می‌کند."""
        cls._run('start ms-settings:privacy-email')


    @classmethod
    def settings_privacy_file_system(cls) -> None:
        """تنظیم مربوط به privacy-broadfilesystemaccess را باز می‌کند."""
        cls._run('start ms-settings:privacy-broadfilesystemaccess')


    @classmethod
    def settings_privacy_messaging(cls) -> None:
        """تنظیم مربوط به privacy-messaging را باز می‌کند."""
        cls._run('start ms-settings:privacy-messaging')


    @classmethod
    def settings_privacy_notifications(cls) -> None:
        """تنظیم مربوط به privacy-notifications را باز می‌کند."""
        cls._run('start ms-settings:privacy-notifications')


    @classmethod
    def settings_privacy_other_devices(cls) -> None:
        """تنظیم مربوط به privacy-customdevices را باز می‌کند."""
        cls._run('start ms-settings:privacy-customdevices')


    @classmethod
    def settings_privacy_pictures(cls) -> None:
        """تنظیم مربوط به privacy-pictures را باز می‌کند."""
        cls._run('start ms-settings:privacy-pictures')


    @classmethod
    def settings_privacy_radios(cls) -> None:
        """تنظیم مربوط به privacy-radios را باز می‌کند."""
        cls._run('start ms-settings:privacy-radios')


    @classmethod
    def settings_privacy_speech(cls) -> None:
        """تنظیم مربوط به privacy-speech را باز می‌کند."""
        cls._run('start ms-settings:privacy-speech')


    @classmethod
    def settings_privacy_tasks(cls) -> None:
        """تنظیم مربوط به privacy-tasks را باز می‌کند."""
        cls._run('start ms-settings:privacy-tasks')


    @classmethod
    def settings_privacy_videos(cls) -> None:
        """تنظیم مربوط به privacy-videos را باز می‌کند."""
        cls._run('start ms-settings:privacy-videos')


    @classmethod
    def settings_signin_dynamic_lock(cls) -> None:
        """تنظیم مربوط به signinoptions-dynamiclock را باز می‌کند."""
        cls._run('start ms-settings:signinoptions-dynamiclock')


    @classmethod
    def settings_signin_security_key(cls) -> None:
        """تنظیم مربوط به signinoptions-launchsecuritykeyenrollment را باز می‌کند."""
        cls._run('start ms-settings:signinoptions-launchsecuritykeyenrollment')


    @classmethod
    def settings_system_apps_volume(cls) -> None:
        """تنظیم مربوط به apps-volume را باز می‌کند."""
        cls._run('start ms-settings:apps-volume')


    @classmethod
    def settings_system_display_graphics(cls) -> None:
        """تنظیم مربوط به display-advancedgraphics را باز می‌کند."""
        cls._run('start ms-settings:display-advancedgraphics')


    @classmethod
    def settings_system_ease_of_access_display(cls) -> None:
        """تنظیم مربوط به easeofaccess-display را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-display')


    @classmethod
    def settings_system_ease_of_access_keyboard(cls) -> None:
        """تنظیم مربوط به easeofaccess-keyboard را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-keyboard')


    @classmethod
    def settings_system_ease_of_access_magnifier(cls) -> None:
        """تنظیم مربوط به easeofaccess-magnifier را باز می‌کند."""
        cls._run('start ms-settings:easeofaccess-magnifier')


    @classmethod
    def settings_system_emailandaccounts(cls) -> None:
        """تنظیم مربوط به emailandaccounts را باز می‌کند."""
        cls._run('start ms-settings:emailandaccounts')


    @classmethod
    def settings_system_focus_assist(cls) -> None:
        """تنظیم مربوط به quiethours را باز می‌کند."""
        cls._run('start ms-settings:quiethours')


    @classmethod
    def settings_system_nightlight(cls) -> None:
        """تنظیم مربوط به nightlight را باز می‌کند."""
        cls._run('start ms-settings:nightlight')


    @classmethod
    def settings_system_optionalfeatures(cls) -> None:
        """تنظیم مربوط به optionalfeatures را باز می‌کند."""
        cls._run('start ms-settings:optionalfeatures')


    @classmethod
    def settings_system_project(cls) -> None:
        """تنظیم مربوط به project را باز می‌کند."""
        cls._run('start ms-settings:project')


    @classmethod
    def settings_system_save_locations(cls) -> None:
        """تنظیم مربوط به savelocations را باز می‌کند."""
        cls._run('start ms-settings:savelocations')


    @classmethod
    def settings_system_speech(cls) -> None:
        """تنظیم مربوط به speech را باز می‌کند."""
        cls._run('start ms-settings:speech')


    @classmethod
    def settings_system_storage_policies(cls) -> None:
        """تنظیم مربوط به storagepolicies را باز می‌کند."""
        cls._run('start ms-settings:storagepolicies')


    @classmethod
    def settings_system_workplace(cls) -> None:
        """تنظیم مربوط به workplace را باز می‌کند."""
        cls._run('start ms-settings:workplace')


    @classmethod
    def settings_typing(cls) -> None:
        """تنظیم مربوط به typing را باز می‌کند."""
        cls._run('start ms-settings:typing')


    @classmethod
    def settings_video_playback(cls) -> None:
        """تنظیم مربوط به videoplayback را باز می‌کند."""
        cls._run('start ms-settings:videoplayback')


    @classmethod
    def settings_windowsupdate_history(cls) -> None:
        """تنظیم مربوط به windowsupdate-history را باز می‌کند."""
        cls._run('start ms-settings:windowsupdate-history')


    @classmethod
    def settings_windowsupdate_options(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start ms-settings:windowsupdate-options')

    @classmethod
    def file_explorer_options(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start control folders')
 
 
    @classmethod
    def Malware_Removal_Tool(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start mrt')

    @classmethod
    def Windows_memory_checker(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start mdsched')        


    @classmethod
    def admin_tools(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start control admintools')     

    @classmethod
    def Bluetooth_Transfer_Wizard(cls) -> None:
        """تنظیم مربوط به windowsupdate-options را باز می‌کند."""
        cls._run('start fsquirt') 
                                   
    @classmethod
    def settings_windowsupdate_restartoptions(cls) -> None:
        """تنظیم مربوط به windowsupdate-restartoptions را باز می‌کند."""
        cls._run('start ms-settings:windowsupdate-restartoptions')


    @classmethod
    def settings_xbox_networking(cls) -> None:
        """تنظیم مربوط به gaming-xboxnetworking را باز می‌کند."""
        cls._run('start ms-settings:gaming-xboxnetworking')


class TavanaCommands(WindowsCommands):
    """دستورات اختصاصی برنامه‌ی توانا (پاک‌کردن تاریخچه، خروج از برنامه و ارتباط با هوش مصنوعی)."""

    @classmethod
    def clear_search_history(cls) -> None:
        """تاریخچه‌ی تایپ را پاک می‌کند و برنامه را برای اعمال تغییر مجدداً راه‌اندازی می‌کند."""
        try:
            database.clear_type_history()
            print("✅ Search history cleared")

            QApplication.quit()

            open_app = sys.executable
            subprocess.Popen([open_app] + sys.argv)

            sys.exit(0)

        except Exception as e:
            print(f"Error clearing history: {e}")

    @classmethod
    def clear_directories(cls) -> None:
        """کش مسیرها و آیکون‌های استخراج‌شده را پاک می‌کند و برنامه را برای اعمال تغییر مجدداً راه‌اندازی می‌کند."""
        try:
            database.clear_directory_history()
            rmtree(PROGRAM_ICONS_DIR, ignore_errors=True)
            print("✅ Directories is cleaned!")

            QApplication.quit()

            open_app = sys.executable
            subprocess.Popen([open_app] + sys.argv)

            sys.exit(0)

        except Exception as e:
            print(f"Error clearing history: {e}")

    @classmethod
    def quit_from_app(cls) -> None:
        """از برنامه خارج می‌شود."""
        sys.exit(0)

    @classmethod
    def ask_ai(cls, question: str) -> str:
        """سؤال کاربر را از طریق یک سرویس هوش مصنوعی سازگار با OpenAI می‌پرسد و پاسخ را برمی‌گرداند."""
        api_key = os.environ.get("TAVANA_AI_API_KEY")
        if not api_key:
            logger.warning(
                "TAVANA_AI_API_KEY تنظیم نشده؛ درخواست ask_ai نادیده گرفته شد.")
            return "خطا: کلید API تنظیم نشده است (TAVANA_AI_API_KEY)."

        try:
            from openai import OpenAI
        except ImportError:
            logger.error("پکیج openai نصب نیست.")
            return "خطا: پکیج openai نصب نشده است."

        try:
            client = OpenAI(
                base_url=os.environ.get(
                    "TAVANA_AI_BASE_URL", "https://api.gapgpt.app/v1"),
                api_key=api_key,
            )
            response = client.chat.completions.create(
                model=os.environ.get("TAVANA_AI_MODEL", "gemini-2.5-pro"),
                messages=[{"role": "user", "content": question}],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"خطا در فراخوانی ask_ai: {e}")
            return f"خطا در ارتباط با سرویس هوش مصنوعی: {e}"

def _load_commands(commands_data, handler):
    commands = {}

    for key, command_data in commands_data.items():
        if isinstance(command_data, dict):
            func_name = command_data["action"]
        else:
            func_name = command_data

        func = getattr(handler, func_name, None)

        if func:
            commands[key] = func

    return commands


def load_windows_commands() -> dict[str, Callable]:
    """دستورات ویندوز را از دیتابیس بخوان و نگاشت کلیدواژه → تابع اجراکننده را برگردان."""
    try:
        commands_data = database.get_windows_commands()
    except Exception as e:
        logger.error(f"Error loading windows commands: {e}")
        return {}
    return _load_commands(commands_data, WindowsCommands())


def load_tavana_commands() -> dict[str, Callable]:
    """دستورات اختصاصی توانا را از دیتابیس بخوان و نگاشت کلیدواژه → تابع اجراکننده را برگردان."""
    try:
        commands_data = database.get_tavana_commands()
    except Exception as e:
        logger.error(f"Error loading tavana commands: {e}")
        return {}
    return _load_commands(commands_data, TavanaCommands())