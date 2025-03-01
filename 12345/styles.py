# Create a new file for centralized styling
COLORS = {
    'primary': '#34495e',      # Dark blue-gray
    'secondary': '#2c3e50',    # Darker blue-gray
    'accent': '#3498db',       # Bright blue
    'accent_hover': '#2980b9', # Darker blue
    'success': '#2ecc71',      # Green
    'warning': '#f1c40f',      # Yellow
    'error': '#e74c3c',        # Red
    'text_light': '#ecf0f1',   # Light gray
    'text_dark': '#2c3e50',    # Dark blue-gray
    'board_brown': '#c4a484',  # Wood color
    'board_lines': '#4a4a4a',  # Dark gray for board lines
    'gradient_start': '#d5d4d0',
    'gradient_end': '#d5d4d0',
}

MAIN_MENU_STYLE = """
    QWidget {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #d5d4d0, stop:1 #d5d4d0);
    }
    QLabel#title {
        color: #2c3e50;
        font-size: 72px;
        font-weight: bold;
        font-family: 'Segoe UI';
        margin-bottom: 30px;
    }
"""

MENU_BUTTON_STYLE = """
    QPushButton {
        background-color: #34495e;
        color: #ecf0f1;
        border: none;
        border-radius: 20px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: bold;
        font-family: 'Segoe UI';
        min-width: 300px;
        margin: 10px;
    }
    QPushButton:hover {
        background-color: #3498db;
    }
    QPushButton:pressed {
        background-color: #2980b9;
    }
"""

BOARD_CONTAINER_STYLE = """
    QFrame#leftPanel {
        background-color: rgba(52, 73, 94, 0.95);
        border-radius: 20px;
        margin: 10px;
        padding: 20px;
    }
    QFrame#rightPanel {
        background-color: #c4a484;
        border-radius: 20px;
        margin: 10px;
        padding: 20px;
    }
    QLabel {
        color: #ecf0f1;
        font-size: 16px;
        font-weight: bold;
        font-family: 'Segoe UI';
    }
    QPushButton {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 12px;
        font-size: 14px;
        font-weight: bold;
        font-family: 'Segoe UI';
        min-height: 45px;
    }
    QPushButton:hover {
        background-color: #2980b9;
    }
    QListWidget {
        background-color: rgba(236, 240, 241, 0.1);
        border-radius: 15px;
        color: white;
        padding: 10px;
        font-size: 14px;
        font-family: 'Segoe UI';
    }
"""

SETTINGS_STYLE = """
    QWidget {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #d5d4d0, stop:1 #d5d4d0);
    }
    QGroupBox {
        background-color: rgba(52, 73, 94, 0.95);
        border-radius: 15px;
        margin-top: 20px;
        padding: 20px;
        font-size: 16px;
        font-weight: bold;
        font-family: 'Segoe UI';
        color: #ecf0f1;
    }
    QLabel {
        color: #ecf0f1;
        font-size: 14px;
        font-family: 'Segoe UI';
    }
    QComboBox, QSpinBox {
        background-color: #ecf0f1;
        border: none;
        border-radius: 10px;
        padding: 8px;
        min-width: 150px;
        color: #2c3e50;
        font-size: 14px;
        font-family: 'Segoe UI';
    }
    QCheckBox {
        color: #ecf0f1;
        font-size: 14px;
        font-family: 'Segoe UI';
        spacing: 10px;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
        border-radius: 5px;
        background-color: #ecf0f1;
    }
    QCheckBox::indicator:checked {
        background-color: #3498db;
    }
"""