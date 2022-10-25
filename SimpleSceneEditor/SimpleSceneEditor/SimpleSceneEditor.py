from pickle import OBJ
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import *



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

    def rename(self,list):
        pass

    def updateTraslation(self, newTranslation):
        self.translation = newTranslation

    def updateRotation(self, newRotation):
        self.rotation = newRotation
    
    def updateColor(self, newColor):
        self.color = newColor

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        self.scale = [1.0,1.0,1.0]
        self.indicator = 1 #1 = cube
        self.name = "cube" #will be changed in add to dict

    def updateScale(self, newScale):
        self.scale = newScale
        
    def editprompt(self,list):
        #create cube edit plane

        #Text fields: translation (x,y,z)
        # rotation (x,y,z)
        # color (r,g,b)
        # scale (x,y,z)

        #Create Field Items
        
        self.translationFieldX = QLineEdit(str(self.translation[0]))
        self.translationFieldY = QLineEdit(str(self.translation[1]))
        self.translationFieldZ = QLineEdit(str(self.translation[2]))
        self.translationButton = QPushButton("Update Translation")
        
        self.rotationFieldX = QLineEdit(str(self.rotation[0]))
        self.rotationFieldY = QLineEdit(str(self.rotation[1]))
        self.rotationFieldZ = QLineEdit(str(self.rotation[2]))
        self.rotationButton = QPushButton("Update Rotation")
        
        self.colorFieldR = QLineEdit(str(self.color[0]))
        self.colorFieldG = QLineEdit(str(self.color[1]))
        self.colorFieldB = QLineEdit(str(self.color[2]))
        self.colorButton = QPushButton("Update Color")
        
        self.scaleFieldX = QLineEdit(str(self.scale[0]))
        self.scaleFieldY = QLineEdit(str(self.scale[1]))
        self.scaleFieldZ = QLineEdit(str(self.scale[2]))
        self.scaleButton = QPushButton("Update Scale")

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
