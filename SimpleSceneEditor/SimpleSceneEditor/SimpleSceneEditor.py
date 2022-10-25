from ast import Delete
from gettext import translation
from lib2to3.pytree import Node
from pickle import OBJ
import sys
import random
from tkinter import CURRENT
from PySide6 import QtCore, QtWidgets, QtGui, Qt3DCore, Qt3DInput, Qt3DAnimation, Qt3DExtras, Qt3DLogic, QtQuick3D
from PySide6.QtCore import Slot
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.Qt3DCore import *
from PySide6.Qt3DExtras import *
from PySide6.Qt3DLogic import *
from PySide6.Qt3DInput import *

#https://doc.qt.io/qtforpython/ Was used as documentation
        
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

class Object3D:
    def __init__(self, objList = ObjectList(), swapActionPane = None, revertPane = None, renderWindow = None):
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

        self.objList = objList
        self.swapActionPane = swapActionPane
        self.revertPane = revertPane
        self.renderWindow = renderWindow

        self.entity = None #mesh entity
        self.mesh = None #mesh
        self.transform = None #mesh transform
        self.material = None #mesh material

    def delete(self):
        #Take list, remove object from list
        self.renderWindow.view.removeObject(self.entity)
        self.objList.deleteObject(self)
        self.objList.update()
        
    def editprompt(self):
        #create edit plane
        pass

    def updateRender(self):
        #sadly we have to delete the object and then add it again
        self.renderWindow.view.removeObject(self.entity)
        self.renderWindow.view.addObject(self)

    def updateTraslation(self):
        self.translation = [float(self.translationFieldX.text()),float(self.translationFieldY.text()),float(self.translationFieldZ.text())]
        self.updateRender()

    #Construct quaternion from inputted rotation
    def updateRotation(self):
        self.rotation = QQuaternion.fromEulerAngles(QVector3D(float(self.rotationFieldX.text()),float(self.rotationFieldY.text()),float(self.rotationFieldZ.text())))
        self.updateRender()
    
    def updateColor(self):
        self.color = [int(self.colorFieldR.text()),int(self.colorFieldG.text()),int(self.colorFieldB.text())]
        for i in range(3): #Lock into RGB range
            if self.color[i] < 0:
                self.color[i] = 0
            elif self.color[i] > 255:
                self.color[i] = 255
        self.updateRender()
        

class Cube(Object3D):
    def __init__(self, objList = ObjectList(), swapActionPane = None, revertPane = None, renderWindow = None):
        super().__init__(objList, swapActionPane, revertPane, renderWindow)
        self.scale = [1.0,1.0,1.0]
        self.indicator = 1 #1 = cube
        self.name = "cube" #will be changed in add to dict
        self.actionPane = QVBoxLayout()

        
    

        

    def updateScale(self):
        self.scale = [float(self.scaleFieldX.text()),float(self.scaleFieldY.text()),float(self.scaleFieldZ.text())]
        self.updateRender()
        
    def editprompt(self):
        #create cube edit plane

        #Create Field Items
        
        def callUpdateFunc():
            self.objList.modifyObject(self)
        
        self.translationFieldX = QLineEdit(str(self.translation[0]))
        self.translationFieldY = QLineEdit(str(self.translation[1]))
        self.translationFieldZ = QLineEdit(str(self.translation[2]))
        self.translationButton = QPushButton("Update Translation")
        self.translationButton.clicked.connect(self.updateTraslation)
        self.translationButton.clicked.connect(callUpdateFunc)
        
        quaternionEuler = self.rotation.toEulerAngles()
        self.rotationFieldX = QLineEdit(str(quaternionEuler.x()))
        self.rotationFieldY = QLineEdit(str(quaternionEuler.y()))
        self.rotationFieldZ = QLineEdit(str(quaternionEuler.z()))
        self.rotationButton = QPushButton("Update Rotation")
        self.rotationButton.clicked.connect(self.updateRotation)
        self.rotationButton.clicked.connect(callUpdateFunc)
        
        self.colorFieldR = QLineEdit(str(self.color[0]))
        self.colorFieldG = QLineEdit(str(self.color[1]))
        self.colorFieldB = QLineEdit(str(self.color[2]))
        self.colorButton = QPushButton("Update Color")
        self.colorButton.clicked.connect(self.updateColor)
        self.colorButton.clicked.connect(callUpdateFunc)
        
        self.scaleFieldX = QLineEdit(str(self.scale[0]))
        self.scaleFieldY = QLineEdit(str(self.scale[1]))
        self.scaleFieldZ = QLineEdit(str(self.scale[2]))
        self.scaleButton = QPushButton("Update Scale")
        self.scaleButton.clicked.connect(self.updateScale)
        self.scaleButton.clicked.connect(callUpdateFunc)

        #Create action pane
        self.actionPane = QVBoxLayout()
        self.actionPane.addWidget(QtWidgets.QLabel("Action: Edit " + self.name, alignment=QtCore.Qt.AlignTop))

        if self.revertPane is not None and self.swapActionPane is not None:

            returnButton = QPushButton("Return to Add")
            returnButton.clicked.connect(self.revertPane)

            #Add buttons
            horizontalGroupBoxT = QGroupBox(("Translation"))
            hlayoutT = QHBoxLayout();
            hlayoutT.addWidget(self.translationFieldX)
            hlayoutT.addWidget(self.translationFieldY)
            hlayoutT.addWidget(self.translationFieldZ)
            hlayoutT.addWidget(self.translationButton)
            horizontalGroupBoxT.setLayout(hlayoutT)
            self.actionPane.addWidget(horizontalGroupBoxT)
            
            horizontalGroupBoxR = QGroupBox(("Rotation"))
            hlayoutR = QHBoxLayout();
            hlayoutR.addWidget(self.rotationFieldX)
            hlayoutR.addWidget(self.rotationFieldY)
            hlayoutR.addWidget(self.rotationFieldZ)
            hlayoutR.addWidget(self.rotationButton)
            horizontalGroupBoxR.setLayout(hlayoutR)
            self.actionPane.addWidget(horizontalGroupBoxR)
            
            horizontalGroupBoxC = QGroupBox(("Color"))
            hlayoutC = QHBoxLayout();
            hlayoutC.addWidget(self.colorFieldR)
            hlayoutC.addWidget(self.colorFieldG)
            hlayoutC.addWidget(self.colorFieldB)
            hlayoutC.addWidget(self.colorButton)
            horizontalGroupBoxC.setLayout(hlayoutC)
            self.actionPane.addWidget(horizontalGroupBoxC)
            
            horizontalGroupBoxS = QGroupBox(("Scale"))
            hlayoutS = QHBoxLayout();
            hlayoutS.addWidget(self.scaleFieldX)
            hlayoutS.addWidget(self.scaleFieldY)
            hlayoutS.addWidget(self.scaleFieldZ)
            hlayoutS.addWidget(self.scaleButton)
            horizontalGroupBoxS.setLayout(hlayoutS)
            self.actionPane.addWidget(horizontalGroupBoxS)


            self.actionPane.addWidget(returnButton)

            #Set pane
            self.swapActionPane(self.actionPane)


class Sphere(Object3D):
    
    def __init__(self, objList = ObjectList(), swapActionPane = None, revertPane = None, renderWindow = None):
        super().__init__(objList, swapActionPane, revertPane, renderWindow)
        self.radius = 1.0
        self.indicator = 2 #2 = sphere
        self.name = "sphere" #will be changed in add to dict

    def updateRender(self):
        self.mesh.setRadius(self.radius)
        self.transform = Qt3DCore.QTransform()
        self.transform.setRotation(self.rotation)
        self.transform.setTranslation(QVector3D(self.translation[0],self.translation[1],self.translation[2]))
            
        # Material
        self.material = Qt3DExtras.QPhongMaterial()
        self.material.setAmbient(QColor(self.color[0], self.color[1], self.color[2]))
        self.material.setDiffuse(0)
        self.material.setShininess(1)
        self.material.setSpecular(0)



    def updateRadius(self):
        self.radius = float(self.radiusField.text())
        if self.radius <= 0.0:
            self.radius = 0.000000001
        self.updateRender()
           


    #Shares a lot of code with cube, could be generalized
    def editprompt(self):
        #create sphere edit plane

        #Create Field Items
        
        def callUpdateFunc():
            self.objList.modifyObject(self)
        
        self.translationFieldX = QLineEdit(str(self.translation[0]))
        self.translationFieldY = QLineEdit(str(self.translation[1]))
        self.translationFieldZ = QLineEdit(str(self.translation[2]))
        self.translationButton = QPushButton("Update Translation")
        self.translationButton.clicked.connect(self.updateTraslation)
        self.translationButton.clicked.connect(callUpdateFunc)
        
        quaternionEuler = self.rotation.toEulerAngles()
        self.rotationFieldX = QLineEdit(str(quaternionEuler.x()))
        self.rotationFieldY = QLineEdit(str(quaternionEuler.y()))
        self.rotationFieldZ = QLineEdit(str(quaternionEuler.z()))
        self.rotationButton = QPushButton("Update Rotation")
        self.rotationButton.clicked.connect(self.updateRotation)
        self.rotationButton.clicked.connect(callUpdateFunc)
        
        self.colorFieldR = QLineEdit(str(self.color[0]))
        self.colorFieldG = QLineEdit(str(self.color[1]))
        self.colorFieldB = QLineEdit(str(self.color[2]))
        self.colorButton = QPushButton("Update Color")
        self.colorButton.clicked.connect(self.updateColor)
        self.colorButton.clicked.connect(callUpdateFunc)
        
        self.radiusField = QLineEdit(str(self.radius))
        self.radiusButton = QPushButton("Update Radius")
        self.radiusButton.clicked.connect(self.updateRadius)
        self.radiusButton.clicked.connect(callUpdateFunc)

        #Create action pane
        self.actionPane = QVBoxLayout()
        self.actionPane.addWidget(QtWidgets.QLabel("Action: Edit " + self.name, alignment=QtCore.Qt.AlignTop))

        if self.revertPane is not None and self.swapActionPane is not None:

            returnButton = QPushButton("Return to Add")
            returnButton.clicked.connect(self.revertPane)

            #Add buttons
            horizontalGroupBoxT = QGroupBox(("Translation"))
            hlayoutT = QHBoxLayout();
            hlayoutT.addWidget(self.translationFieldX)
            hlayoutT.addWidget(self.translationFieldY)
            hlayoutT.addWidget(self.translationFieldZ)
            hlayoutT.addWidget(self.translationButton)
            horizontalGroupBoxT.setLayout(hlayoutT)
            self.actionPane.addWidget(horizontalGroupBoxT)
            
            horizontalGroupBoxR = QGroupBox(("Rotation"))
            hlayoutR = QHBoxLayout();
            hlayoutR.addWidget(self.rotationFieldX)
            hlayoutR.addWidget(self.rotationFieldY)
            hlayoutR.addWidget(self.rotationFieldZ)
            hlayoutR.addWidget(self.rotationButton)
            horizontalGroupBoxR.setLayout(hlayoutR)
            self.actionPane.addWidget(horizontalGroupBoxR)
            
            horizontalGroupBoxC = QGroupBox(("Color"))
            hlayoutC = QHBoxLayout();
            hlayoutC.addWidget(self.colorFieldR)
            hlayoutC.addWidget(self.colorFieldG)
            hlayoutC.addWidget(self.colorFieldB)
            hlayoutC.addWidget(self.colorButton)
            horizontalGroupBoxC.setLayout(hlayoutC)
            self.actionPane.addWidget(horizontalGroupBoxC)
            
            horizontalGroupBoxR = QGroupBox(("Radius"))
            hlayoutR = QHBoxLayout();
            hlayoutR.addWidget(self.radiusField)
            hlayoutR.addWidget(self.radiusButton)
            horizontalGroupBoxR.setLayout(hlayoutR)
            self.actionPane.addWidget(horizontalGroupBoxR)


            self.actionPane.addWidget(returnButton)

            #Set pane
            self.swapActionPane(self.actionPane)

    

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
            objDelete.clicked.connect(obj.delete)
            objEdit = QPushButton("Edit")
            objEdit.clicked.connect(obj.editprompt)
            #Create obj delete button
            #Create obj edit button
            self.table.setItem(objCounter, 0, QTableWidgetItem(objName))
            self.table.setItem(objCounter, 1, QTableWidgetItem())
            self.table.setIndexWidget(self.table.model().index(objCounter, 1), objDelete)
            self.table.setItem(objCounter, 2, QTableWidgetItem())
            self.table.setIndexWidget(self.table.model().index(objCounter, 2), objEdit)
            objCounter += 1
        self.addWidget(self.table)

class ActionPaneAdd(QVBoxLayout):

    def __init__(self,objList = ObjectList(), text = None, swapActionPane = None, revertPane = None, renderPane = None):
        super().__init__()
        if text is not None:
            self.addWidget(text)
        self.objList = objList
        self.addCubeButton = QPushButton("Cube")
        self.addSphereButton = QPushButton("Sphere")
        self.addCubeButton.clicked.connect(self.addCubeCall)
        self.addSphereButton.clicked.connect(self.addSphereCall)
        self.addWidget(self.addCubeButton)
        self.addWidget(self.addSphereButton)
        self.swapActionPane = swapActionPane
        self.revertPane = revertPane
        self.renderPane = renderPane
    
    def addCubeCall(self):
        cube = Cube(self.objList, self.swapActionPane, self.revertPane, self.renderPane)
        self.objList.addObject(cube)
        self.objList.update()
        self.renderPane.view.addObject(cube)
        

    def addSphereCall(self):
        sphere = Sphere(self.objList, self.swapActionPane, self.revertPane, self.renderPane)
        self.objList.addObject(sphere)
        self.objList.update()
        self.renderPane.view.addObject(sphere)

#Based on https://doc.qt.io/qtforpython/examples/example_3d__simple3d.html
class RenderWindow(Qt3DExtras.Qt3DWindow):
    def __init__(self):
        super().__init__()
        # Root entity
        self.rootEntity = Qt3DCore.QEntity()

        # Camera
        self.camera().lens().setPerspectiveProjection(45, 16 / 9, 0.1, 1000)
        self.camera().setPosition(QVector3D(0, 0, 40))
        self.camera().setViewCenter(QVector3D(0, 0, 0))

        # For camera controls

        self.camController = Qt3DExtras.QOrbitCameraController(self.rootEntity)
        self.camController.setLinearSpeed(50)
        self.camController.setLookSpeed(180)
        self.camController.setCamera(self.camera())

        self.setRootEntity(self.rootEntity)

    def addObjectCube(self, object: Cube):
        #mesh, transform
        object.mesh = Qt3DExtras.QCuboidMesh()
        object.transform = Qt3DCore.QTransform()
        object.transform.setScale3D(QVector3D(object.scale[0],object.scale[1],object.scale[2]))
        object.transform.setRotation(object.rotation)
        object.transform.setTranslation(QVector3D(object.translation[0],object.translation[1],object.translation[2]))
            
        # Material
        object.material = Qt3DExtras.QPhongMaterial()
        object.material.setAmbient(QColor(object.color[0], object.color[1], object.color[2]))

        #Linking
        object.entity.addComponent(object.mesh)
        object.entity.addComponent(object.transform)
        object.entity.addComponent(object.material)

    def addObjectSphere(self, object: Sphere):
        #Mesh, radius, and transform
        object.mesh = Qt3DExtras.QSphereMesh()
        object.mesh.setRadius(object.radius)
        object.transform = Qt3DCore.QTransform()
        object.transform.setRotation(object.rotation)
        object.transform.setTranslation(QVector3D(object.translation[0],object.translation[1],object.translation[2]))
            
        # Material
        object.material = Qt3DExtras.QPhongMaterial()
        object.material.setAmbient(QColor(object.color[0], object.color[1], object.color[2]))

        #Linking
        object.entity.addComponent(object.mesh)
        object.entity.addComponent(object.transform)
        object.entity.addComponent(object.material)

    def addObject(self, object):
        object.entity = Qt3DCore.QEntity(self.rootEntity)
        if object.indicator == 0:
            pass
        elif object.indicator == 1: #cube
            self.addObjectCube(object)
        else:
            self.addObjectSphere(object)


    def removeRecursive(self, objectID, currentNode : Qt3DCore.QNode):
        if currentNode is not None:
            if currentNode.id() == objectID:
                currentNode.deleteLater()
                pass
            for node in currentNode.childNodes():
                self.removeRecursive(objectID, node)

    def removeObject(self, object : Qt3DCore.QEntity):
        self.removeRecursive(object.id(),self.rootEntity)

     


#Layout which contains a widget acting as a container
#for a Qt3DWindow, the render view
class RenderPane (QVBoxLayout):
    def __init__(self,objList = ObjectList()):
        super().__init__()
        self.view = RenderWindow()
        self.container = QWidget.createWindowContainer(self.view)
        self.addWidget(self.container)

        



class MainWindow (QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.listPane = ListPane()
        self.objList = ObjectList(self.listPane)
        self.renderPane = RenderPane(self.objList)
        addBackupText = QtWidgets.QLabel("Action: Add Object", alignment=QtCore.Qt.AlignTop)

        #self.layout = QtWidgets.QVBoxLayout(self)

        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(layout)

        self.toplayout = ActionPaneAdd(self.objList, addBackupText, self.swapActionPane, self.revertPane, self.renderPane) #return to this to return to add pane
        self.midlayout = self.listPane
        self.bottomlayout = self.renderPane
        self.centralWidget.layout().addLayout(self.toplayout,25)
        self.centralWidget.layout().addLayout(self.midlayout,25)
        self.centralWidget.layout().addLayout(self.bottomlayout,50)


    def swapActionPane(self, newPane):
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(layout)
        self.toplayout.setParent(None)
        self.toplayout = newPane
        self.midlayout.setParent(None)
        self.bottomlayout.setParent(None)
        self.centralWidget.layout().addLayout(self.toplayout,25)
        self.centralWidget.layout().addLayout(self.midlayout,25)
        self.centralWidget.layout().addLayout(self.bottomlayout,50)

    def revertPane(self):
        addBackupText = QtWidgets.QLabel("Action: Add Object", alignment=QtCore.Qt.AlignTop)
        self.centralWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralWidget)
        layout = QtWidgets.QVBoxLayout()
        self.centralWidget.setLayout(layout)

        self.toplayout.setParent(None)
        self.toplayout = ActionPaneAdd(self.objList, addBackupText, self.swapActionPane, self.revertPane) 
        self.midlayout.setParent(None)
        self.bottomlayout.setParent(None)
        self.centralWidget.layout().addLayout(self.toplayout,25)
        self.centralWidget.layout().addLayout(self.midlayout,25)
        self.centralWidget.layout().addLayout(self.bottomlayout,50)
        

    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(1200,900)
    widget.show()

    sys.exit(app.exec())
