from gettext import translation
from pickle import OBJ
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot
from PySide6.QtWidgets import *
from PySide6.QtGui import *



class Object3D:
    def __init__(self):
        self.name = ""
        self.color = [122,122,122] #All objects default to gray
        self.translation = [0.0,0.0,0.0]
        self.rotation = QQuaternion()
        self.indicator = 0 #0 = not any object
        
        self.translationFieldX = QLineEdit(str(self.translation[0]))
        self.translationFieldY = QLineEdit(str(self.translation[1]))
        self.translationFieldZ = QLineEdit(str(self.translation[2]))
        self.translationButton = QPushButton("Update Translation")
        
        quaternionEuler = self.rotation.toEulerAngles()
        self.rotationFieldX = QLineEdit(str(quaternionEuler.x()))
        self.rotationFieldY = QLineEdit(str(quaternionEuler.y()))
        self.rotationFieldZ = QLineEdit(str(quaternionEuler.z()))
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

    #Construct quaternion from inputted rotation
    def updateRotation(self):
        self.rotation = QQuaternion.fromEulerAngles(QVector3D(float(self.rotationFieldX.text()),float(self.rotationFieldY.text()),float(self.rotationFieldZ.text())))
        
    
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


    

class ListPane(QVBoxLayout):

    def __init__(self):
        super().__init__()
        self.text = QtWidgets.QLabel("List", alignment=QtCore.Qt.AlignTop)
        self.addWidget(self.text)
        self.table = QTableWidget()
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Delete", "Edit"])

    def updateListPane(self, updatedListDic = {}):
        self.removeWidget(self.table)
        self.table.deleteLater()
        self.table = QTableWidget()
        self.table.setRowCount(len(updatedListDic))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Delete", "Edit"])
        objCounter = 0
        for objKey in updatedListDic:
            obj = updatedListDic[objKey]
            objName = obj.name
            objDelete = QPushButton("Delete")
            objEdit = QPushButton("Edit")
            #Create obj delete button
            #Create obj edit button
            self.table.setItem(objCounter, 0, QTableWidgetItem(objName))
            self.table.setItem(objCounter, 1, QTableWidgetItem())
            self.table.setIndexWidget(self.table.model().index(objCounter, 1), objDelete)
            self.table.setItem(objCounter, 2, QTableWidgetItem())
            self.table.setIndexWidget(self.table.model().index(objCounter, 2), objEdit)
            objCounter += 1
        self.addWidget(self.table)
        
class ObjectList():

    def __init__(self, listPane = None):
        self.objectDict = {}
        self.cubeNum = 0
        self.sphereNum = 0
        self.listPane = listPane
    
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
            self.objectDict[object.name] = object

    def deleteObject(self, object):
        if object.indicator == 0:
            pass
        del self.objectDict[object.name]


    def modifyObject(self, object):
        if object.indicator == 0:
            pass
        self.objectDict[object.name]

    def update(self):
        if(self.listPane is not None):
            self.listPane.updateListPane(self.objectDict)

class ActionPaneAdd(QVBoxLayout):

    def __init__(self,objList = ObjectList()):
        super().__init__()
        self.objList = objList
        self.addCubeButton = QPushButton("Cube")
        self.addSphereButton = QPushButton("Sphere")
        self.addCubeButton.clicked.connect(self.addCubeCall)
        self.addSphereButton.clicked.connect(self.addSphereCall)
        self.addWidget(self.addCubeButton)
        self.addWidget(self.addSphereButton)
        self.setContentsMargins(1,1,1,1) 
    
    def addCubeCall(self):
        cube = Cube()
        self.objList.addObject(cube)
        self.objList.update()

    def addSphereCall(self):
        sphere = Sphere()
        self.objList.addObject(sphere)
        self.objList.update()

class MainWindow (QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.listPane = ListPane()
        self.objList = ObjectList(self.listPane)
        self.addBackup = ActionPaneAdd(self.objList) #return to this to return to add pane
        self.actionPane = self.addBackup #default action is adding objects


        self.layout = QtWidgets.QVBoxLayout(self)
        llayout = self.actionPane
        rlayout = self.listPane
        self.layout.addLayout(llayout,50)
        self.layout.addLayout(rlayout,50)
        

    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())
