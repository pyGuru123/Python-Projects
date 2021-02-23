import tkinter
from PIL import Image, ImageTk

class ImageProcessor:
	def __init__(self, path):
		self.path = path
		self.img = Image.open(self.path)
		self.size = width, height = self.img.width, self.img.height

	def display_image(self):
		return ImageTk.PhotoImage(self.img), self.size

	def zoom(self, factor):
		if factor > 1:
			basewidth = int(self.size[0] * (factor / 100))
			wpercent = (basewidth/float(self.img.size[0]))
			hsize = int((float(self.img.size[1])*float(wpercent)))
			img = self.img.resize((basewidth,hsize), Image.ANTIALIAS)
			return ImageTk.PhotoImage(img)
