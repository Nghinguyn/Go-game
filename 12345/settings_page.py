from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QComboBox, QSpinBox, QCheckBox, QGroupBox, QButtonGroup, QRadioButton,
                            QFrame, QSlider)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QIcon

class SettingsPage(QWidget):

    board_size_changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.board_size_combo.currentTextChanged.connect(self.on_board_size_changed)
        

    def on_board_size_changed(self, size_text):
        """Handle board size changes"""
        try:
            size = int(size_text.split('×')[0])
            self.board_size_changed.emit(size)  # Emit the signal with new size
        except ValueError as e:
            print(f"Error converting board size: {e}")
    
    def set_board_size_callback(self, callback):
        """Set callback for board size changes"""
        self.board_size_changed_callback = callback
        
    def set_current_board_size(self, size):
        """Update the combo box to reflect current board size"""
        self.board_size_combo.setCurrentText(f'{size}×{size}')

    def init_ui(self):
        # Set background color and style for the entire page
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                color: #ECF0F1;
            }
            QGroupBox {
                background-color: #34495E;
                border-radius: 15px;
                margin-top: 15px;
                padding: 20px;
                font-size: 16px;
                font-weight: bold;
                border: none;
            }
            QGroupBox::title {
                color: #3498DB;
                padding: 0px 15px;
            }
            QLabel {
                font-size: 14px;
                color: #ECF0F1;
            }
            QComboBox, QSpinBox {
                background-color: #ECF0F1;
                border: none;
                border-radius: 5px;
                padding: 8px;
                min-width: 150px;
                color: #2C3E50;
                font-size: 14px;
            }
            QComboBox:hover, QSpinBox:hover {
                background-color: #BDC3C7;
            }
            QCheckBox {
                font-size: 14px;
                spacing: 10px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                background-color: #ECF0F1;
            }
            QCheckBox::indicator:checked {
                background-color: #3498DB;
                image: url(check.png);
            }
            QPushButton {
                background-color: #3498DB;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 25px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            QPushButton#backButton {
                background-color: #E74C3C;
            }
            QPushButton#backButton:hover {
                background-color: #C0392B;
            }
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #ECF0F1;
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498DB;
                border: none;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #2980B9;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet("""
            font-size: 32px;
            color: #3498DB;
            font-weight: bold;
            margin-bottom: 20px;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Game Settings Group
        game_group = self.create_game_settings_group()
        main_layout.addWidget(game_group)

        # Display Settings Group
        display_group = self.create_display_settings_group()
        main_layout.addWidget(display_group)

        # Sound Settings Group
        sound_group = self.create_sound_settings_group()
        main_layout.addWidget(sound_group)

        # Buttons Container
        buttons_container = QFrame()
        buttons_layout = QHBoxLayout()
        buttons_container.setLayout(buttons_layout)

        self.back_btn = QPushButton("← Back")
        self.back_btn.setObjectName("backButton")
        self.apply_btn = QPushButton("✓ Apply Settings")
        
        buttons_layout.addWidget(self.back_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.apply_btn)

        main_layout.addWidget(buttons_container)
        self.setLayout(main_layout)

    def create_game_settings_group(self):
        group = QGroupBox("Game Settings")
        layout = QVBoxLayout()

        # Board Size Setting
        board_container = QHBoxLayout()
        size_label = QLabel("Board Size:")
        self.board_size_combo = QComboBox()
        # Update these lines to change board size options
        self.board_size_combo.addItems(['7×7', '9×9'])  # Changed from ['9×9', '13×13', '19×19']
        self.board_size_combo.setCurrentText('9×9')     # Changed default from '19×19' to '9×9'
        board_container.addWidget(size_label)
        board_container.addWidget(self.board_size_combo)
        board_container.addStretch()

        # Timer Setting
        timer_container = QHBoxLayout()
        timer_label = QLabel("Game Time (minutes):")
        self.timer_spin = QSpinBox()
        self.timer_spin.setRange(1, 180)
        self.timer_spin.setValue(30)
        self.timer_spin.setSingleStep(5)
        timer_container.addWidget(timer_label)
        timer_container.addWidget(self.timer_spin)
        timer_container.addStretch()

        layout.addLayout(board_container)
        layout.addLayout(timer_container)
        group.setLayout(layout)
        return group
        
    def create_timer_settings(self, main_layout):
        group = QGroupBox("Timer Settings")
        layout = QHBoxLayout()
        timer_label = QLabel("Game Time (minutes):")
        self.timer_spin = QSpinBox()
        self.timer_spin.setRange(10, 300)
        self.timer_spin.setValue(30)
        self.timer_spin.setSingleStep(5)

        layout.addWidget(timer_label)
        layout.addWidget(self.timer_spin)
        layout.addStretch()
        
        group.setLayout(layout)
        main_layout.addWidget(group)
        
    def create_display_settings_group(self):
        group = QGroupBox("Display Settings")
        layout = QVBoxLayout()

        # Create a button group for window modes
        self.window_mode_group = QButtonGroup(self)
        
        # Create radio buttons instead of checkboxes
        self.fullscreen_radio = QRadioButton("Fullscreen Mode")
        self.window_fullscreen_radio = QRadioButton("Windowed Fullscreen")
        self.normal_window_radio = QRadioButton("Windowed Mode")
        
        # Add radio buttons to the button group
        self.window_mode_group.addButton(self.fullscreen_radio)
        self.window_mode_group.addButton(self.window_fullscreen_radio)
        self.window_mode_group.addButton(self.normal_window_radio)
        
        # Set default selection
        self.fullscreen_radio.setChecked(True)

        # Theme Selection
        theme_container = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(['Classic', 'Modern', 'Dark', 'Light'])
        theme_container.addWidget(theme_label)
        theme_container.addWidget(self.theme_combo)
        theme_container.addStretch()

        # Add widgets to layout
        layout.addWidget(self.fullscreen_radio)
        layout.addWidget(self.window_fullscreen_radio)
        layout.addWidget(self.normal_window_radio)
        layout.addLayout(theme_container)
        
        group.setLayout(layout)
        return group
        
    def create_sound_settings_group(self):
        group = QGroupBox("Sound Settings")
        layout = QVBoxLayout()

        # Sound Enable/Disable
        self.sound_enabled = QCheckBox("Enable Sound Effects")
        self.sound_enabled.setChecked(True)

        # Volume Slider
        volume_container = QHBoxLayout()
        volume_label = QLabel("Volume:")
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(70)
        volume_container.addWidget(volume_label)
        volume_container.addWidget(self.volume_slider)

        layout.addWidget(self.sound_enabled)
        layout.addLayout(volume_container)
        group.setLayout(layout)
        return group
    
    def create_navigation_buttons(self, main_layout):
        button_layout = QHBoxLayout()

        self.back_btn = QPushButton("Back to Menu")
        self.apply_btn = QPushButton("Apply Settings")

        for btn in [self.back_btn, self.apply_btn]:
            btn.setFixedSize(200, 50)
            btn.setFont(QFont('Arial', 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #2C3E50;
                    color: #ECF0F1;
                    border: none;
                    border-radius: 15px;
                    padding: 15px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #34495E;
                }
                QPushButton:pressed {
                    background-color: #2980B9;
                }
            """)
            button_layout.addWidget(btn)

        main_layout.addLayout(button_layout)

    def get_settings(self):
        board_size = int(self.board_size_combo.currentText().split('×')[0])
        return {
            'board_size': board_size,
            'timer_minutes': self.timer_spin.value(),
            'fullscreen': self.fullscreen_radio.isChecked(),
            'window_fullscreen': self.window_fullscreen_radio.isChecked(),
            'normal_window': self.normal_window_radio.isChecked(),
            'sound_enabled': self.sound_enabled.isChecked(),
            'volume': self.volume_slider.value(),
            'theme': self.theme_combo.currentText()
        }
    
    def apply_settings(self):
        try:
            new_settings = self.settings_page.get_settings()
            print(f"Applying new settings: {new_settings}")  # Debug print
            
            # Apply window mode
            if new_settings['fullscreen']:
                self.showFullScreen()
            elif new_settings['window_fullscreen']:
                self.showMaximized()
            else:
                self.showNormal()
                self.setGeometry(100, 100, 1024, 768)

            # Apply board size if changed
            if new_settings['board_size'] != self.settings['board_size']:
                print(f"Board size changing from {self.settings['board_size']} to {new_settings['board_size']}")
                self.on_board_size_changed(new_settings['board_size'])
            
            # Store new settings
            self.settings = new_settings
            self.show_main_menu()
        except Exception as e:
            print(f"Error applying settings: {e}")
            import traceback
            traceback.print_exc()
