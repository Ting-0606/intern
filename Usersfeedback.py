from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QButtonGroup, QHBoxLayout, QVBoxLayout, QMainWindow, QLabel, QLineEdit, QMessageBox, QCheckBox, QRadioButton, QComboBox, QSpinBox

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
        


    def on_submit_clicked(self): #self: 
        
        reply = QMessageBox.question(
            self,
            "Confirm Submission",
            "Are you sure you want to submit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()  #self so specific window close


    def clear_clicked(self):
        User_name.clear()
        User_name.setFocus()#put cursor back to the name field

        gender_group.setExclusive(False) ;"""QButtonGroup designed have 1 default choice due to 
        auto-exclusive so need clear them before cleaning the option then restore the exclusivity"""
        male.setChecked(False)
        female.setChecked(False)
        other.setChecked(False)
        gender_group.setExclusive(True)#restore the exclusivity

        spinbox.setValue(18)

        music.setChecked(False)
        sports.setChecked(False)
        reading.setChecked(False)

        country.setCurrentIndex(0)
        
        



    closeEvent = closeWindow #assign the function to handle close events
'''class: house blue print
def : ability for house
self : refering to specific house'''   

    
  
            
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
gender_label = QLabel("Gender:")
male = QRadioButton("Male")
female = QRadioButton("Female")
other = QRadioButton("Other")

gender_group = QButtonGroup() #groups the radio buttons so can select one button at once
gender_group.addButton(male)
gender_group.addButton(female)
gender_group.addButton(other)

layoutV_gender = QVBoxLayout()
layoutH_gender = QHBoxLayout()

layoutV_gender.addWidget(male)
layoutV_gender.addWidget(female)
layoutV_gender.addWidget(other)
layoutH_gender.addWidget(gender_label)
layoutH_gender.addLayout(layoutV_gender)
layoutH_gender.addStretch()
layoutV.addLayout(layoutH_gender)

#age
spinbox = QSpinBox()
spinbox.setRange(18, 100)
spinbox.setValue(18) #default value
spinbox.setSingleStep(1) #increment/decrement step

age_label = QLabel(f"Age:")
layoutH_age = QHBoxLayout()
layoutH_age.addWidget(age_label)
layoutH_age.addWidget(spinbox)
layoutH_age.addStretch()
layoutV.addLayout(layoutH_age)


#Interests (Checkboxes)
interest_label = QLabel("Interests:")
music = QCheckBox("Music") #qcheckbox : square box that can toggled
sports = QCheckBox("Sports")
reading = QCheckBox("Reading")

layoutV_interest = QVBoxLayout()
layoutH_interest = QHBoxLayout()

layoutH_interest.addWidget(interest_label)
layoutV_interest.addWidget(music)
layoutV_interest.addWidget(sports)
layoutV_interest.addWidget(reading)
layoutH_interest.addLayout(layoutV_interest)
layoutH_interest.addStretch()
layoutV.addLayout(layoutH_interest)

#Country Dropdown (Combo Box)
country_label = QLabel("Country:")
country = QComboBox() #dropdown selection menu
country.addItems(["Select Country","USA","UK","Canada","Australia","China"])
layoutV_country = QVBoxLayout()
layoutV_country.addWidget(country_label)
layoutV_country.addWidget(country)
layoutV.addLayout(layoutV_country)
layoutV.addStretch()







#submit button
submit = QPushButton("Submit", parent = window)
submit.clicked.connect(window.on_submit_clicked) #window. : to call the def in MyWindow()


#clear form button
clear = QPushButton("Clear Form", parent=window)
clear.clicked.connect(window.clear_clicked)
layoutH1 = QHBoxLayout()
layoutH1.addWidget(submit)
layoutH1.addWidget(clear)
layoutV.addLayout(layoutH1)

window.show()

app.exec()#event loop that keep the app running
#keep the engine running until user turn off


