from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow

app = QApplication([])#creating an object that control everything in the GUI
#starting car engine

window = QMainWindow() #create blank window
window.setWindowTitle("Button Example")
window.setGeometry(100, 100, 800, 700) 

#centre a button
central_widget = QWidget()#create a container (for placing the vertical box) and set to center
window.setCentralWidget(central_widget)

layout = QVBoxLayout()#create a vertical layout (Vertical box)
layout = QHBoxLayout()
layout.addStretch()# add sth above/on the left of the bottom


button = QPushButton("Click me", parent = window)#make the button a child of the window
layout.addWidget(button)#add the button to the box

layout.addStretch()#add sth under/on the right of the bottom

central_widget.setLayout(layout)#apply layout to the container(putting the box into it)

def button_click():#function to run when the button is clicked
    print("Clicked")

button.clicked.connect(button_click)#connect the click event to button_click function

window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


