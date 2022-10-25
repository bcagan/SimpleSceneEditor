import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot



class Object3D:
    def __init__(self):
        color = [122,122,122] #All objects default to gray
        translation = [0.0,0.0,0.0]
        indicator = 0 #0 = not any object
        #Rotation defined once I figure out how to implement quaternions

    def delete(self, list):
        #Take list, remove object from list
        list.update()
        
    def editprompt(self,list):
        #create edit plane
        pass

    def edit(self,list):
        self.delete(list)
        #modify list
        list.update()

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        scale = [1.0,1.0,1.0]
        indicator = 1 #1 = cube

class Sphere(Object3D):
    
    def __init__(self):
        super().__init__()
        radius = 1.0
        indicator = 2 #2 = sphere

class MyWidget (QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hello World", "Konnichiha Sekai", "Ohayou Tokyo", "G'day Mate"]

        self.button = QtWidgets.QPushButton("Click here")
        
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())
