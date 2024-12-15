import base64
import codecs
import os
import time
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QProgressBar, QWidget, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QColor, QPixmap
from utils import apply_encryption, generate_decryption_code, append_colored_text

# Set up colors
CYAN = QColor(0, 255, 255)  # Light blue color
GREEN = QColor(0, 255, 0)  # Green color
YELLOW = QColor(255, 255, 0)  # Yellow color
RED = QColor(255, 0, 0)  # Red color
MAGENTA = QColor(255, 0, 255)  # Pink color
BLUE = QColor(0, 0, 255)  # Blue color
WHITE = QColor(255, 255, 255)  # White color
SILVER = QColor(192, 192, 192)  # Silver color
GOLD = QColor(255, 215, 0)  # Gold color

# New colors
ORANGE = QColor(255, 165, 0)  # Orange color
LIGHT_BLUE = QColor(173, 216, 230)  # Light blue color
LIGHT_GREEN = QColor(144, 238, 144)  # Light green color
VIOLET = QColor(238, 130, 238)  # Violet color
LIGHT_PINK = QColor(255, 182, 193)  # Light pink color
LIGHT_YELLOW = QColor(255, 255, 224)  # Light yellow color
DARK_BLUE = QColor(0, 0, 139)  # Dark blue color
DARK_RED = QColor(139, 0, 0)  # Dark red color

# Print ASCII Art at the beginning of the script in gold color
ascii_art = """
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

                ███████╗██╗   ██╗██████╗ ███████╗██████╗
                ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗
                ███████╗██║   ██║██████╔╝█████╗  ██████╔╝
                ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗
                ███████║╚██████╔╝██║     ███████╗██║  ██║
                ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝

            ███████╗███╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗
            ██╔════╝████╗  ██║██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗
            █████╗  ██╔██╗ ██║██║     ██████╔╝ ╚████╔╝ ██████╔╝
            ██╔══╝  ██║╚██╗██║██║     ██╔══██╗  ╚██╔╝  ██╔═══╝
            ███████╗██║ ╚████║╚██████╗██║  ██║   ██║   ██║
            ╚══════╝╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝

▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
"""

# Static AES (Fernet) key
key = Fernet.generate_key()
cipher = Fernet(key)

class EncryptionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Super Encryption")
        self.setGeometry(100, 100, 620, 700)

        self.setStyleSheet("background-color: #333333; color: white; font-family: Consolas, monaco;")

        self.init_ui()

    def init_ui(self):
        # Create a window containing the user interface

        # Display ASCII Art in the text output window with orange color
        self.terminal_output = QTextEdit(self)
        self.terminal_output.setReadOnly(True)  # Make the text in the output window non-editable
        self.terminal_output.setStyleSheet(
           "background-color: black; color: white; font-family: Consolas; font-size: 10pt;"
        )
        append_colored_text(self.terminal_output, ascii_art, ORANGE)  # Add the colored text to the output window
        self.terminal_output.setAlignment(Qt.AlignCenter)  # Center the text in the window

        # Create a welcome label
        self.label = QLabel("Welcome to the Super Encryption", self)
        self.label.setAlignment(Qt.AlignCenter)

        # Create a field for entering the number of encryption layers
        self.layer_input = QLineEdit(self)
        self.layer_input.setPlaceholderText("Layers (1-31)")  # Placeholder text
        self.layer_input.setFixedHeight(35)  # Increase the height of the field to make it prominent
        self.layer_input.setAlignment(Qt.AlignCenter)  # Center the text in the field

        # Customize the design of the input field
        self.layer_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {WHITE.name()};  /* White background */
                color: {DARK_BLUE.name()};         /* Text color */
                border: 2px solid {GOLD.name()};   /* Gold border */
                border-radius: 8px;               /* Rounded corners */
                padding: 5px;                     /* Internal spacing */
                font-size: 8pt;                  /* Font size */
            }}
            QLineEdit:focus {{
                border: 2px solid {CYAN.name()};  /* Cyan border when focused */
                background-color: {LIGHT_YELLOW.name()}; /* Light yellow background when focused */
            }}
             """)

        # Create a label to show the default value
        self.layer_label = QLabel("31", self)
        self.layer_label.setAlignment(Qt.AlignCenter)  # Center the text
        self.layer_label.setFixedHeight(35)  # Make the height of the label equal to the input field

        # Customize the design of the label
        self.layer_label.setStyleSheet(f"""
            QLabel {{
                background-color: {SILVER.name()}; /* Silver background */
                color: {DARK_RED.name()};          /* Text color */
                border: 2px solid {GOLD.name()};   /* Gold border */
                border-radius: 8px;               /* Rounded corners */
                font-size: 12pt;                  /* Font size */
                padding: 5px;                     /* Internal spacing */
            }}
             """)

        # Dropdown menu for selecting the encryption type
        self.encryption_choice = QComboBox(self)
        # Add items to the dropdown menu
        self.encryption_choice.addItems([ "All Types Base64 ROT13 Hex Encoding"])
        # Customize the design of the dropdown menu
        self.encryption_choice.setStyleSheet(f"""
            QComboBox {{
                background-color: {ORANGE.name()};  /* Background color */
                color: {DARK_BLUE.name()};         /* Text color */
                border: 2px solid {GOLD.name()};   /* Border */
                border-radius: 8px;               /* Rounded corners */
                padding: 5px;                     /* Internal spacing */
                font-size: 12pt;                  /* Font size */
            }}
            QComboBox:hover {{
                background-color: {LIGHT_GREEN.name()};  /* Background color on hover */
                color: {DARK_RED.name()};               /* Text color on hover */
            }}
            QComboBox:focus {{
                 border: 2px solid {CYAN.name()};        /* Border color when focused */
                 background-color: {LIGHT_BLUE.name()}; /* Background color when focused */
            }}
            QComboBox::drop-down {{
                background-color: {ORANGE.name()};       /* Arrow background color */
                border: none;                          /* No border */
                width: 5px;                           /* Arrow width */
            }}
            QComboBox QAbstractItemView {{
                background-color: {WHITE.name()};      /* Background color of the open menu */
                color: {DARK_BLUE.name()};            /* Text color inside the menu */
                selection-background-color: {CYAN.name()}; /* Background color of the selected item */
                selection-color: {DARK_RED.name()};        /* Text color of the selected item */
                 border: 1px solid {SILVER.name()};         /* Border of the open menu */
             }}
          """)

        # Button to select the file to be encrypted
        self.file_button = QPushButton("Choose File", self)
        self.file_button.clicked.connect(self.choose_file)  # Connect the button to the file selection function
        self.file_button.setFixedSize(150, 40)  # Set the size of the button
        self.file_button.setStyleSheet(f"""
        QPushButton {{
            background-color: {ORANGE.name()};
            color: {DARK_BLUE.name()};
            border: 2px solid {GOLD.name()};   /* Border */
            border-radius: 8px;               /* Rounded corners */
            padding: 5px;                     /* Internal spacing */
            font-size: 12pt;                  /* Font size */
        }}
        QPushButton:hover {{
            background-color: {LIGHT_GREEN.name()};
        }}
        QPushButton:pressed {{
            background-color: {GOLD.name()};
        }}
          """)

        # Button to encrypt the file
        self.encrypt_button = QPushButton("Encrypt", self)
        self.encrypt_button.clicked.connect(self.encrypt_file)  # Connect the button to the encryption function
        self.encrypt_button.setFixedSize(150, 40)  # Set the size of the button
        self.encrypt_button.setStyleSheet(f"""
           QPushButton {{
                background-color: {ORANGE.name()};
                color: {DARK_BLUE.name()};         /* Text color */
                border: 2px solid {GOLD.name()};   /* Border */
                border-radius: 8px;               /* Rounded corners */
                padding: 5px;                     /* Internal spacing */
                font-size: 12pt;                  /* Font size */
            }}
            QPushButton:hover {{
                background-color: {LIGHT_GREEN.name()};
            }}
            QPushButton:pressed {{
               background-color: {GOLD.name()};
            }}
        """)

        # Progress bar to display encryption progress
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)  # Center the text

        # Set up the vertical layout for the interface elements
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)  # Center the elements in the layout

        # Add interface elements to the layout
        self.layout.addWidget(self.terminal_output)  # Text output window
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)  # Label
        self.layout.addWidget(self.layer_input, alignment=Qt.AlignCenter)  # Layer input field
        self.layout.addWidget(self.encryption_choice, alignment=Qt.AlignCenter)  # Dropdown menu
        self.layout.addWidget(self.file_button, alignment=Qt.AlignCenter)  # File selection button
        self.layout.addWidget(self.encrypt_button, alignment=Qt.AlignCenter)  # Encryption button
        self.layout.addWidget(self.progress_bar)  # Progress bar

        # Add an icon at the bottom of the interface
        self.icon_label = QLabel(self)
        pixmap = QPixmap("encryption-icon.png")  # Load the icon file (adjust the path if necessary)
        pixmap = pixmap.scaled(
            60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )  # Scale the icon to 60x60 while maintaining the aspect ratio
        self.icon_label.setPixmap(pixmap)  # Set the icon
        self.icon_label.setAlignment(Qt.AlignCenter)  # Center the icon

        # Set up the main container for the interface
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)  # Set the container as the main window
        self.layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)  # Add the icon to the layout

        # Show the window
        self.show()

    def choose_file(self):
        options = QFileDialog.Options()
        # Add support for multiple types of programming files
        file, _ = QFileDialog.getOpenFileName(self, "Select a File", "",
    "All Files (*.*);;Python Files (*.py);;JavaScript Files (*.js);;"
    "Ruby Files (*.rb);;C++ Files (*.cpp);;"
    " Bash Files  (*.sh);;"
    " PowerShell Files (*.ps1);;",
    options=options)
        if file:
            self.selected_file = file
            self.label.setText(f"Selected file: {self.selected_file}")
            append_colored_text(self.terminal_output, f"File Selected: {file}", GREEN)

    def encrypt_file(self):
        self.terminal_output.clear()
        append_colored_text(self.terminal_output, ascii_art, ORANGE)
        self.terminal_output.setAlignment(Qt.AlignCenter)  # Center the text in the window

        if hasattr(self, 'selected_file'):
            try:
                layers = int(self.layer_input.text())
                # Check the number of layers
                if layers < 1 or layers > 31:
                    self.label.setText("Error: The number of layers must be between 1 and 31!")
                    append_colored_text(self.terminal_output, "Error: The number of layers must be between 1 and 31!", RED)
                    return
            except ValueError:
                self.label.setText("Error: Please enter a valid number for layers!")
                append_colored_text(self.terminal_output, "Error: Invalid input for layers!", RED)
                return

            encryption_choice = self.encryption_choice.currentText()
            encrypted_code, time_taken = apply_encryption(self.selected_file, layers, encryption_choice, self.terminal_output)

            # Determine the file name and extension based on the original file
            file_dir = os.path.dirname(self.selected_file)  # Directory path
            file_name, file_extension = os.path.splitext(os.path.basename(self.selected_file))  # File name and extension
            output_file = os.path.join(file_dir, f"{file_name}_encrypted{file_extension}")  # Determine the name of the encrypted file

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(generate_decryption_code(encrypted_code, layers, file_extension))

            self.label.setText(f"Encrypted script saved as: {output_file}")
            append_colored_text(self.terminal_output, f"File saved as: {output_file}", CYAN)
        else:
            self.label.setText("Please select a file first!")
            append_colored_text(self.terminal_output, "Error: No file selected!", RED)
