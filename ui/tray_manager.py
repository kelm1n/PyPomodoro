from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (
    QSystemTrayIcon, QMenu, QWidget,
    QWidgetAction, QVBoxLayout, QLabel,
    QProgressBar,
)

from utils.paths import asset_path
from ui.style import APP_STYLE


class TrayManager:
    def __init__(self, parent, on_open, on_exit):
        self.parent = parent

        self.tray_icon = QSystemTrayIcon(parent)
        self.tray_icon.setIcon(
            QIcon(str(asset_path("logotyp.svg")))
        )
        self.tray_icon.setToolTip("PyPomodoro")

        self.menu = QMenu(parent)
        self.menu.setStyleSheet(APP_STYLE)

        self.create_progress_widget()

        self.show_action = QAction("Открыть", parent)
        self.exit_action = QAction("Выход", parent)


        self.show_action.triggered.connect(on_open)
        self.exit_action.triggered.connect(on_exit)

        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        self.menu.addAction(self.exit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.on_tray_activated)

        self.tray_icon.show()

        

    def create_progress_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(5)

        self.mode_label = QLabel("Фокус")
        self.mode_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)

        self.time_label = QLabel("25:00")
        self.time_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(self.mode_label)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.time_label)

        widget.setObjectName("tray_widget")
        self.mode_label.setObjectName("tray_title")
        self.time_label.setObjectName("tray_details")
        self.progress_bar.setObjectName("tray_progress")

        self.progress_action = QWidgetAction(self.parent)
        self.progress_action.setDefaultWidget(widget)

        self.menu.addAction(self.progress_action)

    def update(self, mode, remaining, total):
        descriptions = {
            "focus": "Фокус",
            "short_break": "Короткий перерыв",
            "long_break": "Длинный перерыв",
        }

        self.mode_label.setText(descriptions[mode])

        self.progress_bar.setRange(0, max(1, total))
        self.progress_bar.setValue(total - remaining)

        minutes, seconds = divmod(remaining, 60)
        self.time_label.setText(
            f"{minutes:02}:{seconds:02}"
        )

        progress = int(
            (total - remaining) / max(1, total) * 100
        )

        self.tray_icon.setToolTip(
            f"PyPomodoro | {descriptions[mode]} | "
            f"{minutes:02}:{seconds:02} | {progress}%"
        )

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.parent.show_window()