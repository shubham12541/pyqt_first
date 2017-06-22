import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import mainwindow_auto

class MainWindow(QMainWindow, mainwindow_auto.Ui_MainWindow):

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.modifyUI()
        self.btnLogin.clicked.connect(lambda: self.pressedLogin())

    def modifyUI(self):
        pic = QLabel(self)
        pic.setAlignment(Qt.AlignCenter)
        pic.setPixmap(QPixmap("avatar.jpg"))
        pic.show()

    def pressedLogin(self):
        print("Logged In")  
    

def main():
    app = QApplication(sys.argv)
    form = MainWindow() 
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


