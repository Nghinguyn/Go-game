from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *




class UserPageDialog(QDialog):
    game_started = pyqtSignal(dict)  # Signal to emit player settings
    
    def __init__(self, parent, GoGameClass):
        super().__init__(parent)
        self.setWindowTitle("Player Setup")
        self.setFixedSize(600, 800)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.player_mode = None
        self.p1_name = None  # Will be set when mode is selected
        self.initUI()

        self.start_game_button = QPushButton("Start Game")
        self.start_game_button.setEnabled(False)  # Initially disabled
        
        self.GoGameClass = GoGameClass

        

    def initUI(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(30)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create main container with styling
        container = QFrame(self)
        container.setStyleSheet(self._get_container_style())
        
        layout = QVBoxLayout(container)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)  # Increased padding
        
        # Title
        title = QLabel("Player Setup")
        title.setStyleSheet(self._get_title_style())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Setup stack widget
        self.setup_stack = QStackedWidget()
        
        # Create and add pages
        self.mode_select_page = self._create_mode_select_page()
        self.one_player_page = self._create_player_page(single_player=True)
        self.two_player_page = self._create_player_page(single_player=False)
        
        self.setup_stack.addWidget(self.mode_select_page)
        self.setup_stack.addWidget(self.one_player_page)
        self.setup_stack.addWidget(self.two_player_page)

        if hasattr(self, 'player1') and self.player1:
            p1_name = self.player1.get('name', 'Player 1')
        else:
            p1_name = 'Player 1'
        p1_group = QGroupBox(f"Player 1: {p1_name}")
        
        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(self.setup_stack)
        
        main_layout.addWidget(container)


        

    def _create_player_page(self, single_player=True):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(30)
        layout.setContentsMargins(20, 20, 20, 20)

        # Player Forms Container
        forms_container = QWidget()
        forms_layout = QVBoxLayout(forms_container)
        forms_layout.setSpacing(20)

        # Player Forms
        for i in range(1 if single_player else 2):
            group = QGroupBox(f"Player {i+1}")
            group.setStyleSheet(self._get_group_style())
            group_layout = QFormLayout()  # Changed to QFormLayout for better alignment
            group_layout.setSpacing(15)
            group_layout.setContentsMargins(20, 30, 20, 20)

            # Name Input
            name_label = QLabel("Name:")
            name_input = QLineEdit()
            name_input.setPlaceholderText("Enter name")
            name_input.setStyleSheet(self._get_line_edit_style())

            # Connect to the appropriate validation logic
            if single_player and i == 0:
                name_input.textChanged.connect(self._validate_single_player_inputs)
            else:
                name_input.textChanged.connect(self._validate_two_player_inputs)

            # Store references
            if i == 0:
                self.p1_name = name_input
            else:
                self.p2_name = name_input

            # Stone Color Selection
            color_label = QLabel("Stone Color:")
            color_combo = QComboBox()
            color_combo.addItems(["Black", "White"])
            color_combo.setStyleSheet(self._get_combobox_style())

            # Store references
            if i == 0:
                self.p1_color = color_combo
            else:
                self.p2_color = color_combo

            # Add to form layout
            group_layout.addRow(name_label, name_input)
            group_layout.addRow(color_label, color_combo)

            group.setLayout(group_layout)
            forms_layout.addWidget(group)

        layout.addWidget(forms_container)

        # Buttons Container
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)

        # Start Game Button
        start_btn = QPushButton("Start Game")
        start_btn.setFixedWidth(150)
        start_btn.setStyleSheet(self._get_action_button_style())
        start_btn.clicked.connect(self._start_game)  # Connect to start game logic
        self.start_game_button = start_btn  # Store reference for dynamic enabling/disabling

        # Back Button
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(150)
        back_btn.setStyleSheet(self._get_button_style())
        back_btn.clicked.connect(self._back_to_mode_select)

        button_layout.addStretch()
        button_layout.addWidget(start_btn)
        button_layout.addWidget(back_btn)
        button_layout.addStretch()

        layout.addStretch()
        layout.addWidget(button_container)

        return page





    


    def _show_player_setup(self, single_player):
        """Switch to the appropriate player setup page."""
        self.player_mode = "single" if single_player else "two_player"
        self._clear_inputs()  # Clear inputs before switching modes

        # Safely disconnect signals to avoid interference
        if hasattr(self, 'p1_name') and self.p1_name:
            try:
                self.p1_name.textChanged.disconnect()
            except TypeError:
                pass  # Ignore if no connection exists

        if not single_player and hasattr(self, 'p2_name') and self.p2_name:
            try:
                self.p2_name.textChanged.disconnect()
            except TypeError:
                pass  # Ignore if no connection exists

        # Connect the correct validation logic
        if single_player:
            self.p1_name.textChanged.connect(self._validate_single_player_inputs)
        else:
            self.p1_name.textChanged.connect(self._validate_two_player_inputs)
            if hasattr(self, 'p2_name') and self.p2_name:
                self.p2_name.textChanged.connect(self._validate_two_player_inputs)

        print(f"Switching to {self.player_mode} mode")

        # Set the current widget based on the mode
        if single_player:
            self.setup_stack.setCurrentWidget(self.one_player_page)
        else:
            self.setup_stack.setCurrentWidget(self.two_player_page)




    def _clear_inputs(self):
        """Clear all input fields."""
        if hasattr(self, 'p1_name') and self.p1_name:
            self.p1_name.clear()
            self.show_error_message(self.p1_name, False)  # Hide error message
        if hasattr(self, 'p2_name') and self.p2_name:
            self.p2_name.clear()
            self.show_error_message(self.p2_name, False)  # Hide error message

        # Reset dropdown selections
        if hasattr(self, 'p1_color') and self.p1_color:
            self.p1_color.setCurrentIndex(0)
        if hasattr(self, 'p2_color') and self.p2_color:
            self.p2_color.setCurrentIndex(0)





    def _back_to_mode_select(self):
        """Handle back button click."""
        self._clear_inputs()  # Clear inputs when returning to mode select
        self.setup_stack.setCurrentWidget(self.mode_select_page)




    def _start_game(self):
        """Handle game start."""
        if not self._validate_inputs():  # Validate inputs before starting the game
            return

        try:
            # Create game settings
            game_settings = {
                'mode': self.player_mode,
                'player1': {
                    'name': self.p1_name.text().strip(),
                    'color': self.p1_color.currentText()
                }
            }

            if self.player_mode == "single":
                game_settings['player2'] = {
                    'name': 'Computer',
                    'color': 'White' if self.p1_color.currentText() == 'Black' else 'Black'
                }
            else:  # Two-player mode
                game_settings['player2'] = {
                    'name': self.p2_name.text().strip(),
                    'color': self.p2_color.currentText()
                }

            print(f"Game settings: {game_settings}")
            
            # Use the existing GoGameClass instance passed to the dialog
            if self.GoGameClass:
                self.GoGameClass.setup_game(game_settings)  # Setup the game with settings
                self.game_started.emit(game_settings)  # Emit settings to parent
                self.accept()  # Close the dialog
            else:
                raise ValueError("GoGameClass not properly initialized")

        except Exception as e:
            print(f"Error starting game: {e}")
            self._show_error("Error starting game. Please try again.")




    def _validate_inputs(self):
        """Validate inputs based on the selected mode."""
        if self.player_mode == "single":
            return self._validate_single_player_inputs()
        elif self.player_mode == "two_player":
            return self._validate_two_player_inputs()
        return False


    def _validate_single_player_inputs(self):
        """Validate inputs for single-player mode."""
        if not hasattr(self, 'p1_name'):
            return False

        player1_valid = bool(self.p1_name.text().strip())  # Check if Player 1's name is valid
        self.show_error_message(self.p1_name, not player1_valid)  # Show error if invalid
        self.start_game_button.setEnabled(player1_valid)  # Enable button if valid
        return player1_valid




    def _validate_two_player_inputs(self):
        """Validate inputs for two-player mode."""
        if not hasattr(self, 'p1_name') or not hasattr(self, 'p2_name'):
            return False

        player1_valid = bool(self.p1_name.text().strip())
        player2_valid = bool(self.p2_name.text().strip())

        self.show_error_message(self.p1_name, not player1_valid)
        self.show_error_message(self.p2_name, not player2_valid)

        # Enable button only if both players' inputs are valid
        self.start_game_button.setEnabled(player1_valid and player2_valid)
        return player1_valid and player2_valid






    def _show_error(self, message):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        msg.setStyleSheet(self._get_message_box_style())
        msg.exec()

    def show_error_message(self, input_field, show):
        """Show or hide error message for an input field."""
        if not hasattr(input_field, 'error_label'):
            # Create error label if it doesn't exist
            error_label = QLabel("Please enter a valid name!")
            error_label.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 12px;
                    margin-top: 5px;
                }
            """)
            error_label.setVisible(False)
            input_field.error_label = error_label

            # Add error label to the parent layout
            parent_layout = input_field.parent().layout()
            if parent_layout:
                parent_layout.addWidget(error_label)

        input_field.error_label.setVisible(show)


    # Styles

    def _get_container_style(self):
        return """
            QFrame {
                background-color: rgba(44, 62, 80, 0.95);
                border-radius: 20px;
                border: 2px solid rgba(52, 152, 219, 0.5);
            }
        """

    def _get_title_style(self):
        return """
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """

    def _get_group_style(self):
        return """
            QGroupBox {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background-color: rgba(52, 73, 94, 0.8);
                border: 2px solid #3498db;
                border-radius: 15px;
                margin-top: 25px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 20px;
                background-color: #2c3e50;
            }
        """

    def _get_button_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2472a4;
            }
            QPushButton#mode_button {
                background-color: #3498db;
                margin: 5px 10px;
            }
            QPushButton#action_button {
                background-color: #2ecc71;
            }
            QPushButton#action_button:hover {
                background-color: #27ae60;
            }
            QPushButton#back_button {
                background-color: #e74c3c;
            }
            QPushButton#back_button:hover {
                background-color: #c0392b;
            }
        """

    def _get_mode_button_style(self):
        return """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """

    def _get_line_edit_style(self):
        return """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 16px;
                color: #2c3e50;
                min-height: 25px;
                min-width: 200px;
            }
            QLineEdit:focus {
                border-color: #2ecc71;
                background-color: white;
            }
        """


    def _get_combobox_style(self):
        return """
            QComboBox {
                background-color: rgba(255, 255, 255, 0.9); /* Light background for the combo box */
                border: 2px solid #3498db; /* Blue border */
                border-radius: 10px;
                padding: 8px 15px;
                font-size: 16px;
                color: black; /* Set text color to black */
                min-height: 25px;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(resources/down-arrow.png); /* Optional arrow icon */
                width: 12px;
                height: 12px;
            }
            QComboBox:on {
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
            }
            QComboBox QAbstractItemView {
                background-color: white; /* Dropdown menu background color */
                border: 2px solid #3498db; /* Dropdown border */
                border-radius: 0;
                selection-background-color: #3498db; /* Highlight color for selected item */
                color: black; /* Text color for dropdown items */
            }
        """


    def _get_action_button_style(self):
        return """
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 12px;
                font-size: 18px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """

    def _get_message_box_style(self):
        return """
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
        """
    
    def _get_label_style(self):
        return """
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                margin-right: 10px;
            }
        """
    
    def _switch_to_single_mode(self):
        print("Switching to single mode")
        # Don't recreate the widgets, just update the layout
        self._create_player_page(single_player=True)
        
    def _switch_to_two_player_mode(self):
        print("Switching to two player mode")
        # Don't recreate the widgets, just update the layout
        self._create_player_page(single_player=False)



    def _create_mode_select_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(25)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with navigation controls
        header = QHBoxLayout()
        
        # Back button using unicode symbol
        back_btn = QPushButton("←")
        back_btn.setFixedSize(40, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 2px solid rgba(255, 255, 255, 0.7);
                border-radius: 20px;
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        back_btn.clicked.connect(self.close)
        
        # Title (center)
        title = QLabel("Select Mode")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        
        # Add widgets to header
        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Mode selection buttons container
        buttons_container = QVBoxLayout()
        buttons_container.setSpacing(20)
        
        # Create mode selection buttons
        self.one_player_btn = QPushButton("One Player")
        self.two_player_btn = QPushButton("Two Players")
        
        # Style buttons
        for btn in [self.one_player_btn, self.two_player_btn]:
            btn.setStyleSheet(self._get_mode_button_style())
            btn.setFixedHeight(60)
            buttons_container.addWidget(btn)
        
        # Connect buttons
        self.one_player_btn.clicked.connect(lambda: self._show_player_setup(True))
        self.two_player_btn.clicked.connect(lambda: self._show_player_setup(False))
        
        layout.addLayout(buttons_container)
        layout.addStretch()
        
        return page

    def _refresh_page(self):
        """Reset all inputs and return to mode select"""
        self._back_to_mode_select()
        if hasattr(self, 'p1_name'):
            self.p1_name.clear()
        if hasattr(self, 'p2_name'):
            self.p2_name.clear()
        
        # Reset color selections
        if hasattr(self, 'p1_color'):
            self.p1_color.setCurrentIndex(0)
        if hasattr(self, 'p2_color'):
            self.p2_color.setCurrentIndex(0)


    
    def _on_input_changed(self):
        """Handle input changes and validate based on the current mode."""
        self._validate_inputs()  # Call the validation method based on the selected mode










        
