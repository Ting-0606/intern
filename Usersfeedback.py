from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QComboBox

app = QApplication([])#creating an object that control everything in the GUI
#starting car engine

#messagebox
class Mywindow(QMainWindow):
    def closeWindow(self, event): #as this function will only work when an event happen, so "event"parameter should include in()
        reply = QMessageBox.question(
            self,
            "Exit",#title of the message box
            "Are you sure you want to quit?",#text show in the message box
            QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No, #buttons for selection
            QMessageBox.StandardButton.No #default button
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
        
    closeEvent = closeWindow #assign the function to handle close events

window = Mywindow() 
window.setWindowTitle("A Form")
window.setGeometry(100, 100, 800, 700) 

central_widget = QWidget()
window.setCentralWidget(central_widget)

layoutV = QVBoxLayout()
central_widget.setLayout(layoutV)

#Name input section
Input_name = QLabel("Enter your name:")
User_name = QLineEdit()
layoutH = QHBoxLayout()
layoutH.addWidget(Input_name)
layoutH.addWidget(User_name)
layoutV.addLayout(layoutH)

#Gender Selection(Radio Buttons)

#Interests (Checkboxes)

#Country Dropdown (Combo Box)


window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


