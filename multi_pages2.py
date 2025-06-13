from PyQt6.QtWidgets import QApplication, QBoxLayout, QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton

class mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-page Layouts")
        self.setGeometry(100, 100, 400, 300)

        self.init_ui()

    def init_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        #create pages
        self.main()
        self.home()
        self.setting()
        self.fill()

    def main(self):
        page = QWidget()
        label = QLabel("Main")
        
        Home_btn = QPushButton("Home")
        Sett_btn = QPushButton("Setting")
        Fill_btn = QPushButton("Fill")

        Home_btn.clicked.connect(lambda:self.stack.setCurrentIndex(1))
        Fill_btn.clicked.connect(lambda:self.stack.setCurrentIndex(3))
        Sett_btn.clicked.connect(lambda:self.stack.setCurrentIndex(2))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Home_btn)
        layout.addWidget(Sett_btn)
        layout.addWidget(Fill_btn)

        page.setLayout(layout)
        self.stack.addWidget(page) #index0

    def home (self):
        page = QWidget() #make the page be widget so later can add to stack
        label = QLabel("Home")

        Sett_btn = QPushButton("Setting")
        Fill_btn = QPushButton("Fill")
        Main_btn = QPushButton("Main")

        Main_btn.clicked.connect(lambda:self.stack.setCurrentIndex(0))
        Fill_btn.clicked.connect(lambda:self.stack.setCurrentIndex(3))
        Sett_btn.clicked.connect(lambda:self.stack.setCurrentIndex(2))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Main_btn)
        layout.addWidget(Fill_btn)
        layout.addWidget(Sett_btn)

        page.setLayout(layout)
        self.stack.addWidget(page) #index1

    def setting (self):
        page = QWidget() #make the page be widget so later can add to stack
        label = QLabel("Setting")

        Home_btn = QPushButton("Home")
        Fill_btn = QPushButton("Fill")
        Main_btn = QPushButton("Main")

        Main_btn.clicked.connect(lambda:self.stack.setCurrentIndex(0))
        Fill_btn.clicked.connect(lambda:self.stack.setCurrentIndex(3))
        Home_btn.clicked.connect(lambda:self.stack.setCurrentIndex(1))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Main_btn)
        layout.addWidget(Fill_btn)
        layout.addWidget(Home_btn)

        page.setLayout(layout)
        self.stack.addWidget(page) #index2

    def fill (self):
        page = QWidget() #make the page be widget so later can add to stack
        label = QLabel("Fill")

        Sett_btn = QPushButton("Setting")
        Home_btn = QPushButton("Home")
        Main_btn = QPushButton("Main")

        Main_btn.clicked.connect(lambda:self.stack.setCurrentIndex(0))
        Home_btn.clicked.connect(lambda:self.stack.setCurrentIndex(1))
        Sett_btn.clicked.connect(lambda:self.stack.setCurrentIndex(2))

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Main_btn)
        layout.addWidget(Home_btn)
        layout.addWidget(Sett_btn)

        page.setLayout(layout)
        self.stack.addWidget(page) #index3








if __name__ == "__main__":
    app = QApplication([])
    window = mywindow()
    window.show()
    app.exec()