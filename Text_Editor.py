from PyQt6.QtWidgets import QMainWindow, QMessageBox, QApplication, QTextEdit, QListWidget, QFileDialog, QDockWidget
from PyQt6.QtGui import QAction, QIcon #QAction create menu items
from PyQt6.QtCore import Qt
import sys #sys exit handling


class TextEditor (QMainWindow): #main application of the class from QMainWindow
#create window  
    def __init__(self):#instruction of setting up a window
        super().__init__() #instruction follow the QMainWindow 

        #window properties
        self.setWindowTitle("Text editor by PyQt6")
        self.setGeometry(100,100,800,600)

        self.init_ui() #all UI setup will be inside here
    
    #add file actions
    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        path, _ =  QFileDialog.getOpenFileName(#open system file picker dialog , "path , _" unpacks the tuple, storing path as str, as "open()" read str not tuple
            self,
            "Open File", #title of the dialog window
            "", #start in current directory
            "Text (*.txt);;All Files(*)"#file filters(user can choose between two), ";;"seperate options
        )
        if path:#check if path is not empty
            try: #if nothing wrong then code will run the following
                with open(path,'r') as file: #with: ensure file closed after reading
                    self.text_area.setText(file.read())#"file.read()" means read file content as string, "self.text_area.setText()" display

            except Exception as error : #when error occurs, python raises an "Exception", python catch error and store in "error"
                QMessageBox.warning(
                    self,#make current window be parent of this box, so it will appear in center of window
                    "Error",# title
                    f"Failed to open file :/n{str(error)}"
                )


    def save_file(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "Text Files (*txt);;All Files(*)"
        )
        if path:
            try:
                with open(path, 'w') as file:
                    file.write(self.text_area.toPlainText())#"self.text_area.toPlainText()"extracts text from text area
                    #"file.write()" write those extracted words into the file.
            except Exception as e:
                QMessageBox.warning(
                    self,#make current window be parent of this box, so it will appear in center of window
                    "Error",# title
                    f"Failed to save file :/n{str(e)}"
                )        


    def show_about(self):
        QMessageBox.about(
            self,
            "About",
            "Text editor built by PyQt6"
        )

    def closeEvent(self,event):
        if self.text_area.document().isModified():#"isModified" is a method of QTextDocument not QTextEdit(text_area), so "document()" is needed
            reply = QMessageBox.question(
                self,
                "Unsaved",
                "Do you want to save before quitting?",
                QMessageBox.StandardButton.Save|QMessageBox.StandardButton.No|QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel
            )
            if reply == QMessageBox.StandardButton.Save:
                self.save_file()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return#stop the code here, prevent the code run continuously to "event.accrpt()"
        event.accept()
        
    




    def init_ui(self): #UI setup
        #add text area
        self.text_area = QTextEdit()#creat central text widget
        self.setCentralWidget(self.text_area)#make the area fill the window 

        #menu system
        menubar = self.menuBar() #create a menu bar

        #file menu
        file_menu = menubar.addMenu("&File") #& = Alt + F shortcut

        #New file action
        new_action= QAction("&New", self) #Qaction made a clickable menu item 
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)

        #Open_file action
        open_action= QAction("&Open", self) #Qaction made a clickable menu item 
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)

        #Save file action
        save_action= QAction("&Save", self) #Qaction made a clickable menu item 
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        file_menu.addSeparator()#visual separation

        #Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        #edit menu
        edit_menu = menubar.addMenu("&Edit")

        #copy
        copy_action = QAction("&Copy", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.text_area.copy)
        edit_menu.addAction(copy_action)

        #paste
        paste_action = QAction("&Paste", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.text_area.paste)
        edit_menu.addAction(paste_action)

        #help menu
        help_menu = menubar.addMenu("&Help")
        
        #About
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)



if __name__== "__main__": #checks of the script is being run directly
    app = QApplication(sys.argv) 
    '''QApplication like the brain of robot, sys.argv like the instructions for the robot,
     turning on the brain with instruction '''
    editor = TextEditor()
    editor.show()
    sys.exit(app.exec())
    '''"app.exec()" keep the app running in a loop and when user close the window it returns a 
    exit code, when "sys.exit" receive an exit code, it exit python'''


        
       