import os
import sys


import ctypes

from PyQt5.QtWidgets import QApplication

if sys.platform.startswith("win"):
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Tazz-GUI")

from views.mainview import MainView

os.chdir(r"G:\My Drive\7. Future_Up\GUI_Python_Project")

if __name__ == '__main__':
    app = QApplication([])
    main_window = MainView()
    main_window.show()
    app.exec_()
