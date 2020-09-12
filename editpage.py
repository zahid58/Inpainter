from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QMainWindow, QSlider, QLabel, QGridLayout, QGraphicsScene, QFileDialog, QFrame, QApplication, QPushButton, QTextEdit, QMessageBox, QGraphicsView
from PyQt5 import uic
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QImage, QPainterPath, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QPoint
import sys
import resources
from editor import Editor

class Editpage(QMainWindow):
	def __init__(self, homepage, image_path):
		super().__init__()
		self.homepage = homepage
		self.image_path = image_path
		self.setupUi()
		
	def setupUi(self):	

		uic.loadUi("ui_edit.ui", self)
		self.penButton = self.findChild(QPushButton, "pen_button")
		self.eraserButton = self.findChild(QPushButton, "eraser_button")
		self.backButton = self.findChild(QPushButton, "back_button")
		self.nextButton = self.findChild(QPushButton, "next_button")
		self.minButton = self.findChild(QPushButton, "min_button")
		self.maxButton = self.findChild(QPushButton, "max_button")
		self.greenMarker = self.findChild(QPushButton, "green_marker")
		self.redMarker = self.findChild(QPushButton, "red_marker")
		self.blueMarker = self.findChild(QPushButton, "blue_marker")
		self.markerWidthSlider = self.findChild(QSlider, "marker_width_slider")
		self.titleBar = self.findChild(QFrame, "title_bar")
		self.infoLabel = self.findChild(QLabel, "info_label")
		self.mainFrame = self.findChild(QFrame, "main_frame")
		self.viewFrame = self.findChild(QFrame, "view_frame")
		
		self.penButton.setProperty('selected',True)
		self.penButton.setStyle(self.penButton.style())
		self.eraserButton.setProperty('selected',False)
		self.eraserButton.setStyle(self.penButton.style())

		self.penButton.clicked.connect(self.penSelect)
		self.eraserButton.clicked.connect(self.eraserSelect)
		self.backButton.clicked.connect(self.goBack)
		self.minButton.clicked.connect(self.showMinimized)
		self.maxButton.clicked.connect(self.showMaximized)
		self.nextButton.clicked.connect(self.processImage)

		self.redMarker.setProperty('selected',True)
		self.redMarker.setStyle(self.redMarker.style())
		self.greenMarker.setProperty('selected',False)
		self.greenMarker.setStyle(self.greenMarker.style())
		self.blueMarker.setProperty('selected',False)
		self.blueMarker.setStyle(self.blueMarker.style())

		self.redMarker.clicked.connect(self.redSelect)
		self.blueMarker.clicked.connect(self.blueSelect)
		self.greenMarker.clicked.connect(self.greenSelect)

		flags = Qt.WindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
		self.setWindowFlags(flags)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.scene = QGraphicsScene()
		#print(type(self.markerWidthSlider))
		self.imageView = Editor(self.scene, self.viewFrame, slider = self.markerWidthSlider)
		
		self.imageView.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding))
		# print(self.viewFrame.width(), self.viewFrame.height())
		self.imageView.setGeometry(0,0,self.viewFrame.width(),self.viewFrame.height())
		self.imageView.viewport().setFixedSize(self.viewFrame.width(),self.viewFrame.height())
		
		
		self.imageView.setPhoto(QPixmap(self.image_path))

		# the layout makes sure imageview expands with the frame
		vbox = QVBoxLayout()
		vbox.addWidget(self.imageView)
		self.viewFrame.setLayout(vbox)


	def redSelect(self):
		self.redMarker.setProperty('selected',True)
		self.redMarker.setStyle(self.redMarker.style())
		self.greenMarker.setProperty('selected',False)
		self.greenMarker.setStyle(self.greenMarker.style())
		self.blueMarker.setProperty('selected',False)
		self.blueMarker.setStyle(self.blueMarker.style())
		self.imageView.brushColor = "red"	

	def greenSelect(self):
		self.redMarker.setProperty('selected',False)
		self.redMarker.setStyle(self.redMarker.style())
		self.greenMarker.setProperty('selected',True)
		self.greenMarker.setStyle(self.greenMarker.style())
		self.blueMarker.setProperty('selected',False)
		self.blueMarker.setStyle(self.blueMarker.style())
		self.imageView.brushColor = "green"	

	def blueSelect(self):
		self.redMarker.setProperty('selected',False)
		self.redMarker.setStyle(self.redMarker.style())
		self.greenMarker.setProperty('selected',False)
		self.greenMarker.setStyle(self.greenMarker.style())
		self.blueMarker.setProperty('selected',True)
		self.blueMarker.setStyle(self.blueMarker.style())
		self.imageView.brushColor = "blue"	

	def penSelect(self):
		self.penButton.setProperty('selected',True)
		self.penButton.setStyle(self.penButton.style())
		self.eraserButton.setProperty('selected',False)
		self.eraserButton.setStyle(self.penButton.style())
		self.imageView.drawing = False
		self.imageView.drawMode = True


	def eraserSelect(self):
		self.penButton.setProperty('selected',False)
		self.penButton.setStyle(self.penButton.style())
		self.eraserButton.setProperty('selected',True)
		self.eraserButton.setStyle(self.penButton.style())
		self.imageView.drawing = False
		self.imageView.drawMode = False


	def goBack(self):
		self.homepage.show()
		self.hide()
		

	def processImage(self):
		self.imageView.inpaint()



	
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editpage = Editpage()
    editpage.show()
    app.exec()
		



'''
		isTest = widget.property(‘Test’)

		buttonReply = QMessageBox.question(self, 'test message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			print("Yes")
		else:
			print("No")			
			
		#fileName, _ = QFileDialog.getOpenFileName(None, "Open image file...")
		#editpage = Editpage(fileName)

'''