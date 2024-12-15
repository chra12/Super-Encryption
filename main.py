import sys
from PyQt5.QtWidgets import QApplication
from encryption_app import EncryptionApp

def main():
    app = QApplication(sys.argv)
    ex = EncryptionApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
