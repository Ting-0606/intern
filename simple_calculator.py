from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QLineEdit

app = QApplication([])#creating an object that control everything in the GUI
#starting car engine

window = QMainWindow() #create blank window
window.setWindowTitle("Simple Calculator")
window.setGeometry(100, 100, 800, 700) 

#centre a button
central_widget = QWidget()#create a container (for placing the vertical box) and set to center
window.setCentralWidget(central_widget)

#create label for user's input
Enter_number1 = QLabel("Enter number:")#QLabel:display text
Enter_number2 = QLabel("Enter number:")#QLabel:display text
Input1 = QLineEdit()#text box for user input
Input2 = QLineEdit()#text box for user input
Answer = QLabel(" ") 


plus_button = QPushButton("+", parent = window)#make the button a child of the window
minus_button = QPushButton("-", parent = window)#make the button a child of the window
times_button = QPushButton("x", parent = window)#make the button a child of the window
divide_button = QPushButton("/", parent = window)#make the button a child of the window


layoutH = QHBoxLayout()
layoutH.addStretch()# add sth above/on the left of the bottom

layoutH.addWidget(plus_button)#add the button to the box
layoutH.addWidget(minus_button)
layoutH.addWidget(times_button)
layoutH.addWidget(divide_button)

layoutH.addStretch()# add sth above/on the left of the bottom


layoutV = QVBoxLayout()#create a vertical layout (Vertical box)
layoutV.addStretch()

layoutV.addWidget(Enter_number1)
layoutV.addWidget(Input1)
layoutV.addLayout(layoutH)#like putting a smallerbox(layoutH) into a larger box(layoutV)
layoutV.addWidget(Enter_number2)
layoutV.addWidget(Input2)
layoutV.addWidget(Answer)

layoutV.addStretch()#add sth under/on the right of the bottom

layoutH1 = QHBoxLayout()
layoutH1.addStretch()

layoutH1.addLayout(layoutV)

layoutH1.addStretch()

central_widget.setLayout(layoutH1)#apply layout(layoutH1) to the container(central_widget)(putting the box into container)

def plus():#function to run when the button is clicked
    number1 = Input1.text()#.text(): gets text from QLineEdit
    number2 = Input2.text()#.text(): gets text from QLineEdit
    ans = float(number1) + float(number2)
    Answer.setText(f"The answer is {ans}!")#.setText: update QLabel's text

def minus():#function to run when the button is clicked
    number1 = Input1.text()#.text(): gets text from QLineEdit
    number2 = Input2.text()#.text(): gets text from QLineEdit
    ans = float(number1) - float(number2)
    Answer.setText(f"The answer is {ans}!")#.setText: update QLabel's text

def times():#function to run when the button is clicked
    number1 = Input1.text()#.text(): gets text from QLineEdit
    number2 = Input2.text()#.text(): gets text from QLineEdit
    ans = float(number1) * float(number2)
    Answer.setText(f"The answer is {ans}!")#.setText: update QLabel's text

def divide():#function to run when the button is clicked
    number1 = Input1.text()#.text(): gets text from QLineEdit
    number2 = Input2.text()#.text(): gets text from QLineEdit
    ans = float(number1)/float(number2)
    Answer.setText(f"The answer is {ans}!")#.setText: update QLabel's text

plus_button.clicked.connect(plus)#connect the click event to button_click function
minus_button.clicked.connect(minus)#connect the click event to button_click function
times_button.clicked.connect(times)#connect the click event to button_click function
divide_button.clicked.connect(divide)#connect the click event to button_click function


window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


