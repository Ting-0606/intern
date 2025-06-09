from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

app = QApplication([])#creating an object that control everything in the GUI
#starting car engine

window = QMainWindow() #create blank window
window.setWindowTitle("My first app")
window.setGeometry(100, 100, 800, 700) 

window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


