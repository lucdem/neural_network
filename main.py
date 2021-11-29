import sys

from PyQt5.QtWidgets import QApplication

from gui.main_window import MainWindow
from app import NetManager


app = QApplication(sys.argv)

net_manager = NetManager()
window = MainWindow(net_manager)

app.exec()