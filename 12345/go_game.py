import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from board import GoBoard
from main_menu import MainMenu
from settings_page import SettingsPage
from userPage import UserPage


class GoGame(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            # Initialize player information
            self.player1_name = ""
            self.player1_color = "black"
            self.player2_name = ""
            self.player2_color = "white"
            
            self.setWindowTitle("Go Game")
            # Remove this line since we're going fullscreen
            # self.setGeometry(100, 100, 1024, 768)
            
            # Initialize settings with fullscreen as default
            self.settings = {
                'board_size': 9,
                'timer_minutes': 30,
                'fullscreen': True,  # Changed from False
                'window_fullscreen': False,
                'normal_window': False  # Changed from True
            }

            # Create stacked widget
            self.stacked_widget = QStackedWidget()
            self.setCentralWidget(self.stacked_widget)
            
            # Initialize pages
            self.init_pages()
            self.setup_connections()

            # Keep track of current board
            self.current_board = None

            # Start in fullscreen mode
            self.showFullScreen()

        except Exception as e:
            print(f"Error in initialization: {e}")
            raise

    def init_pages(self):
        # Create pages
        self.main_menu = MainMenu()
        self.settings_page = SettingsPage()
        self.user_page = UserPage()
        
        # Create initial board
        self.current_board = GoBoard()
        self.current_board.set_board_size(self.settings['board_size'])
        self.current_board.back_btn.clicked.connect(self.handle_board_back)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.settings_page)
        self.stacked_widget.addWidget(self.user_page)
        self.stacked_widget.addWidget(self.current_board)

    def setup_connections(self):
        # Main menu connections
        self.main_menu.start_btn.clicked.connect(self.show_user_page)
        self.main_menu.settings_btn.clicked.connect(self.show_settings)
        self.main_menu.exit_btn.clicked.connect(self.close)
        
        # User page connections
        self.user_page.back_btn.clicked.connect(self.show_main_menu)
        self.user_page.start_btn.clicked.connect(self.start_game)

        # Settings page connections
        self.settings_page.back_btn.clicked.connect(self.show_main_menu)
        self.settings_page.apply_btn.clicked.connect(self.apply_settings)

    def show_user_page(self):
        self.stacked_widget.setCurrentWidget(self.user_page)

    def on_board_size_changed(self, size_text):
        """Handle board size changes"""
        try:
            # Extract just the number from the text (e.g., '7×7' becomes 7)
            size = int(size_text.split('×')[0])
            print(f"Emitting board size changed signal: {size}")  # Debug print
            self.board_size_changed.emit(size)
        except ValueError as e:
            print(f"Error converting board size: {e}")

    def start_game(self):
        if self.user_page.validate_input():
            player1_info, player2_info = self.user_page.get_players_info()
            
            try:
                # Create new board
                new_board = GoBoard()
                new_board.set_board_size(self.settings['board_size'])
                new_board.set_player_info(
                    player1_name=player1_info[0],
                    player2_name=player2_info[0]
                )
                
                # Connect back button
                new_board.back_btn.clicked.connect(self.handle_board_back)
                
                # Remove old board if it exists
                if self.current_board is not None:
                    self.stacked_widget.removeWidget(self.current_board)
                    self.current_board.deleteLater()
                
                # Set new board
                self.current_board = new_board
                self.stacked_widget.addWidget(self.current_board)
                self.stacked_widget.setCurrentWidget(self.current_board)
                
            except Exception as e:
                print(f"Error in start_game: {e}")
                import traceback
                traceback.print_exc()

    def show_settings(self):
        self.stacked_widget.setCurrentWidget(self.settings_page)

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)


    def apply_settings(self):
        try:
            new_settings = self.settings_page.get_settings()
            print(f"Applying new settings: {new_settings}")
            
            # Apply board size if changed
            if new_settings['board_size'] != self.settings['board_size']:
                # Create new board with new size
                new_board = GoBoard()
                new_board.set_board_size(new_settings['board_size'])
                new_board.back_btn.clicked.connect(self.handle_board_back)
                
                # Remove old board if it exists
                if self.current_board is not None:
                    self.stacked_widget.removeWidget(self.current_board)
                    self.current_board.deleteLater()
                
                # Set new board
                self.current_board = new_board
                self.stacked_widget.addWidget(self.current_board)
            
            # Apply window mode
            if new_settings['fullscreen']:
                self.showFullScreen()
            elif new_settings['window_fullscreen']:
                self.showMaximized()
            else:
                self.showNormal()
                self.setGeometry(100, 100, 1024, 768)
            
            # Store new settings
            self.settings = new_settings.copy()
            self.show_main_menu()
            
        except Exception as e:
            print(f"Error applying settings: {e}")
            import traceback
            traceback.print_exc()


    def handle_board_back(self):
        """Handle back button click from game board"""
        try:
            # If in fullscreen, return to normal window mode first
            if self.isFullScreen():
                self.showNormal()
                self.settings['fullscreen'] = False
                self.settings['window_fullscreen'] = False
                self.settings['normal_window'] = True
            
            # Show main menu
            self.show_main_menu()
            
        except Exception as e:
            print(f"Error handling board back: {e}")
            import traceback
            traceback.print_exc()

def main():
    try:
        app = QApplication(sys.argv)
        app.setStyle('Fusion')
        game = GoGame()
        game.show()
        return app.exec()
    except Exception as e:
        print(f"Error in main: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())