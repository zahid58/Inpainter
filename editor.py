from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QGraphicsView, QGraphicsScene, QSlider, QFileDialog, QShortcut
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPen, QPainter, QActionEvent, QKeySequence
import numpy as np
import backend
from qimage2ndarray import rgb_view, array2qimage
import cv2

class Editor(QtWidgets.QGraphicsView):

    def __init__(self, scene = None, parent = None, slider = None):
        super(Editor, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        if scene is not None:
            self._scene = scene
        else:
            self._scene = QtWidgets.QGraphicsScene(self)
        
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.drawMode = True
        self.drawing = False
        self.brushColor = "red"
        self.brushSlider = slider
        self.lastPoint = QPoint()
        self.color_index = {"red":0, "green":1, "blue":2}

        self._method = "Telea"
        self._mask = None
        self._current_image = None
        self._unmarkedImage = None
        self.set_mask = False

        self.inpaintSc = QShortcut(QKeySequence('Ctrl+I'), self)
        self.inpaintSc.activated.connect(self.inpaint)
        self.saveSc = QShortcut(QKeySequence('Ctrl+S'), self)
        self.saveSc.activated.connect(self.save)
        self.resetSc = QShortcut(QKeySequence('Ctrl+Z'), self)
        self.resetSc.activated.connect(self.reset)        

    def setInpaintingMethod(self, method):
        self._method = method

    def hasPhoto(self):
        return not self._empty

    def fit(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0


    def setMask(self):
        self._mask = QImage(self._photo.pixmap().size(), QImage.Format_RGB32)
        self._mask.fill(Qt.black)

    def setPhoto(self, pixmap=None):
        if pixmap.height() > 720 or pixmap.width() > 1280:
            pixmap = pixmap.scaled(1280, 720, Qt.KeepAspectRatio)
        self._zoom = 0
        self._unmarkedImage = QPixmap(pixmap)
        self._current_image = rgb_view(pixmap.toImage())
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())  
        self.setMask()


    def wheelEvent(self, event):

        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fit()
            else:
                self._zoom = 0
        super(Editor, self).wheelEvent(event)            
    
    
    def mouseMoveEvent(self, event):

        if(event.buttons() and Qt.LeftButton) and self.drawing:
            if self.set_mask:
                self.setMask()
                self.set_mask = False
            painter = QPainter (self._mask)
            if not painter.isActive():
                painter.begin(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            if self.drawMode:
                painter.setPen(QPen(Qt.white, self.brushSlider.value(), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            else:
                painter.setPen(QPen(Qt.black, self.brushSlider.value(), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, self.mapToScene(event.pos()))
            painter.end()
            self.lastPoint = self.mapToScene(event.pos())
            img = np.array(self._current_image, dtype = np.float32)
            mask = rgb_view(self._mask)
            channel = self.color_index[self.brushColor]
            ind = np.all(mask != [0,0,0], axis=-1)
            color = np.array([50,50,50], dtype = np.float32)
            color[channel] = 250
            img[ind] = img[ind]*0.45 + color*0.55
            self._photo.setPixmap(QPixmap(array2qimage(img))) #

        super(Editor, self).mouseMoveEvent(event)        


    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:            
            self.drawing = True
            self.lastPoint = self.mapToScene(event.pos())


    def mouseReleaseEvent(self, event):

        if self.drawMode:
            if event.button() == Qt.LeftButton:
                self.drawing = False
        super(Editor, self).mouseReleaseEvent(event)    


    def inpaint(self):

        img = np.array(self._current_image)              
        mask = rgb_view(self._mask)

        if self._method == "Navier-Stokes":
            output_rgb = backend.inpaint_cv2(img, mask,method="ns")

        elif self._method == "Telea":
            output_rgb = backend.inpaint_cv2(img, mask,method="telea") 

        elif self._method == "Deepfill":                        
            output_rgb = backend.inpaint_deepfill(img, mask)        
        
        # add calls to your inpainting methods here
        
        else:
            raise Exception("this inpainting method is not recognized!")

        output = array2qimage(output_rgb)
        self.set_mask = True
        self.setMask()
        self._current_image = output_rgb
        self._photo.setPixmap(QPixmap(output))


    def save(self):
        try:
            image_path, _ = QFileDialog.getSaveFileName() 
            img = self._photo.pixmap().toImage()
            if not image_path.endswith(".png"):
                image_path += ".png"
            img.save(image_path, "PNG")
        except:
            pass

    def reset(self):
        self._photo.setPixmap(self._unmarkedImage) 
        self.set_mask = True
        self.setMask()
        self._current_image = rgb_view(self._unmarkedImage.toImage())      


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = Editor(self)

        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)

        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        HBlayout = QtWidgets.QHBoxLayout()
        HBlayout.setAlignment(QtCore.Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        VBlayout.addLayout(HBlayout)

    def loadImage(self):
        fileName, dummy = QFileDialog.getOpenFileName(self, "Open image file.")
        self.viewer.setPhoto(QPixmap(fileName))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())


