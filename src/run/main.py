import sys
from PyQt5.QtWidgets import QApplication
from ui_layout import UILayout

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UILayout()
    window.setWindowTitle("Minimal Timer Demo")
    window.resize(400, 200)
    window.show()
    sys.exit(app.exec_())
