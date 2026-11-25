import sys

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from storage.storage_manager import load_settings


if __name__ == "__main__":
    settings = load_settings() #подгрузка ранее сохр. настроек

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    window = MainWindow(settings)
    window.show()

    sys.exit(app.exec())