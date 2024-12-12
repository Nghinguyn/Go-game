from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import json
import os


class SettingsDialog(QDialog):
    # Create a custom signal for settings changes
    settings_changed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Game Settings")
        self.setFixedSize(600, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
       # Set default settings
        self.default_settings = {
            'board_size': 9,
            'timer': 5,
            'window_mode': "FullScreen",
            'sound_enabled': True
        }
        
        # Load saved settings or use defaults
        self.current_settings = self.load_settings()
        
        self.initUI()
        self.apply_loaded_settings()
        
        
        
    def load_settings(self):
        """Load settings from file or return defaults if file doesn't exist"""
        settings_file = os.path.join(os.path.dirname(__file__), 'game_settings.json')
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return self.default_settings.copy()
            
    def save_settings(self, settings):
        """Save settings to file"""
        settings_file = os.path.join(os.path.dirname(__file__), 'game_settings.json')
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
            
    def apply_loaded_settings(self):
        """Apply loaded settings to UI elements"""
        # Set board size
        if self.current_settings['board_size'] == 7:
            self.board_7x7.setChecked(True)
        else:
            self.board_9x9.setChecked(True)
            
        # Set timer
        self.timer_slider.setValue(self.current_settings['timer'])
        self.timer_label.setText(f"{self.current_settings['timer']} minutes")
        
        # Set window mode
        index = self.window_modes.findText(self.current_settings['window_mode'])
        if index >= 0:
            self.window_modes.setCurrentIndex(index)
            
        # Set sound
        self.sound_toggle.setChecked(self.current_settings['sound_enabled'])
        self._update_sound_button()



    

    def apply_settings(self):
        """Apply settings, save them, and show success message"""
        # Get and emit settings
        settings = self.get_settings()
        self.settings_changed.emit(settings)
        self.save_settings(settings)  # Save settings when applied
        
        # Create and show success message
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Settings applied successfully!")
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Remove window decorations only
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        
        # Style the message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                border-radius: 15px;
                min-width: 300px;
                padding: 20px;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QLabel#qt_msgbox_label {
                color: white;
                font-size: 16px;
            }
            QLabel#qt_msgboxex_icon_label {
                padding: 10px;
            }
        """)
        
        msg.exec()






    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        
        # Create main container with styling
        container = QFrame(self)
        container.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setSpacing(25)
        
        # Title
        title = QLabel("Game Settings")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                padding: 20px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Board Size Section
        board_group = QGroupBox("Game Board Size")
        board_group.setStyleSheet(self._get_group_style())
        board_layout = QHBoxLayout()
        
        self.board_7x7 = QRadioButton("7 x 7")
        self.board_9x9 = QRadioButton("9 x 9")
        self.board_9x9.setChecked(True)
        
        for radio in [self.board_7x7, self.board_9x9]:
            radio.setStyleSheet(self._get_radio_style())
            board_layout.addWidget(radio)
            
        board_group.setLayout(board_layout)
        
        # Timer Section
        timer_group = QGroupBox("Game Timer")
        timer_group.setStyleSheet(self._get_group_style())
        timer_layout = QVBoxLayout()
        
        self.timer_slider = QSlider(Qt.Orientation.Horizontal)
        self.timer_slider.setMinimum(5)
        self.timer_slider.setMaximum(60)
        self.timer_slider.setValue(5)
        self.timer_slider.setStyleSheet(self._get_slider_style())
        
        self.timer_label = QLabel("5 minutes")
        self.timer_label.setStyleSheet("color: white;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.timer_slider.valueChanged.connect(self._update_timer_label)
        
        timer_layout.addWidget(self.timer_slider)
        timer_layout.addWidget(self.timer_label)
        timer_group.setLayout(timer_layout)
        
        # Window Mode Section
        window_group = QGroupBox("Window Mode")
        window_group.setStyleSheet(self._get_group_style())
        window_layout = QVBoxLayout()
        
        self.window_modes = QComboBox()
        self.window_modes.addItems(["FullScreen", "Window Fullscreen", "Normal Window"])
        self.window_modes.setStyleSheet(self._get_combobox_style())
        
        window_layout.addWidget(self.window_modes)
        window_group.setLayout(window_layout)
        
        # Sound Toggle Section
        sound_group = QGroupBox("Sound")
        sound_group.setStyleSheet(self._get_group_style())
        sound_layout = QHBoxLayout()
        
        self.sound_toggle = QPushButton()
        self.sound_toggle.setCheckable(True)
        self.sound_toggle.setChecked(True)
        self.sound_toggle.clicked.connect(self._update_sound_button)
        self.sound_toggle.setStyleSheet(self._get_toggle_style())
        self._update_sound_button()
        
        sound_layout.addWidget(self.sound_toggle)
        sound_group.setLayout(sound_layout)
        




        # Create button container at the bottom
        button_container = QHBoxLayout()
        button_container.setSpacing(20)
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Style string for both buttons
        button_style = """
            QPushButton {
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
                min-width: 120px;
            }
        """

        # Apply Button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #2ecc71;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.apply_button.clicked.connect(self.apply_settings)

        # Back Button
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet(button_style + """
            QPushButton {
                background-color: #3498db;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.back_button.clicked.connect(self.close)

        
        # Add buttons to container
        button_container.addWidget(self.apply_button)
        button_container.addWidget(self.back_button)
        

        # Add all widgets to main layout (only once!)
        layout.addWidget(title)
        layout.addWidget(board_group)
        layout.addWidget(timer_group)
        layout.addWidget(window_group)
        layout.addWidget(sound_group)
        layout.addLayout(button_container)
        
        main_layout.addWidget(container)

    def save_and_close(self):
        settings = self.get_settings()
        self.settings_changed.emit(settings)
        self.accept()  # Use accept() instead of close()

        
    def _get_group_style(self):
        return """
            QGroupBox {
                color: white;
                font-size: 20px;        
                font-weight: bold;
                border: 2px solid #34495e;
                border-radius: 15px;     
                margin-top: 20px;        
                padding: 20px;           
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 15px;         
            }
        """
        
    def _get_radio_style(self):
        return """
            QRadioButton {
                color: white;
                font-size: 18px;
                spacing: 15px;
            }
            QRadioButton::indicator {
                width: 25px;
                height: 25px;
                border-radius: 12px;
                border: 2px solid #3498db;
            }
            QRadioButton::indicator:checked {
                background-color: #3498db;
            }
        """
        
    def _get_slider_style(self):
        return """
            QSlider::groove:horizontal {
                border: 1px solid #3498db;
                height: 30px;
                background: #34495e;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                border: 1px solid #2980b9;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
        """
        
    def _get_combobox_style(self):
        return """
            QComboBox {
                color: white;
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QComboBox QAbstractItemView {
                color: white;
                background-color: #34495e;
                selection-background-color: #3498db;
            }
        """
        
    def _get_toggle_style(self):
        return """
            QPushButton {
                min-width: 80px;
                min-height: 30px;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #2ecc71;
            }
            QPushButton:!checked {
                background-color: #e74c3c;
            }
        """
        
    def _update_timer_label(self):
        value = self.timer_slider.value()
        self.timer_label.setText(f"{value} minutes")
        
    def _update_sound_button(self):
        self.sound_toggle.setText("ON" if self.sound_toggle.isChecked() else "OFF")
        
    def get_settings(self):
        return {
            'board_size': 7 if self.board_7x7.isChecked() else 9,
            'timer': self.timer_slider.value(),
            'window_mode': self.window_modes.currentText(),
            'sound_enabled': self.sound_toggle.isChecked()
        }
    


    def apply_settings(self):
        """Apply settings and show success message"""
        # Get and emit settings
        settings = self.get_settings()
        self.settings_changed.emit(settings)
        
        # Create and show success message
        msg = QMessageBox(self)
        msg.setWindowTitle("Success")
        msg.setText("Settings applied successfully!")
        msg.setIcon(QMessageBox.Icon.Information)
        
        # Remove window decorations and make background translucent
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        
        # Style the message box
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2c3e50;
                border-radius: 15px;
            }
            QMessageBox QLabel {
                color: white;
                font-size: 16px;
                padding: 10px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Show the message box
        msg.exec()


        
    def close_dialog(self):
        """Close the dialog without applying settings"""
        self.accept()
        
    def save_and_close(self):
        """Apply settings and close dialog (can be used for other buttons if needed)"""
        self.apply_settings()
        self.close_dialog()
