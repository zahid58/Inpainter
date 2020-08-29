from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSizePolicy, QGraphicsView, QGraphicsScene, QFileDialog
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR, QPoint
from PyQt5.QtGui import QImage, QPixmap, QPainterPath, QPen, QPainter

class Editor(QtWidgets.QGraphicsView):

    def __init__(self, scene = None, parent = None):
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
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)) 
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.drawMode = True
        self.drawing = False
        self.brushSize = 4
        self.brushColor = Qt.red
        self.lastPoint = QPoint()

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        print(rect.getCoords())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                print(rect.getCoords())
                scenerect = self.transform().mapRect(rect)
                print(rect.getCoords())
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                print(factor)
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap()) 
        self.setSceneRect(QRectF(self._photo.pixmap.rect()))  
        self.fitInView()

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
                self.fitInView()
            else:
                self._zoom = 0
        print(self._zoom)
        super(Editor, self).wheelEvent(event)            
    
    def mouseMoveEvent(self, event):
        if self.drawMode:
            if(event.buttons() and Qt.LeftButton) and self.drawing:
                pixmap = self._photo.pixmap()    
                painter = QPainter(pixmap)
                if not painter.isActive():
                    painter.begin(self)
                painter.setRenderHint(QPainter.Antialiasing, True)
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.lastPoint, self.mapToScene(event.pos()))
                painter.end()
                self.lastPoint = self.mapToScene(event.pos())
                self._photo.setPixmap(pixmap)

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



class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = Editor(self)
        # 'Load image' button
        self.btnLoad = QtWidgets.QToolButton(self)
        self.btnLoad.setText('Load image')
        self.btnLoad.clicked.connect(self.loadImage)
        # Arrange layout
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
