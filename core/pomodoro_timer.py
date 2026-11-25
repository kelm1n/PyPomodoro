from PyQt6.QtCore import QObject, QTimer, pyqtSignal


class PomodoroTimer(QObject):
    time_updated = pyqtSignal(int, int)
    mode_changed = pyqtSignal(str)
    session_completed = pyqtSignal(str)

    def __init__(self, settings):
        super().__init__()

        # self.work_time = 25
        # self.short_break = 5
        # self.long_break = 15

        self.work_time = settings["work_time"]
        self.short_break = settings["short_break"]
        self.long_break = settings["long_break"]

        self.session_count = 0
        self.current_mode = "focus"

        self.remain_time = self.work_time * 60
        self.total_time = self.remain_time

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

    def change_duration(self, value):
        if not self.timer.isActive():
            self.work_time = value
            self.remain_time = value * 60
            self.total_time = self.remain_time
            self.update_display()

    def start_timer(self):
        if self.remain_time <= 0:
            self.reset_timer()

        if self.remain_time > 0:
            self.timer.start()

    def pause_timer(self):
        self.timer.stop()

    def reset_timer(self):
        self.timer.stop()

        if self.current_mode == "focus":
            self.remain_time = self.work_time * 60

        elif self.current_mode == "short_break":
            self.remain_time = self.short_break * 60

        else:
            self.remain_time = self.long_break * 60

        self.total_time = self.remain_time
        self.update_display()

    def format_time(self, sec):
        hours = sec // 3600
        minutes = (sec % 3600) // 60
        seconds = sec % 60

        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"

        return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        if self.remain_time > 0:
            self.remain_time -= 1

        if self.remain_time <= 0:
            self.remain_time = 0
            self.timer.stop()

            self.session_completed.emit(self.current_mode)
            self.switch_mode()
            return

        self.update_display()

    def update_display(self):
        self.time_updated.emit(
            self.remain_time,
            self.total_time
        )

    def switch_mode(self):
        if self.current_mode == "focus":
            self.session_count += 1

            if self.session_count % 4 == 0:
                self.current_mode = "long_break"
                self.remain_time = self.long_break * 60

            else:
                self.current_mode = "short_break"
                self.remain_time = self.short_break * 60

        else:
            self.current_mode = "focus"
            self.remain_time = self.work_time * 60

        self.total_time = self.remain_time

        self.mode_changed.emit(self.current_mode)
        self.update_display()