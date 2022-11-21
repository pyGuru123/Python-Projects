import os
import fitz
import datetime
from tkinter import PhotoImage

# Miner -------------------------------------------------------------

def pdf_is_encrypted(file):
	pdf = fitz.Document(file)
	return pdf.isEncrypted

class Miner:
	def __init__(self, filepath, password=None):
		self.filepath = filepath
		self.filename = os.path.basename(self.filepath)
		self.pdf = fitz.open(filepath)
		if password is not None:
			self.pdf.authenticate(password)

	def read_pdf(self):
		metadata = self.pdf.metadata
		numPages = self.pdf.page_count
		toc = self.pdf.get_toc()
		
		page = self.pdf.load_page(0)
		pagesize = page.mediabox_size

		return metadata, numPages, toc, tuple(pagesize)

	def get_page(self, page_num, zoom=None):
		page = self.pdf.load_page(page_num)
		if zoom:
			mat = fitz.Matrix(zoom, zoom)
			pix = page.get_pixmap(matrix=mat)
		else:
			pix = page.get_pixmap()
		px1 = fitz.Pixmap(pix, 0) if pix.alpha else pix
		imgdata = px1.tobytes('ppm')
		return PhotoImage(data=imgdata)

	def get_text(self, page_num, format_):
		page = self.pdf.loadPage(page_num)
		text = page.getText(format_)
		return text 

	def get_image(self, page_num):
		page = self.pdf.loadPage(page_num)
		pix = page.getPixmap()
		pix.writeImage(f'{self.filename}-Page-{page_num}.png')

	def extract_pdf_page(self, page_num, outfile):
		pdf2 = fitz.open()
		pdf2.insertPDF(self.pdf, from_page=page_num, to_page=page_num)
		pdf2.save(outfile)

		return 'done'

	def rotate_pdf_page(self, from_, to_, outfile, angle):
		pdf2 = fitz.open()
		pdf2.insertPDF(self.pdf, from_page=from_, to_page=to_, rotate=angle)
		pdf2.save(outfile)

		return 'done'

	def extract_page_images(self, page_num):
		if not os.path.exists('images/'):
			os.mkdir('images/')

		filename = os.path.basename(self.filepath)
		for image in self.pdf.getPageImageList(page_num):
			xref = image[0]
			pix = fitz.Pixmap(self.pdf, xref)
			if pix.n < 5:
				pix.writePNG(f"images/{filename}-page{page_num}-{xref}.png")
			else:
				pix1 = fitz.Pixmap(fitz.csRGB, pix)
				pix1.writePNG(f"images/{filename}-page{page_num}-{xref}.png")
				pix1 = None
			pix = None
		return len(self.pdf.getPageImageList(page_num))

	def encrypt_pdf_file(self, password, outfile):
		perm = int(
				    fitz.PDF_PERM_ACCESSIBILITY  # always use this
				    | fitz.PDF_PERM_PRINT  # permit printing
				    | fitz.PDF_PERM_COPY  # permit copying
				    | fitz.PDF_PERM_ANNOTATE  # permit annotations
				)
		encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm
		self.pdf.save(outfile, encryption=encrypt_meth, user_pw=password,
						 permissions=perm)
		return 'done'

	def decrypt_pdf_file(self, outfile):
		self.pdf.save(outfile)
		return 'done'

	def split_pdf_file(self, from_, to_, outfile):
		pdf2 = fitz.open()
		pdf2.insertPDF(self.pdf, from_page=from_, to_page=to_)
		pdf2.save(outfile)

		return 'done'

	def merge_pdf_file(self, infile,  from_, to_, outfile):
		pdf2 = fitz.open(infile)
		pdf2.insertPDF(self.pdf, from_page=from_, to_page=to_)
		pdf2.save(outfile)

		return 'done'

	def watermark_pdf_file(self, page_num, image_file, coords, outfile):
		rect = fitz.Rect(*coords)
		page = self.pdf.loadPage(page_num)
		page.insertImage(rect, image_file)
		self.pdf.save(outfile)

		return 'done'

# Custom Functions --------------------------------------------------
def current():
	dt = datetime.datetime.now()
	access_time = dt.strftime('%b %d %Y, %H:%M')
	return access_time

def configuration():
	# images
	if not os.path.exists('images/'):
		os.mkdir('images/')

	# recent
	if not os.path.exists('files/recents.txt'):
		with open('files/recents.txt', 'w') as file:
			file.write('')

	# about
	if not os.path.exists('files/about.txt'):
		with open('files/about.txt', 'w') as file:
			file.write('Moonlight PDF Reader\n\n')
			file.write('Moonlight PDF reader is a simple image\n')
			file.write('based PDF reader created with python.\n\n')
			file.write('Dependencies : pymupdf, pillow \n\n')
			file.write('@Author : Prajjwal Pathak (pyGuru)\n')
			file.write('@Created: 2020-10-11 11:10:00')