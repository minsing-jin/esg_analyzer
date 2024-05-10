from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))
        self.setGeometry(300, 300, 300, 200)
        self.show()
