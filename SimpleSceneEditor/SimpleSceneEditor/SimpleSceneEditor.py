from gettext import translation
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
        #Rotation defined once I figure out how to implement quaternions
        self.indicator = 0 #0 = not any object
        
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

    def delete(self, list):
        #Take list, remove object from list
        list.deleteObject(self)
        list.update()
        
    def editprompt(self,list):
        #create edit plane
        pass

    def updateTraslation(self):
        self.translation = [float(self.translationFieldX.text()),float(self.translationFieldY.text()),float(self.translationFieldZ.text())]

    def updateRotation(self):
        self.rotation = [float(self.rotationFieldX.text()),float(self.rotationFieldY.text()),float(self.rotationFieldZ.text())]
    
    def updateColor(self):
        self.color = [int(self.colorFieldR.text()),int(self.colorFieldG.text()),int(self.colorFieldB.text())]

class Cube(Object3D):
    def __init__(self):
        super().__init__()
        self.scale = [1.0,1.0,1.0]
        self.indicator = 1 #1 = cube
        self.name = "cube" #will be changed in add to dict

    def updateScale(self):
        self.scale = [float(self.scaleFieldX.text()),float(self.scaleFieldY.text()),float(self.scaleFieldZ.text())]
        
    def editprompt(self,list):
        #create cube edit plane

        #Create Field Items

        updateLambda = lambda:list.modifyObject(self)
        def callUpdateLambda():
            updateLambda()
        
        self.translationFieldX = QLineEdit(str(self.translation[0]))
        self.translationFieldY = QLineEdit(str(self.translation[1]))
        self.translationFieldZ = QLineEdit(str(self.translation[2]))
        self.translationButton = QPushButton("Update Translation")
        self.translationButton.clicked.connect(self.updateTraslation)
        self.translationButton.clicked.connect(callUpdateLambda)
        
        self.rotationFieldX = QLineEdit(str(self.rotation[0]))
        self.rotationFieldY = QLineEdit(str(self.rotation[1]))
        self.rotationFieldZ = QLineEdit(str(self.rotation[2]))
        self.rotationButton = QPushButton("Update Rotation")
        self.rotationButton.clicked.connect(self.updateRotation)
        self.rotationButton.clicked.connect(callUpdateLambda)
        
        self.colorFieldR = QLineEdit(str(self.color[0]))
        self.colorFieldG = QLineEdit(str(self.color[1]))
        self.colorFieldB = QLineEdit(str(self.color[2]))
        self.colorButton = QPushButton("Update Color")
        self.colorButton.clicked.connect(self.updateColor)
        self.colorButton.clicked.connect(callUpdateLambda)
        
        self.scaleFieldX = QLineEdit(str(self.scale[0]))
        self.scaleFieldY = QLineEdit(str(self.scale[1]))
        self.scaleFieldZ = QLineEdit(str(self.scale[2]))
        self.scaleButton = QPushButton("Update Scale")
        self.scaleButton.clicked.connect(self.updateScale)
        self.scaleButton.clicked.connect(callUpdateLambda)


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
    
class ActionPaneAdd(QVBoxLayout):
    
    def addCubeCall(self):
        cube = Cube()
        self.objList.addObject(cube)
        self.objList.update()

    def addSphereCall(self):
        sphere = Sphere()
        self.objList.addObject(sphere)
        self.objList.update()

    def __init__(self,objList = ObjectList()):
        self.objList = objList
        self.addCubeButton = QPushButton("Cube")
        self.addSphereButton = QPushButton("Sphere")
        self.addCubeButton.clicked.connnect(self.addCubeCall)
        self.addSphereButton.clicked.connnect(self.addSphereButton)
        self.addWidget(self.addCubeButton)
        self.addWidget(self.addSphereButton)
        self.setContentsMargins(1,1,1,1) 

class MainWindow (QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.addBackup = ActionPaneAdd(self, list) #return to this to return to add pane
        self.actionPane = self.addBackup #default action is adding objects
        self.listPane = ListPane(self)

        self.list = ObjectList()

        self.layout = QtWidgets.QVBoxLayout(self)
        llayout = self.actionPane
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1,1,1,1)
        rlayout.addWidget(self.listPane)
        self.layout.addLayout(llayout,50)
        self.layout.addLayout(rlayout,50)
        

    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())
