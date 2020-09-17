from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QFrame, QApplication, QPushButton, QTextEdit, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import Qt
from editpage import Editpage
import resources
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Homepage(QMainWindow):
	def __init__(self):
		super().__init__()
		uic.loadUi(resource_path("ui_main.ui"), self)

		self.minButton = self.findChild(QPushButton, "minimize_button")
		self.closeButton = self.findChild(QPushButton, "close_button")
		self.addImageButton = self.findChild(QPushButton, "add_image_button")
		self.titleBar = self.findChild(QFrame, "title_bar")
		self.previewImage = self.findChild(QLabel, "preview_image")
		self.offset = None

		self.minButton.clicked.connect(self.showMinimized)
		self.closeButton.clicked.connect(self.close)
		self.addImageButton.clicked.connect(self.add_image)

		flags = Qt.WindowFlags(Qt.FramelessWindowHint)
		self.setWindowFlags(flags)
		self.setAttribute(Qt.WA_TranslucentBackground)

		self.moveAtCenter()
		self.show()

	def moveAtCenter(self):
		screen = QApplication.desktop().screenGeometry()
		x = (screen.width() - self.width())//2
		y = (screen.height() - self.height())//2
		self.move(x,y)		

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
		try:
			image_path, _ = QFileDialog.getOpenFileName(None, "Open image file...")
			self.editpage = Editpage(self, image_path)
			self.hide()
			self.editpage.show()
		except:
			return

	
if __name__ == "__main__":
    app = QApplication(sys.argv)
    homepage = Homepage()
    homepage.show()
    app.exec()
		

