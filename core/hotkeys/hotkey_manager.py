
from PySide6.QtGui import QKeySequence, QShortcut
from pynput import keyboard


class HotkeyManager:
    def __init__(self, window) -> None:
        super().__init__()
        self.window = window

        try:
            self.hotkey_listener = keyboard.GlobalHotKeys({
                '<ctrl>+<space>': lambda: self.window.toggle_signal.emit(),
            })
        except:
            print(
                "something is wrong in core/hotkeys/hotkey_manager.py | register_global_hotkeys(self):")

    def return_the_answer_hotkey(self):

        submit_answer = QShortcut(QKeySequence("Return"), self.window)
        submit_answer.activated.connect(self.window.submit_signal.emit)

        self.window.ui.submitBtn.clicked.connect(
            self.window.submit_signal.emit)
