APP_STYLE = """
QMainWindow {
    background-color: #15171C;
}

QWidget {
    color: #ECEDEF;
    font-family: "Segoe UI";
    font-size: 14px;
}

/* Логотип */
QLabel#logo {
    font-size: 19px;
    font-weight: 700;
    color: #F1F1F2;
}

/* Центральная карточка */
QFrame#timer_card {
    background-color: #1E2128;
    border: 1px solid #2B2F38;
    border-radius: 22px;
}

/* Описание режима */
QLabel#description-focus {
    background-color: #2bbf51;
    color: #153c1f;
    font-size: 14px;
    border-radius: 9px;
    padding: 7px 14px;
    font-weight: bold;
}

QLabel#description-break {
    background-color: #D94B4B;
    color: #FFFFFF;
    font-size: 14px;
    border-radius: 9px;
    padding: 7px 14px;
    font-weight: bold;
}

/* Таймер */
QLabel#timer_label {
    color: #F5F5F5;
    font-size: 88px;
    font-weight: 600;
    background: transparent;
}

/* Прогресс */
QProgressBar#progress {
    background-color: #30343E;
    border: none;
    border-radius: 2px;
}

QProgressBar#progress::chunk {
    background-color: #E7795B;
    border-radius: 2px;
}

/* Кнопки */
QPushButton {
    min-height: 46px;
    border: 1px solid transparent;
    border-radius: 10px;
    padding: 0 20px;
    font-size: 14px;
    font-weight: 600;
}

/* Старт */
QPushButton#start_btn {
    background-color: #E7795B;
    color: white;
}

QPushButton#start_btn:hover {
    background-color: #363B46;
    border: 1px solid #F6A18A;
}

QPushButton#start_btn:pressed {
    background-color: #20232B;
    border: 1px solid #B9563D;
}

/* Пауза и сброс */
QPushButton#secondary_btn {
    background-color: #E7795B;
    color: #D8DADE;
    border: 1px solid #3A3F4B;
}

QPushButton#secondary_btn:hover {
    background-color: #363B46;
    border: 1px solid #555C6B;
}

QPushButton#secondary_btn:pressed {
    background-color: #20232B;
    border: 1px solid #E7795B;
}

/* Выход */
QPushButton#exit_btn {
    background-color: #E7795B;
    color: #D8DADE;
    border: 1px solid #3A3F4B;
}

QPushButton#exit_btn:hover {
    background-color: #492D32;
    border: 1px solid #B95C66;
    color: #FFB8BE;
}

QPushButton#exit_btn:pressed {
    background-color: #352126;
    border: 1px solid #D94B4B;
}

/* Настройки */
QLabel#settings_label {
    color: #9297A3;
    font-size: 13px;
}

QSpinBox#time_input {
    background-color: #20232B;
    color: #ECEDEF;
    border: 1px solid #343944;
    border-radius: 9px;
    padding: 8px 12px;
    min-width: 100px;
    min-height: 25px;
}

QSpinBox#time_input:focus {
    border: 1px solid #E7795B;
}

QSpinBox#time_input::up-button {
    subcontrol-origin: border;
    width: 22px;
    background-color: #292D36;
    border-left: 1px solid #343944;
}

QSpinBox#time_input::down-button {
    subcontrol-origin: border;
    width: 22px;
    background-color: #292D36;
    border-left: 1px solid #343944;
}

QSpinBox#time_input::up-button {
    subcontrol-position: top right;
    border-top-right-radius: 8px;
}

QSpinBox#time_input::down-button {
    subcontrol-position: bottom right;
    border-bottom-right-radius: 8px;
}

QSpinBox#time_input::up-arrow {
    image: url(assets/arrowup.svg);
    width: 15px;
    height: 15px;
}

QSpinBox#time_input::down-arrow {
    image: url(assets/arrowdown.svg);
    width: 15px;
    height: 15px;
}

/* Индикатор в меню трея */
QLabel#tray_title {
    color: #ECEDEF;
    font-weight: 600;
}

QLabel#tray_details {
    color: #A8ADB8;
    font-size: 12px;
}

QProgressBar#tray_progress {
    min-height: 7px;
    max-height: 7px;
    border: none;
    border-radius: 3px;
    background-color: #30343E;
}

QProgressBar#tray_progress::chunk {
    background-color: #E7795B;
    border-radius: 3px;
}

/* Системный трей */
QMenu {
    background-color: #1E2128;
    color: #ECEDEF;
    border: 1px solid #343944;
    padding: 5px;
}

QMenu::item {
    background-color: transparent;
    color: #ECEDEF;
    padding: 8px 24px;
    border-radius: 5px;
}

QMenu::item:selected {
    background-color: #30343E;
    color: #FFFFFF;
}

QMenu::separator {
    height: 1px;
    background-color: #343944;
    margin: 5px 8px;
}

/* Виджеты внутри трея */
QWidget#tray_widget {
    background-color: #1E2128;
    color: #ECEDEF;
}

QLabel#tray_title,
QLabel#tray_details {
    background-color: transparent;
    color: #ECEDEF;
}

QProgressBar#tray_progress {
    background-color: #30343E;
    border: none;
    border-radius: 3px;
}

QProgressBar#tray_progress::chunk {
    background-color: #E7795B;
    border-radius: 3px;
}

"""
