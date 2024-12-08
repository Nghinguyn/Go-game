from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QProgressBar, QSlider, QVBoxLayout, QWidget
from PyQt6.uic.properties import QtWidgets


class DrawingCanvas:
    pass


def setupUi(self):
    """
    Set up the main UI components and layout.
    """
    # Apply stylesheet
    self.setStyleSheet("""
        /* Existing stylesheet code */
    """)

    # Create main widget and layout
    mainWidget = QWidget(self)
    self.setCentralWidget(mainWidget)
    mainLayout = QHBoxLayout(mainWidget)

    # Initialize canvas and sidebar
    self.canvas = DrawingCanvas()
    self.sidebar = self.createSidebar()

    # Add sidebar and canvas to main layout
    mainLayout.addWidget(self.sidebar)
    mainLayout.addWidget(self.canvas)

    # Create menu bar with File and Help menus
    self.fileMenu = self.menuBar().addMenu("File")
    self.helpMenu = self.menuBar().addMenu("Help")

    # Add the file and help actions...
    # (existing menu actions)

def createSidebar(self):
    """
    Create the sidebar with game information, controls, and the tab widget.
    """
    sidebar = QWidget()
    sidebar.setFixedWidth(200)
    layout = QVBoxLayout(sidebar)

    # Header
    header = QLabel("Pictionary", sidebar)
    header.setObjectName("header")
    header.setAlignment(Qt.AlignmentFlag.AlignCenter)
    header.setFont(QtGui.QFont("Arial", 19, QtGui.QFont.Weight.Bold))

    # Countdown Timer Label
    self.countdownLabel = QLabel("Time Left: --:--", sidebar)
    self.countdownLabel.setObjectName("countdownLabel")
    self.countdownLabel.setFont(QtGui.QFont("", 12, QtGui.QFont.Weight.Bold))
    self.countdownLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.countdownLabel.setVisible(False)

    # Progress Bar for Timer
    self.progressBar = QProgressBar(sidebar)
    self.progressBar.setRange(0, self.timer_duration)
    self.progressBar.setValue(self.timer_duration)
    self.progressBar.setVisible(False)

    # Player turn and score
    self.playerTurn = QLabel("Player Turn", sidebar)
    self.scoreLabel = QLabel(sidebar)
    self.scoreLabel.setObjectName("scoreLabel")
    self.updateScores()

    # Brush size using QSlider
    brushLabel = QLabel("Brush size:", sidebar)
    brushLayout = QHBoxLayout()
    self.sizeSlider = QSlider(Qt.Orientation.Horizontal, sidebar)
    self.sizeSlider.setRange(1, 50)
    self.sizeSlider.setValue(4)
    self.sizeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
    self.sizeSlider.setTickInterval(5)
    self.sizeSlider.valueChanged.connect(self.changeBrushSize)
    self.brushSizeLabel = QLabel(f"{self.sizeSlider.value()}", sidebar)
    brushLayout.addWidget(self.sizeSlider)
    brushLayout.addWidget(self.brushSizeLabel)

    # Color selection using a color wheel (QColorDialog)
    selectColor = QLabel("Select color:", sidebar)
    self.colorButton = QPushButton("Choose Color", sidebar)
    self.colorButton.clicked.connect(self.openColorDialog)
    self.currentColorDisplay = QLabel("", sidebar)
    self.currentColorDisplay.setObjectName("currentColorDisplay")
    self.currentColorDisplay.setFixedSize(30, 30)
    self.currentColorDisplay.setStyleSheet(f"background-color: {self.canvas.brushColor.name()};")
    self.currentColorDisplay.setFrameShape(QtWidgets.QFrame.Shape.Box)
    colorLayout = QHBoxLayout()
    colorLayout.addWidget(self.colorButton)
    colorLayout.addWidget(self.currentColorDisplay)

    # Note
    note = QLabel("** Note **\nFor every correct guess, \n"
                  "the guesser gets 2 points \n"
                  "and the drawer gets 1.\nPress Ctrl + K to skip round")
    note.setWordWrap(True)

    # Skip button
    skipButton = QPushButton("Skip round", sidebar)
    skipButton.setObjectName("skipButton")
    skipButton.setStyleSheet("background-color: #dc3545; color: white;")
    skipButton.clicked.connect(self.skipRound)
    skipButton.setShortcut("Ctrl+K")

    # Add tab widget to the sidebar
    self.tabWidget = self.createTabWidget()
    layout.addWidget(header)
    layout.addWidget(self.countdownLabel)
    layout.addWidget(self.progressBar)
    layout.addWidget(self.playerTurn)
    layout.addWidget(self.scoreLabel)
    layout.addWidget(brushLabel)
    layout.addLayout(brushLayout)
    layout.addWidget(selectColor)
    layout.addLayout(colorLayout)
    layout.addWidget(note)
    layout.addWidget(skipButton)
    layout.addWidget(self.tabWidget)  # Add the Tab Widget here

    # Add a spacer to prevent stretching at the bottom
    layout.addSpacerItem(
        QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding))

    return sidebar
