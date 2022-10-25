from pickle import OBJ
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot



class Object3D:
    def __init__(self):
        self.name = ""
        self.color = [122,122,122] #All objects default to gray
        self.translation = [0.0,0.0,0.0]
        self.indicator = 0 #0 = not any object
        #Rotation defined once I figure out how to implement quaternions

    def delete(self, list):
        #Take list, remove object from list
        list.deleteObject(self)
        list.update()
        
    def editprompt(self,list):
        #create edit plane
        pass

    def edit(self,list):
        list.modifyObject(self)
        list.update()

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        self.scale = [1.0,1.0,1.0]
        self.indicator = 1 #1 = cube
        self.name = "cube" #will be changed in add to dict

class Sphere(Object3D):
    
    def __init__(self):
        super().__init__()
        self.radius = 1.0
        self.indicator = 2 #2 = sphere
        self.name = "sphere" #will be changed in add to dict

class ObjectList():

    def __init__(self):
        self.objectDict = {}
        self.cubeNum = 0
        self.sphereNum = 0

    def addObject(self, object):
        if object.indicator == 0:
            pass
        elif object.indicator == 1: #cube
            newName = "cube" + str(self.cubeNum)
            self.cubeNum += 1
            object.name = newName
            self.objectDict[object.name] = object
        else:
            newName = "sphere" + str(self.sphereNum)
            self.sphereNum += 1
            object.name = newName

    def deleteObject(self, object):
        if object.indicator == 0:
            pass
        self.objectDict.pop(object.name)


    def modifyObject(self, object):
        if object.indicator == 0:
            pass
        self.objectDict[object.name]

    def update(self):
        pass

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
