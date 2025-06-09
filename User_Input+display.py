from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QLineEdit

app = QApplication([])#creating an object that control everything in the GUI
#starting car engine

window = QMainWindow() #create blank window
window.setWindowTitle("Greeting App")
window.setGeometry(100, 100, 800, 700) 

#centre a button
central_widget = QWidget()#create a container (for placing the vertical box) and set to center
window.setCentralWidget(central_widget)

#create label for user's input
Question = QLabel("What is your name?")#QLabel:display text
user_name_input = QLineEdit()#text box for user input
output_for_greeting = QLabel(" ") 



layout = QVBoxLayout()#create a vertical layout (Vertical box)
layout = QHBoxLayout()
layout.addStretch()# add sth above/on the left of the bottom


button = QPushButton("Enter", parent = window)#make the button a child of the window

layout.addWidget(Question)
layout.addWidget(user_name_input)
layout.addWidget(button)#add the button to the box
layout.addWidget(output_for_greeting)

layout.addStretch()#add sth under/on the right of the bottom

central_widget.setLayout(layout)#apply layout to the container(putting the box into it)

def button_click():#function to run when the button is clicked
    name = user_name_input.text()#.text(): gets text from QLineEdit
    output_for_greeting.setText(f"Hello, {name}!")#.setText: update QLabel's text

button.clicked.connect(button_click)#connect the click event to button_click function


window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


