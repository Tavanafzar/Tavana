"""جلوگیری از اجرای هم‌زمان چند نمونه از توانا (single instance)."""

from PySide6.QtCore import QObject, Signal
from PySide6.QtNetwork import QLocalServer, QLocalSocket

# یک نام یکتا برای سرور محلی؛ اگر برنامه‌های دیگری هم از همین روش استفاده کنند
# تداخل پیش نیاید.
_SERVER_NAME = "Tavana-SingleInstance-8f2c1a4e"


class SingleInstanceGuard(QObject):
    """با یک QLocalServer/QLocalSocket تشخیص می‌دهد که آیا نمونه‌ی دیگری از برنامه
    در حال اجراست یا نه. اگر نمونه‌ای موجود باشد، پیام «نمایش بده» را برایش می‌فرستد
    تا پنجره‌ی همان نمونه ظاهر شود؛ نمونه‌ی جدید باید بلافاصله بسته شود.
    """

    show_requested = Signal()

    def __init__(self):
        super().__init__()
        self._server: QLocalServer | None = None
        self._pending_connections = []

    def try_acquire(self) -> bool:
        """اگر نمونه‌ی دیگری در حال اجرا باشد True برمی‌گرداند (یعنی این نمونه باید
        خارج شود). در غیر این صورت سرور محلی را راه‌اندازی و False برمی‌گرداند.
        """

        probe = QLocalSocket()
        probe.connectToServer(_SERVER_NAME)
        if probe.waitForConnected(200):
            probe.write(b"show")
            probe.flush()
            probe.waitForBytesWritten(200)
            probe.disconnectFromServer()
            return True

        # اگر نمونه‌ی قبلی بدون بسته‌شدن تمیز (مثلاً کرش) از بین رفته باشد، ممکن است
        # فایل سرور محلی باقی مانده باشد؛ برای اطمینان حذفش می‌کنیم.
        QLocalServer.removeServer(_SERVER_NAME)

        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._on_new_connection)
        self._server.listen(_SERVER_NAME)
        return False

    def _on_new_connection(self):
        conn = self._server.nextPendingConnection()
        if conn is None:
            return
        self._pending_connections.append(conn)
        conn.readyRead.connect(lambda c=conn: self._handle_message(c))
        conn.disconnected.connect(lambda c=conn: self._cleanup_connection(c))

    def _handle_message(self, conn):
        data = bytes(conn.readAll())
        if data == b"show":
            self.show_requested.emit()
        conn.disconnectFromServer()

    def _cleanup_connection(self, conn):
        if conn in self._pending_connections:
            self._pending_connections.remove(conn)
        conn.deleteLater()