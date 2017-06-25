import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class LoginWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'First App'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = self.createGridLayout()
        self.setLayout(layout)

        self.show()

    def createGridLayout(self):
        self.grid = QGroupBox("User Login")
        
        self.grid.setGeometry(self.left, self.top, self.width/4, self.height/4)

        profilePic = QLabel(self)
        profilePic.setAlignment(Qt.AlignCenter)
        profilePic.setPixmap(QPixmap("avatar.png"))

        btnLogin = QPushButton("Login", self)
        btnLogin.setToolTip("Login User")
        btnLogin.clicked.connect(self.login_click)

        layout = QGridLayout()

        layout.addWidget(QLabel(" ", self), 0, 0)
        layout.addWidget(profilePic, 1, 0)
        layout.addWidget(btnLogin, 2, 0) 
        layout.addWidget(QLabel(" ", self), 3, 0)

        return layout
        

    @pyqtSlot()
    def login_click(self):
        print("User Logged In")       



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = LoginWindow()
    sys.exit(app.exec_())
