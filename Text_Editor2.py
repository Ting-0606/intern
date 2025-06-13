from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel, QApplication, QTextEdit, QListWidget, QFileDialog, QDockWidget, QWidget, QPlainTextEdit, QToolBar
from PyQt6.QtGui import QAction, QIcon, QPainter, QTextFormat
from PyQt6.QtCore import Qt, QRect, QSize
import sys #sys exit handling
'''qtW for ui component
qtg for graphic
qtc for non-gui functionality'''

class LineNumberArea (QWidget):
    def __init__(self, editor):
        super().__init__(editor)#glued to the editor
        self.editor = editor #rmb which editor
    """this allow LineNumberArea know which editor it's for, 
so when editor scrolls, line number scroll"""

    def sizeHint(self): #originally, it used to suggest what size the widget(line no. area) need, but now customize using QSize()
        return QSize(self.editor.line_number_area_width(),0);'''get the width from the main editor 
and 0 for height means it will stretch to match the editor'''

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)
        '''editor.line....event is a method draw line number, match them up with 
        correct lines of text and handle scrolling synchronization'''

    

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

  
    
    #line no. methods 
    #calculating Line No. area width
    def line_number_area_width(self):
        digits = len(str(max(1,self.text_area.blockCount())))#count digits in total lines
        '''max(1,...) ensure at least 1 line'''
        space = 20 + self.fontMetrics().horizontalAdvance('9') * digits #width = padding + (digit_width * digit_count)
        return space
        '''9 is the widest digit,and the .font...Advance() get the pixel width of it'''

    
    #updating margin width
    def update_line_number_area_width(self):
        self.text_area.setViewportMargins(self.line_number_area_width(),0, 0, 0)#(left, top, right, bottom)

    #painting line number
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area) #create painter for line number area
        painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)#gray bg
        '''fillRect() fills a rectangle with a solid color;
        event.rect() is the region needing repaint, like you scroll, 
        newly exposed area is in event.rect()'''

        #finds where to draw first line number
        block = self.text_area.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.text_area.blockBoundingGeometry(block).translated(
            self.text_area.contentOffset()).top()
        '''blockboundingGeometry() give the line position relative to document;
        translated() adjust the position by adding scroll offset;
        contentOffset() returns how much the text is scrolled
        top()extract the y-position of the line top edge'''
        bottom = top + self.text_area.blockBoundingRect(block).height() #y-position of bottom edge

        #drawing visible line no.
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(0, int(top), #X=0, Y=line top position
                            self.line_number_area.width(), 
                            self.fontMetrics().height(), #height of a line
                            Qt.AlignmentFlag.AlignCenter, #right align no.
                            str(block_number))
            
            block = block.next() #go to next text line
            top = bottom #current bottom become next top
            bottom = top + self.text_area.blockBoundingRect(block).height() #update bottom Y-position
            block_number += 1


    def resizeEvent(self, event): #maintain side widgets (like line no.) in sync with their main content area
        super().resizeEvent(event) #call parent resize handler
        cr = self.text_area.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), 
                                        self.line_number_area_width(), cr.height()))

    def update_line_number_area(self, rect, dy):
       
        if dy:#scroll delta
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), 
                self.line_number_area.width(), 
                rect.height()
            )
        
        # Ensure full update if needed
        if rect.contains(self.text_area.viewport().rect()):
            self.update_line_number_area_width()



    def init_ui(self): #UI setup


        #add text area
        self.text_area = QPlainTextEdit()#creat central text widget
        self.setCentralWidget(self.text_area)#make the area fill the window 

        #line numbers
        self.line_number_area = LineNumberArea(self)


        self.text_area.setViewportMargins(self.line_number_area_width(), 0, 0, 0)#so that first line will not cover by gray region
        self.text_area.blockCountChanged.connect(self.update_line_number_area_width)#see the changes in the no. of text lines/blocks, block = a line
        self.text_area.updateRequest.connect(self.update_line_number_area)#see any visual updates, like scrolling


        #create toolbar
        toolbar = QToolBar("Main Toolbar",self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea,toolbar) #create a menu bar, "Main Toolbar" is the name
        toolbar.setMovable(False)        


        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        #New file action
        new_action= QAction(QIcon.fromTheme("document-new"),"New", self) #Qaction made a clickable icon, "QIcon.fromTheme("icon name")" set icon for the actrion
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)

        #Open_file action
        open_action= QAction(QIcon.fromTheme("document-open"),"Open", self)  
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        #Save file action
        save_action= QAction(QIcon.fromTheme("document-save"),"Save", self) 
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        toolbar.addSeparator()#visual separation

        #Exit action
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

       

        #copy
        copy_action = QAction(QIcon.fromTheme("edit-copy"),"Copy", self)
        copy_action.triggered.connect(self.text_area.copy)
        toolbar.addAction(copy_action)

        #paste
        paste_action = QAction(QIcon.fromTheme("edit-paste"),"&Paste", self)
        paste_action.triggered.connect(self.text_area.paste)
        toolbar.addAction(paste_action)

        #help menu
        help_menu = menu.addMenu("&Help")
        
        #About
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Create status bar
        self.status_bar = self.statusBar()
        
        # Add permanent widgets
        self.line_col_label = QLabel("Line: 1, Col: 1")
        self.status_bar.addPermanentWidget(self.line_col_label)
        
        # Connect cursor changes
        self.text_area.cursorPositionChanged.connect(self.update_cursor_position)

    def update_cursor_position(self):
        """Update line/col display"""
        cursor = self.text_area.textCursor()
        line = cursor.blockNumber() + 1  # 0-index to 1-index
        col = cursor.columnNumber() + 1
        
        self.line_col_label.setText(f"Line: {line}, Col: {col}")


if __name__== "__main__": #checks of the script is being run directly
    app = QApplication(sys.argv) 
    '''QApplication like the brain of robot, sys.argv like the instructions for the robot,
     turning on the brain with instruction '''
    editor = TextEditor()
    editor.show()
    print(editor.sizeHint())
    sys.exit(app.exec())
    '''"app.exec()" keep the app running in a loop and when user close the window it returns a 
    exit code, when "sys.exit" receive an exit code, it exit python'''


        
       