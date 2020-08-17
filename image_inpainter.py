from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QFrame, QApplication, QPushButton, QTextEdit, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from editpage import Editpage
import sys
import resources

class Homepage(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi("ui_main.ui", self)

		self.minButton = self.findChild(QPushButton, "minimize_button")
		self.closeButton = self.findChild(QPushButton, "close_button")
		self.addImageButton = self.findChild(QPushButton, "add_image_button")
		self.titleBar = self.findChild(QFrame, "title_bar")
		self.previewImage = self.findChild(QLabel, "preview_image")

		self.minButton.clicked.connect(self.showMinimized)
		self.closeButton.clicked.connect(self.close)
		self.addImageButton.clicked.connect(self.add_image)

		flags = Qt.WindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
		self.setWindowFlags(flags)
		self.setAttribute(Qt.WA_TranslucentBackground)
		self.show()

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.offset = event.pos()
		else:
			super().mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if self.offset is not None and event.buttons() == Qt.LeftButton:
			self.move(self.pos() + event.pos() - self.offset)
		else:
			super().mouseMoveEvent(event)

	def mouseReleaseEvent(self, event):
		self.offset = None
		super().mouseReleaseEvent(event)	


	def add_image(self):
		image_path, _ = QFileDialog.getOpenFileName(None, "Open image file...")
		print(image_path)
		self.editpage = Editpage(self, image_path)
		self.hide()
		self.editpage.show()
		#self.editpage.showFullScreen()
		#self.editpage.showMaximized()
		

	
if __name__ == "__main__":
    app = QApplication(sys.argv)
    homepage = Homepage()
    homepage.show()
    app.exec()
		



'''
	def _mousePressEvent(self, event):
		self.offset = event.pos()

	def _mouseMoveEvent(self, event):
		x = event.globalX()
		y = event.globalY()
		x_w = self.offset.x()
		y_w = self.offset.y()
		self.move(x - x_w, y - y_w)


		buttonReply = QMessageBox.question(self, 'test message', "Do you like PyQt5?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
		if buttonReply == QMessageBox.Yes:
			print("Yes")
		else:
			print("No")			
		#fileName, _ = QFileDialog.getOpenFileName(None, "Open image file...")
		#editpage = Editpage(fileName)

'''