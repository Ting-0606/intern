import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QToolBar
from PyQt6.QtGui import QAction


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyQt6 Simple Example")
        self.setGeometry(400, 700, 400, 300)  # x, y, width, height
        
        # Create a button
        self.button = QPushButton("Click Me!", self)
        self.button.setGeometry(150, 100, 100, 40)  # x, y, width, height
        
        # Connect the button click to a function
        self.button.clicked.connect(self.on_button_click)

        toolbar = QToolBar("Text Toolbar")
        self.addToolBar(toolbar)
        exitAct = QAction("Leave",self)
        exitAct.triggered.connect(self.close)
        toolbar.addAction(exitAct)
            
    def on_button_click(self):
        print("Button was clicked!")
        self.button.setText("Clicked!")
 
    def close(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())