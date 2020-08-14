from PyQt5.QtWidgets import QMainWindow, QLabel, QFileDialog, QFrame, QApplication, QPushButton, QTextEdit
from PyQt5 import uic
from PyQt5.QtCore import Qt
#from editpage import Editpage
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

	def add_image(self):
		#fileName, _ = QFileDialog.getOpenFileName(None, "Open image file...")
		#editpage = Editpage(fileName)
		pass


	
if __name__ == "__main__":
    app = QApplication(sys.argv)
    homepage = Homepage()
    homepage.show()
    app.exec()
		