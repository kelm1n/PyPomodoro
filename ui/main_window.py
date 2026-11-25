from threading import Thread
from datetime import date

from playsound3 import playsound

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QSpinBox,
    QProgressBar, QApplication,
)

from core.pomodoro_timer import PomodoroTimer
from storage.statistics_manager import load_statistics, add_focus_session
from ui.style import APP_STYLE
from ui.tray_manager import TrayManager
from utils.paths import asset_path
from storage.storage_manager import save_settings


class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()

        self.settings = settings

        self.pomodoro = PomodoroTimer(settings)

        self.pomodoro.time_updated.connect(
            self.update_timer_display
        )

        self.pomodoro.mode_changed.connect(
            self.update_mode_display
        )

        self.pomodoro.session_completed.connect(
            self.on_session_completed
        )

        self.statistics = load_statistics()

        self.init_ui()
        self.setStyleSheet(APP_STYLE)

        self.tray = TrayManager(
            self,
            on_open=self.show_window,
            on_exit=QApplication.instance().quit,
        )

        self.update_timer_display(
            self.pomodoro.remain_time,
            self.pomodoro.total_time,
        )

    def init_ui(self):
        self.setWindowTitle("PyPomodoro")
        self.setFixedSize(800, 600)
        self.setWindowIcon(
            QIcon(str(asset_path("logotyp.svg")))
        )

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(75, 45, 75, 40)
        main_layout.setSpacing(0)

        card = QFrame()
        card.setObjectName("timer_card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(45, 40, 45, 35)
        card_layout.setSpacing(20)

        self.description = QLabel("Время сосредоточиться")
        self.description.setObjectName("description-focus")
        self.description.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.timer_label = QLabel()
        self.timer_label.setObjectName("timer_label")
        self.timer_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.progress = QProgressBar()
        self.progress.setObjectName("progress")
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(5)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)

        self.start_btn = QPushButton("F1")
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setIcon(
            QIcon(str(asset_path("play.svg")))
        )
        self.start_btn.setIconSize(QSize(37, 37))
        self.start_btn.clicked.connect(self.start_timer)

        self.pause_btn = QPushButton("F2")
        self.pause_btn.setObjectName("secondary_btn")
        self.pause_btn.setIcon(
            QIcon(str(asset_path("pause.svg")))
        )
        self.pause_btn.setIconSize(QSize(37, 37))
        self.pause_btn.clicked.connect(self.pause_timer)

        self.reset_btn = QPushButton("F3")
        self.reset_btn.setObjectName("secondary_btn")
        self.reset_btn.setIcon(
            QIcon(str(asset_path("reset.svg")))
        )
        self.reset_btn.setIconSize(QSize(37, 37))
        self.reset_btn.clicked.connect(self.reset_timer)

        self.exit_btn = QPushButton("Ctrl+Q")
        self.exit_btn.setObjectName("exit_btn")
        self.exit_btn.setIcon(
            QIcon(str(asset_path("exit.svg")))
        )
        self.exit_btn.setIconSize(QSize(37, 37))
        self.exit_btn.clicked.connect(self.exit)

        buttons.addWidget(self.start_btn)
        buttons.addWidget(self.pause_btn)
        buttons.addWidget(self.reset_btn)
        buttons.addWidget(self.exit_btn)

        card_layout.addWidget(self.description)
        card_layout.addWidget(self.timer_label)
        card_layout.addWidget(self.progress)
        card_layout.addSpacing(12)
        card_layout.addLayout(buttons)

        main_layout.addWidget(card)
        main_layout.addStretch(1)


        stats_card = QFrame()
        stats_card.setObjectName("timer_card")
        stats_layout = QVBoxLayout(stats_card)
        stats_layout.setContentsMargins(20, 15, 20, 15)
        stats_layout.setSpacing(6)

        stats_title = QLabel("Статистика")
        stats_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_title.setObjectName("settings_label")

        self.stats_label = QLabel()
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stats_label.setObjectName("settings_label")

        stats_layout.addWidget(stats_title)
        stats_layout.addWidget(self.stats_label)
        main_layout.addWidget(stats_card)
        self.update_statistics_display()


        main_layout.addSpacing(18)

        settings = QHBoxLayout()

        settings_label = QLabel("Длительность сессии")
        settings_label.setObjectName("settings_label")

        self.edit_timer = QSpinBox()
        self.edit_timer.setRange(1, 180)
        self.edit_timer.setValue(self.pomodoro.work_time)
        self.edit_timer.setSuffix(" мин")
        self.edit_timer.setObjectName("time_input")
        self.edit_timer.valueChanged.connect(
            self.change_duration
        )

        settings.addWidget(settings_label)
        settings.addStretch()
        settings.addWidget(self.edit_timer)

        main_layout.addLayout(settings)

        self.setCentralWidget(central)
        self.create_shortcuts()

    def create_shortcuts(self):
        shortcuts = [
            ("F1", self.start_timer),
            ("F2", self.pause_timer),
            ("F3", self.reset_timer),
            ("Ctrl+Q", self.exit),
        ]

        self.shortcuts = []

        for key, callback in shortcuts:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.activated.connect(callback)
            self.shortcuts.append(shortcut)

    def change_duration(self, value):
        self.pomodoro.change_duration(value)
        self.settings["work_time"] = value
        save_settings(self.settings)


    def on_session_completed(self, completed_mode):
        self.play_completion_sound(completed_mode)
        if completed_mode == "focus":
            add_focus_session(self.statistics, self.pomodoro.work_time)
            self.update_statistics_display()

    def update_statistics_display(self):
        today = self.statistics.get("daily", {}).get(
            date.today().isoformat(), {}
        )
        today_sessions = today.get("sessions", 0)
        today_minutes = today.get("focus_minutes", 0)
        total_sessions = self.statistics.get("total_sessions", 0)
        total_minutes = self.statistics.get("total_focus_minutes", 0)
        self.stats_label.setText(
            f"Сегодня: {today_sessions} сессий · {today_minutes} мин\n"
            f"Всего: {total_sessions} сессий · {total_minutes} мин"
        )

    def start_timer(self):
        self.pomodoro.start_timer()

    def pause_timer(self):
        self.pomodoro.pause_timer()

    def reset_timer(self):
        self.pomodoro.reset_timer()

    def update_timer_display(self, remaining, total):
        self.timer_label.setText(
            self.pomodoro.format_time(remaining)
        )

        self.progress.setRange(0, max(1, total))
        self.progress.setValue(total - remaining)

        if hasattr(self, "tray"):
            self.tray.update(
                self.pomodoro.current_mode,
                remaining,
                total,
            )

    def update_mode_display(self, mode):
        descriptions = {
            "focus": (
                "Время сосредоточиться",
                "description-focus"
            ),

            "short_break": (
                "Короткий перерыв",
                "description-break"
            ),

            "long_break": (
                "Длинный перерыв",
                "description-break"
            ),
        }

        text, object_name = descriptions[mode]

        self.description.setText(text)
        self.description.setObjectName(object_name)

        self.description.style().unpolish(self.description)
        self.description.style().polish(self.description)

    def play_completion_sound(self, _completed_mode):
        sound_file = asset_path("alert.mp3")

        if sound_file.exists():
            Thread(
                target=playsound,
                args=(str(sound_file),),
                daemon=True,
            ).start()

    def show_window(self):
        self.show()
        self.activateWindow()
        self.raise_()

    def exit(self):
        QApplication.instance().quit()

    def closeEvent(self, event):
        self.hide()
        event.ignore()