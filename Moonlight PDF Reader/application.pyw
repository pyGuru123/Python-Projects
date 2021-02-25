#! python3
"""
@created: 2020-10-11 11:10:00
@author: Prajjwal Pathak ( pyGuru )

Moonlight PDF Reader

-------------------------------------------------------------------------------
Dependencies:

PyMuPDF v1.17.7+
PyMuPDF can be installed by : pip install pymupdf

-------------------------------------------------------------------------------
Description : 
Moonlight PDF Reader is a python tkinter based pdf reader with many of the 
advanced pdf features
"""

import os
import re
import tkinter as tk
import tkinter.simpledialog
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox

from PIL import ImageGrab
import MoonlightMiner
from CustomWidgets import CustomButton, RecentButton, CustomLabel, CustomFrame

class PDFReader(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.bgcolor = 'gray18'
		self.master['bg'] = self.bgcolor

		self.width = self.master.winfo_screenwidth()
		self.height = self.master.winfo_screenheight()

		self.isHome = True
		self.isAbout = False
		self._attributes()

		self.reader_frame()
		self.options_frame()
		self.right_frame()
		self.meta_frame()

		self.isFullscreen = False

		# bindings with master window
		self.master.bind('<F11>', self.toggleFullScreen)
		self.master.bind('<Escape>', self.quitFullScreen)
		self.master.bind('<Left>', self.prev_page)
		self.master.bind('<Up>', self.prev_page)
		self.master.bind('<Right>', self.next_page)
		self.master.bind('<Down>', self.next_page)
		self.master.bind('<Control-plus>', self.zoom_in)
		self.master.bind('<Control-minus>', self.zoom_out)
		self.master.bind('<Return>', self.search_page)
		self.master.bind('<Control-Key-o>', self.open_file)

	def _attributes(self):
		self.miner = None

		self.name = ''
		self.author = ''
		self.creator = ''
		self.producer = ''
		self.isEncrypted = False
		self.size = 0
		self.numPages = 0
		self.last_accessed = ''

		self.from_ = tk.IntVar()
		self.to_ = tk.IntVar()
		self.rotate_all = tk.IntVar()

		self.current_page = 0
		self.pagesize = None
		self.pagewidth = 0
		self.pageheight = 0
		self.zoom = 1

		self.hthick = 0.5
		self.hcolor = 'gray15'

		self.filepath = None
		self.fileisOpen = False
		self.recently_opened = []
		self.other_filepath = None

		self.custom_function = False

		# variables for putting watermark
		self.x1, self.x2, self.y1, self.y2 = tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()

	# Frames

	def reader_frame(self):
		self.reader = tk.Frame(self, bg=self.bgcolor,  highlightthickness=self.hthick,
								highlightcolor=self.hcolor)
		self.reader.configure(width=self.width-350, height=self.height)
		self.reader.grid_propagate(0)
		self.reader.grid(row=0, column=0, rowspan=3)

		if self.fileisOpen:
			# ribbon
			self.ribbon = CustomFrame(self.reader, bg=self.bgcolor)
			self.ribbon.configure(width=self.width-350, height=55)
			self.ribbon.grid(row=0, column=0, columnspan=2, padx=(0,5), sticky='W')

			self.title = CustomLabel(self.ribbon, width=40, text=self.name[:-4])
			self.title.grid(row=0, column=0, sticky='W', pady=(10,0), padx=2)

			self.up = tk.Button(self.ribbon, image=up_icon, bg=self.bgcolor, 
						relief=tk.FLAT, borderwidth=0, command=self.prev_page)
			self.up.grid(row=0, column=1, pady=(5,0), padx=(50,0))

			self.down = tk.Button(self.ribbon, image=down_icon, bg=self.bgcolor, 
						relief=tk.FLAT, borderwidth=0, command=self.next_page)
			self.down.grid(row=0, column=2, pady=(5,0), padx=(5,0))

			self.temp_page = tk.StringVar()
			self.page_search = tk.Entry(self.ribbon, width=5)
			self.page_search['textvariable'] = self.temp_page
			self.page_search.grid(row=0, column=3, pady=(5,0), padx=(25,0))

			self.search = tk.Button(self.ribbon, image=search_icon, bg=self.bgcolor, 
						relief=tk.FLAT, borderwidth=0, command=self.search_page)
			self.search.grid(row=0, column=4, pady=(5,0), padx=(15,2))

			self.pagetext = f'{self.current_page + 1} / {self.numPages + 1}'
			self.pagelabel = CustomLabel(self.ribbon, text=self.pagetext, anchor='c', width=10)
			self.pagelabel.grid(row=0, column=5, padx=5, pady=(5,0))

			self.zoomin = tk.Button(self.ribbon, image=zoom_in_icon, bg=self.bgcolor, 
						relief=tk.FLAT, borderwidth=0, command=self.zoom_in)
			self.zoomin.grid(row=0, column=6, pady=(5,0), padx=(25,0))

			self.zoomout = tk.Button(self.ribbon, image=zoom_out_icon, bg=self.bgcolor, 
						relief=tk.FLAT, borderwidth=0, command=self.zoom_out)
			self.zoomout.grid(row=0, column=7, pady=(5,0), padx=(5,0))

			self.zoomtext = f'{self.zoom * 100} %'
			self.zoomlabel = CustomLabel(self.ribbon, text=self.zoomtext, anchor='c', width=10)
			self.zoomlabel.grid(row=0, column=8, padx=5, pady=(5,0))
			
			# contents
			self.contents = CustomFrame(self.reader, bg=self.bgcolor)
			self.contents.configure(width=250, height=self.height-85)
			self.contents.grid(row=1, column=0)

			self.tablelabel = CustomLabel(self.contents, width=25, text='Table of Content', anchor='c')
			self.tablelabel.grid(row=0, column=0, padx=4, pady=10)

			self.content_scroll = tk.Scrollbar(self.contents, orient=tk.VERTICAL)
			self.content_scroll.grid(row=1, column=1, sticky='ns')

			self.content_list = tk.Listbox(self.contents, selectmode=tk.SINGLE,
					 selectbackground='sky blue', bg=self.bgcolor, fg='white',
					 yscrollcommand=self.content_scroll.set, font=('Times', 10))
			self.content_list.configure(height=38, width=36)
			self.enumerate_content()
			self.content_list.bind('<Double-1>', self.get_page_content)
			self.content_list.bind('<Return>', self.get_page_content)
			self.content_list.bind('<Enter>', self.root_unbind)
			self.content_list.bind('<Leave>', self.root_bind)
			self.content_list.grid(row=1, column=0, padx=2, sticky='W')

			self.content_scroll.config(command=self.content_list.yview)

			# display
			self.display = CustomFrame(self.reader, bg=self.bgcolor, borderwidth=0)
			self.display.configure(width=self.width-100-350, height=self.height-85)
			self.display.grid(row=1, column=1, padx=(0,5))

			self.scrollx = tk.Scrollbar(self.display, orient=tk.VERTICAL)
			self.scrollx.grid(row=0, column=1, sticky='ns')

			self.scrolly = tk.Scrollbar(self.display, orient=tk.HORIZONTAL)
			self.scrolly.grid(row=1, column=0, sticky='we')

			self.output = tk.Canvas(self.display, bg=self.bgcolor)
			self.output.configure(width=740, height=self.height-110,
						yscrollcommand=self.scrollx.set, 
						xscrollcommand=self.scrolly.set)
			self.output.grid(row=0, column=0)

			self.scrollx.configure(command=self.output.yview)
			self.scrolly.configure(command=self.output.xview)
		else:
			self.home_image = tk.Text(self.reader, bg=self.bgcolor, width=126, height=46)
			self.home_image.grid(row=0, column=0)
			self.home_image.insert(tk.END, '\n\n\n\n\n\n\t\t ')
			self.home_image.image_create(tk.END, image = moonlight)
			self.home_image.configure(state='disabled')


	def options_frame(self):
		self.options = CustomFrame(self, bg=self.bgcolor)
		self.options.configure(width=350, height=55)
		self.options.grid(row=0, column=1, pady=(6,0))

		self.homebutton = CustomButton(self.options, text='Home', width=10,  command=self.toggle_home)
		self.homebutton.grid(row=0, column=0, sticky='W', padx=(10, 20), pady=(1,1))

		self.toolsbutton = CustomButton(self.options, text='Tools', width=10, command=self.toggle_tools)
		self.toolsbutton.grid(row=0, column=1, sticky='W', padx=(5, 20), pady=(1,1))

		self.aboutbutton = CustomButton(self.options, text='About', width=10, command=self.toggle_about)
		self.aboutbutton.grid(row=0, column=2, sticky='W', padx=(5, 20), pady=(1,1))

	def right_frame(self):
		# frame for all custom functions on the right
		self.rightSidebar = CustomFrame(self, bg=self.bgcolor)
		self.rightSidebar.configure(width=350, height=self.height-400)
		self.rightSidebar.grid(row=1, column=1)

		# check if home option is selected, its by-default
		if self.isHome:
			self.openbutton = CustomButton(self.rightSidebar, text='Open', command=self.open_file)
			self.openbutton.grid(row=0, column=0, sticky='W', pady=(20,0), padx=10)

			self.savetext = CustomButton(self.rightSidebar, text='Save as Text', command=self.get_text)
			self.savetext.grid(row=1, column=0, sticky='W', pady=(10,0), padx=10)

			self.closebutton = CustomButton(self.rightSidebar, text='Close File', command=self.close_file)
			self.closebutton.grid(row=2, column=0, sticky='W', pady=(10,0), padx=10)

			self.quitbutton = CustomButton(self.rightSidebar, text='Quit App', command=self.quit)
			self.quitbutton.grid(row=3, column=0, sticky='W', pady=(10,0), padx=10)

			if not self.fileisOpen:
				self.savetext.configure(state='disabled')
				# self.snapshot.configure(state='disabled')
				self.closebutton.configure(state='disabled')

		# check if about option is selected, gives info about Moonlight
		elif self.isAbout:
			self.aboutbox = tk.Text(self.rightSidebar, bg=self.bgcolor, width=40, height=20,
							relief=tk.FLAT, borderwidth=0, fg='white smoke',
							font=('TkDefaultFont', 12))
			
			with open('files/about.txt', 'r') as file:
				data = file.read()

			self.aboutbox.insert(tk.END, data)
			self.aboutbox.configure(state='disabled')
			self.aboutbox.grid(row=0, column=0, sticky='W', pady=(10,0), padx=10)

		# check if some custom function is clicked under tools functions
		elif self.custom_function:
			pass

		# tools option is selected under which lies variety of custom function
		else:
			self.extract = CustomButton(self.rightSidebar, text='Extract Page',
							command=self.extract_page)
			self.extract.grid(row=0, column=0, sticky='W', pady=(10,0), padx=10)

			self.extract_image = CustomButton(self.rightSidebar, text='Extract Images',
							command=self.extract_images)
			self.extract_image.grid(row=0, column=1, sticky='W', pady=(10,0), padx=10)

			self.rotate = CustomButton(self.rightSidebar, text='Rotate Page',
							command=self.rotate_page_frame)
			self.rotate.grid(row=1, column=0, sticky='W', pady=(10,0), padx=10)

			self.export = CustomButton(self.rightSidebar, text='Export PDF',
							command=self.export_pdf_frame)
			self.export.grid(row=1, column=1, sticky='W', pady=(15,0), padx=10)

			self.encrypt = CustomButton(self.rightSidebar, text='Encrypt PDF',
							command=self.encrypt_pdf)
			self.encrypt.grid(row=2, column=0, sticky='W', pady=(15,0), padx=10)

			self.decrypt = CustomButton(self.rightSidebar, text='Decrypt PDF',
							command=self.decrypt_pdf)
			self.decrypt.grid(row=2, column=1, sticky='W', pady=(15,0), padx=10)

			self.split = CustomButton(self.rightSidebar, text='Split PDF',
							command=self.split_pdf_frame)
			self.split.grid(row=3, column=0, sticky='W', pady=(15,0), padx=10)

			self.merge = CustomButton(self.rightSidebar, text='Merge PDF',
							command=self.merge_pdf_frame)
			self.merge.grid(row=3, column=1, sticky='W', pady=(15,0), padx=10)

			self.watermark = CustomButton(self.rightSidebar, text='watermark PDF',
							command=self.watermark_pdf_frame)
			self.watermark.grid(row=4, column=0, sticky='W', pady=(15,0), padx=10)
			
			if not self.fileisOpen:
				self.extract.configure(state='disabled')
				self.extract_image.configure(state='disabled')
				self.rotate.configure(state='disabled')
				self.export.configure(state='disabled')
				self.encrypt.configure(state='disabled')
				self.decrypt.configure(state='disabled')
				self.split.configure(state='disabled')
				self.merge.configure(state='disabled')
				self.watermark.configure(state='disabled')

			if self.isEncrypted:
				self.encrypt.configure(state='disabled')
			else:
				self.decrypt.configure(state='disabled')


	def meta_frame(self):
		# Frame for pdf metadata and recents
		self.metadata = CustomFrame(self, bg=self.bgcolor)
		self.metadata.configure(width=350, height=350, highlightthickness=self.hthick,
								highlightcolor=self.hcolor)
		self.metadata.grid(row=2, column=1)

		if not self.fileisOpen:
			self.recent = CustomLabel(self.metadata, text='Recent')
			self.recent.grid(row=0, column=0, sticky='W', pady=(10,5), padx=10)

			with open('files/recents.txt' ,'r') as file:
				self.recently_opened = file.readlines()

			if len(self.recently_opened) == 0:
				noFileIsOpen = CustomLabel(self.metadata, text='No file is opened recently')
				noFileIsOpen.grid(row=1, column=0, sticky='W', pady=(20,0), padx=10)
			else:
				cnrow = 1
				self.recently_opened = self.recently_opened[:5]
				for recent in range(0, len(self.recently_opened)):
					data = self.recently_opened[recent].split(';')
					filepath = data[0]
					name = os.path.basename(filepath)[:-4]
					size = data[1]
					text = f"\n {name[:25]:<30}, {size}\n {data[2]}"
					btn = RecentButton(self.metadata, text=text,
							command = lambda temppath = filepath:self.open_recent(temppath))
					btn.grid(row=cnrow+recent, column=0, pady=(8,0), padx=10 )
			
		else:
			self.nameLabel = CustomLabel(self.metadata, text=self.name)
			self.nameLabel.grid(row=0, column=0, sticky='W', pady=(10,0), padx=10)

			self.sizeLabel = CustomLabel(self.metadata, text='Size : ' + self.size)
			self.sizeLabel.grid(row=1, column=0, sticky='W', pady=(10,0), padx=10)

			self.pagecount = CustomLabel(self.metadata, text='Page Count : ' + str(self.numPages + 1))
			self.pagecount.grid(row=2, column=0, sticky='W', pady=(10,0), padx=10)

			if self.author:
				self.authorLabel = CustomLabel(self.metadata, text='Author : ' + self.author)
				self.sizeLabel.grid(row=3, column=0, sticky='W', pady=(10,0), padx=10)

			if self.creator:
				self.creatorLabel = CustomLabel(self.metadata, text='Creator : ' + self.creator)
				self.creatorLabel.grid(row=4, column=0, sticky='W', pady=(10,0), padx=10)

			if self.producer:
				self.producerLabel = CustomLabel(self.metadata, text='Producer : ' + self.producer)
				self.producerLabel.grid(row=5, column=0, sticky='W', pady=(10,0), padx=10)

			self.widthlabel = CustomLabel(self.metadata, text=f'Page Width : {self.pagewidth:.0f} px')
			self.widthlabel.grid(row=6, column=0, sticky='W', pady=(10,0), padx=10)

			self.heightlabel = CustomLabel(self.metadata, text=f'Page Height : {self.pageheight:.0f} px')
			self.heightlabel.grid(row=7, column=0, sticky='W', pady=(10,0), padx=10)

	# custom function frames start from here

	def rotate_page_frame(self):
		# rotate the pdf page frame
		self.rightSidebar.destroy()
		self.custom_function = True
		self.right_frame()

		label = CustomLabel(self.rightSidebar, text='Page rotate', anchor='c')
		label.grid(row=0, column=0, pady=15, padx=25, columnspan=3)

		anglelabel = CustomLabel(self.rightSidebar, text='Select angle to rotate', anchor='w')
		anglelabel.grid(row=1, column=0, pady=(15,0), padx=25, columnspan=3)

		ANGLES = [("+90", 90), ("180", 180), ("-90", 270)]
		self.angle = tk.IntVar()
		self.angle.set(90)
		self.radios = [self.create_radios(angle) for angle in ANGLES]
		c = 0
		for radio in self.radios:
			radio.grid(row=2, column=c, pady=20)
			c += 1

		checkbutton = tk.Checkbutton(self.rightSidebar, text='Rotate all pages',
								variable=self.rotate_all)
		checkbutton.grid(row=3, column=0, columnspan=2, padx=10)

		rotate = tk.Button(self.rightSidebar, bg=self.bgcolor, text='rotate', width=15, 
						command=self.rotate_page, fg='white', cursor='hand2')
		rotate.grid(row=4, column=0, pady=20, columnspan=2)

		back = tk.Button(self.rightSidebar, bg=self.bgcolor, image=back_icon, 
						command=self.go_to_tools)
		back.grid(row=4, column=2, pady=20)

	def export_pdf_frame(self):
		# export pdf to png / html / xml frame
		self.rightSidebar.destroy()
		self.custom_function = True
		self.right_frame()

		label = CustomLabel(self.rightSidebar, text='Export PDF', anchor='c')
		label.grid(row=0, column=0, pady=15, padx=10, columnspan=2)

		back = tk.Button(self.rightSidebar, bg=self.bgcolor, image=back_icon, 
						command=self.go_to_tools)
		back.grid(row=0, column=2, pady=20)

		png = CustomButton(self.rightSidebar, text='Export to PNG', anchor='c',
						command=lambda : self.miner.get_image(self.current_page))
		png.grid(row=1, column=0, pady=(15,0), padx=10, columnspan=3)

		html = CustomButton(self.rightSidebar, text='Export to HTML',anchor='c',
						command=self.get_html)
		html.grid(row=2, column=0, pady=(15,0), padx=10, columnspan=3)

		xml = CustomButton(self.rightSidebar, text='Export to XML', anchor='c',
						command=self.get_xml)
		xml.grid(row=3, column=0, pady=(15,0), padx=10, columnspan=3)

	def split_pdf_frame(self):
		# split the pdf frame
		self.rightSidebar.destroy()
		self.custom_function = True
		self.right_frame()

		label = CustomLabel(self.rightSidebar, text='Split PDF', anchor='c')
		label.grid(row=0, column=0, pady=15, padx=25, columnspan=3)

		fromlabel = CustomLabel(self.rightSidebar, text='From page : ', anchor='w', width=10)
		fromlabel.grid(row=1, column=0, pady=15, padx=10)

		fromentry = tk.Entry(self.rightSidebar, width=6, bg=self.bgcolor, fg='white')
		fromentry['textvariable'] = self.from_
		fromentry.grid(row=1, column=1, columnspan=2)

		tolabel = CustomLabel(self.rightSidebar, text='To page : ', anchor='w', width=10)
		tolabel.grid(row=2, column=0, pady=15, padx=10) 

		toentry = tk.Entry(self.rightSidebar, width=6, bg=self.bgcolor, fg='white')
		toentry['textvariable'] = self.to_
		toentry.grid(row=2, column=1, columnspan=2)

		split = tk.Button(self.rightSidebar, bg=self.bgcolor, text='Split', width=15, 
						command=self.split_pdf, fg='white', cursor='hand2')
		split.grid(row=3, column=0, pady=20, columnspan=2)

		back = tk.Button(self.rightSidebar, bg=self.bgcolor, image=back_icon, 
						command=self.go_to_tools)
		back.grid(row=3, column=2, pady=20)

	def merge_pdf_frame(self):
		# merge two pdfs frame
		self.rightSidebar.destroy()
		self.custom_function = True
		self.right_frame()

		label = CustomLabel(self.rightSidebar, text='Merge PDF', anchor='c')
		label.grid(row=0, column=0, pady=15, padx=25, columnspan=3)

		self.filelabel = CustomLabel(self.rightSidebar, text='Select File',anchor='w',
								 wraplength=200, height=3, width=20, bg=self.bgcolor)
		self.filelabel.grid(row=1, column=0, pady=15, padx=10, columnspan=2)

		choosefile = tk.Button(self.rightSidebar, image=clip_icon, command=self.choose_file)
		choosefile.grid(row=1, column=2, pady=20)

		infolabel = CustomLabel(self.rightSidebar, text='It will append this pdf in the end of above pdf',
								 anchor='w', width=35)
		infolabel.grid(row=2, column=0, pady=15, padx=10, columnspan=3)

		fromlabel = CustomLabel(self.rightSidebar, text='From page : ', anchor='w', width=10)
		fromlabel.grid(row=3, column=0, pady=15, padx=10)

		fromentry = tk.Entry(self.rightSidebar, width=6, bg=self.bgcolor, fg='white')
		fromentry['textvariable'] = self.from_
		fromentry.grid(row=3, column=1, columnspan=2)

		tolabel = CustomLabel(self.rightSidebar, text='To page : ', anchor='w', width=10)
		tolabel.grid(row=4, column=0, pady=15, padx=10) 

		toentry = tk.Entry(self.rightSidebar, width=6, bg=self.bgcolor, fg='white')
		toentry['textvariable'] = self.to_
		toentry.grid(row=4, column=1, columnspan=2)

		merge = tk.Button(self.rightSidebar, bg=self.bgcolor, text='Merge', width=15, 
						command=self.merge_pdf, fg='white', cursor='hand2')
		merge.grid(row=5, column=0, pady=20, columnspan=2)

		back = tk.Button(self.rightSidebar, bg=self.bgcolor, image=back_icon, 
						command=self.go_to_tools)
		back.grid(row=5, column=2, pady=20)

	def watermark_pdf_frame(self):
		# watermark pdf frame
		self.rightSidebar.destroy()
		self.custom_function = True
		self.right_frame()

		label = CustomLabel(self.rightSidebar, text='Watermark PDF', anchor='c')
		label.grid(row=0, column=0, pady=15, padx=25, columnspan=4)

		self.filelabel = CustomLabel(self.rightSidebar, text='Select File',anchor='w',
								 wraplength=200, height=3, width=20, bg=self.bgcolor)
		self.filelabel.grid(row=1, column=0, pady=15, padx=10, columnspan=3)

		choosefile = tk.Button(self.rightSidebar, image=clip_icon, 
								command=self.choose_image_file)
		choosefile.grid(row=1, column=3, pady=20)

		x1label = CustomLabel(self.rightSidebar, text='x1 : ', anchor='w', width=5)
		x1label.grid(row=2, column=0, pady=15, sticky='W', padx=(25,2))
		x1entry = tk.Entry(self.rightSidebar, width=5, bg=self.bgcolor, fg='white')
		x1entry['textvariable'] = self.x1
		x1entry.grid(row=2, column=1, columnspan=2, sticky='W')

		y1label = CustomLabel(self.rightSidebar, text='y1 : ', anchor='w', width=5)
		y1label.grid(row=2, column=2, pady=15, sticky='W')
		y1entry = tk.Entry(self.rightSidebar, width=5, bg=self.bgcolor, fg='white')
		y1entry['textvariable'] = self.y1
		y1entry.grid(row=2, column=3, columnspan=2, sticky='W')

		x2label = CustomLabel(self.rightSidebar, text='x2 : ', anchor='w', width=5)
		x2label.grid(row=3, column=0, pady=15, sticky='W', padx=(25,2))
		x2entry = tk.Entry(self.rightSidebar, width=5, bg=self.bgcolor, fg='white')
		x2entry['textvariable'] = self.x2
		x2entry.grid(row=3, column=1, columnspan=2, sticky='W')

		y2label = CustomLabel(self.rightSidebar, text='y2 : ', anchor='w', width=5)
		y2label.grid(row=3, column=2, pady=15, sticky='W')
		y2entry = tk.Entry(self.rightSidebar, width=5, bg=self.bgcolor, fg='white')
		y2entry['textvariable'] = self.y2
		y2entry.grid(row=3, column=3, columnspan=2, sticky='W')

		watermark = tk.Button(self.rightSidebar, bg=self.bgcolor, text='Watermark', width=15, 
						command=self.watermark_pdf, fg='white', cursor='hand2')
		watermark.grid(row=4, column=0, pady=20, columnspan=2, padx=(25,2))

		back = tk.Button(self.rightSidebar, bg=self.bgcolor, image=back_icon, 
						command=self.go_to_tools)
		back.grid(row=4, column=3, pady=20)


	# Frame Switches --------------------------------------------------------------------

	def toggleFullScreen(self, event):
		# toggle to fullscreen
		if self.isFullscreen == False:
			self.master.attributes('-fullscreen', True)
			self.isFullscreen = True

	def quitFullScreen(self, event):
		# quit the fullscreen window
		if self.isFullscreen == True:
			self.master.attributes('-fullscreen', False)
			self.isFullscreen = False

	def create_radios(self, option):
		# create a radio button
		text, value = option
		radio = tk.Radiobutton(self.rightSidebar, text=text, value=value, variable=self.angle,
					 font=('Arial', 11)) 
		return radio

	def choose_file(self):
		# choose a pdf file
		self.other_filepath = filedialog.askopenfilename(initialdir=cwd, filetypes=(("PDF","*.pdf"),))
		if self.other_filepath:
			self.filelabel['text'] = os.path.basename(self.other_filepath)

	def choose_image_file(self):
		# choose a image for watermarking the pdf
		self.other_filepath = filedialog.askopenfilename(initialdir=cwd, 
					filetypes=(("PNG","*.png"),("JPG", '.jpg')))
		if self.other_filepath:
			self.filelabel['text'] = os.path.basename(self.other_filepath)

	def choose_saveasname(self, text):
		# choose a new filename for saving the pdf
		filename = os.path.basename(self.filepath)[:-4] + ' - ' + text + '.pdf'
		filetypes = [('PDF', '*.pdf')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
							filetypes=filetypes)

		return filepath

	def go_to_tools(self):
		# go back to tools frame from a custom function frame
		self.custom_function = False
		self.toggle_tools()

	def toggle_home(self):
		# toggle to the home frame
		self.custom_function = False
		self.isHome = True
		self.isAbout = False
		self.rightSidebar.destroy()
		self.right_frame()

	def toggle_tools(self):
		# toggle to the tools frame
		self.isHome = False
		self.isAbout = False
		self.rightSidebar.destroy()
		self.right_frame()

	def toggle_about(self):
		# toggle to the about frame
		self.custom_function = False
		self.isHome = False
		self.isAbout = True
		self.rightSidebar.destroy()
		self.right_frame()

	# Custom Functions -------------------------------------------------------------------

	def open_recent(self, filepath):
		# take the filepath from the recently opened and open it
		self.open_file(temppath=filepath)

	def open_file(self, event=None, temppath=None):
		# open a new file
		if temppath is None:
			temppath = filedialog.askopenfilename(initialdir=cwd, filetypes=(("PDF","*.pdf"),))
		if temppath:
			if self.fileisOpen:
				self.close_file()
			self.filepath = temppath
			self.name = os.path.basename(self.filepath)
			self.size = str(round(os.stat(self.filepath).st_size / (1024 * 1024), 1)) + 'MB'

			self.isEncrypted = MoonlightMiner.pdf_is_encrypted(self.filepath)
			if self.isEncrypted:
				password = tkinter.simpledialog.askstring("Password", "Enter password:", show='*')
				try:
					self.miner = MoonlightMiner.Miner(self.filepath, password)
					data, self.numPages, self.content, self.pagesize = self.miner.read_pdf()
				except:
					messagebox.showerror('Moonlight PDF Reader', 'Incorrect password')
					self.close_file()
					return ''
			else:
				self.miner = MoonlightMiner.Miner(self.filepath)
				data, self.numPages, self.content, self.pagesize = self.miner.read_pdf()
			
			self.pagewidth, self.pageheight = self.pagesize
			self.numPages -= 1
			self.author = data['author']
			self.creator = data['creator']
			self.producer = data['producer']

			self.fileisOpen = True
			
			self.rightSidebar.destroy()
			self.right_frame()

			self.metadata.destroy()
			self.meta_frame()

			self.reader.destroy()
			self.reader_frame()

			self.update()
			self.get_image()

			self.add_to_recents()

	def close_file(self):
		# close the currently opened file
		self._attributes()

		self.rightSidebar.destroy()
		self.right_frame()

		self.metadata.destroy()
		self.meta_frame()

		self.reader.destroy()
		self.reader_frame()

	def enumerate_content(self):
		# fill table of contents on the left side listbox
		for index, lst in enumerate(self.content):
			self.content_list.insert(index, lst[1])

	def get_image(self):
		# get a image of the pdf page based on zoom level
		dct = {
			0.6 : 200,
			0.8 : 160,
			1 : 100,
			1.2 : 70,
			1.4 : 10,
			1.6 : 2
		}

		self.zoomtext = f'{self.zoom * 100:.0f} %'
		self.zoomlabel['text'] = self.zoomtext

		x = dct[self.zoom]
		self.img_file = self.miner.get_page(self.current_page, self.zoom)
		self.output.create_image(x, 10, anchor='nw', image=self.img_file)

		region = self.output.bbox(tk.ALL)
		self.output.configure(scrollregion=region)

	def zoom_in(self, event=None):
		# zoom in the pdf page
		if self.fileisOpen:
			if self.zoom < 1.6:
				self.zoom = round(self.zoom + 0.2, 1)
				self.get_image()

	def zoom_out(self, event=None):
		# zoom out of the pdf page
		if self.fileisOpen:
			if self.zoom > 0.6:
				self.zoom = round(self.zoom - 0.2, 1)
				self.get_image()

	def page_update(self, current):
		# show an image version of the current pdf page in the center canvas
		self.pagetext = f'{current + 1} / {self.numPages + 1}'
		self.pagelabel['text'] = self.pagetext

		self.get_image()

	def prev_page(self, event=None):
		# turn over to the previous page
		if self.fileisOpen:
			if self.current_page > 0:
				self.current_page -= 1

				self.page_update(self.current_page)

	def next_page(self, event=None):
		# turn over to the next page
		if self.fileisOpen:
			if self.current_page <= self.numPages - 1:
				self.current_page += 1

				self.page_update(self.current_page)

	def search_page(self, event=None):
		# search for the specific page in the pdf
		pgnum = self.temp_page.get()
		if self.fileisOpen and pgnum:
			if 0 < int(pgnum) <= self.numPages + 1:
				self.current_page = int(pgnum) - 1

				self.page_update(self.current_page)
			self.page_search.delete(0, 'end')

	def get_page_content(self, event):
		# get pdf table of content
		if event is not None:
			index = self.content_list.curselection()[0]
			self.current_page = self.content[index][2]
			self.current_page -= 1
			self.page_update(self.current_page)

	def extract_page(self):
		# extract the current page and save as a new pdf file
		filename = os.path.basename(self.filepath)[:-4] + ' - Page ' + str(self.current_page + 1) + '.pdf'
		filetypes = [('PDF', '*.pdf')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
							filetypes=filetypes)
		if filepath:
			status = self.miner.extract_pdf_page(self.current_page, filepath)
			if status == 'done':
				messagebox.showinfo('Moonlight PDF Reader', f'Page extracted successfully')
		

	def extract_images(self):
		# extract all images from the current page of the pdf file
		num_images = self.miner.extract_page_images(self.current_page)
		if num_images > 0:
			messagebox.showinfo('Moonlight PDF Reader', f'{num_images} images extracted')
		else:
			messagebox.showerror('Moonlight PDF Reader', 'No images found')

	def rotate_page(self):
		# rotate single / all pages of the pdf file and save it into a new file
		if self.rotate_all.get():
			filepath = self.choose_saveasname('Rotated')
			from_ = 0
			to_ = self.numPages
		else:
			filename = os.path.basename(self.filepath)[:-4] + ' - Page ' + str(self.current_page + 1) + 'rotated.pdf'
			filetypes = [('PDF', '*.pdf')]
			filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
								filetypes=filetypes)
			from_ = self.current_page
			to_ = self.current_page

		if filepath:
			status = self.miner.rotate_pdf_page(from_, to_, filepath, self.angle.get())
			if status == 'done':
				messagebox.showinfo('Moonlight PDF Reader', f'Page rotated and saved')

	def encrypt_pdf(self):
		# encrypt the pdf file with user given password
		password = tkinter.simpledialog.askstring("Password", "Enter password:", show='*')
		if len(password) >= 5:
			filepath = self.choose_saveasname('Encrypted')
			if filepath:
				status = self.miner.encrypt_pdf_file(password, filepath)
				if status:
					messagebox.showinfo('Moonlight PDF Reader', 'Encrypted successfully')
				else:
					messagebox.showerror('Moonlight PDF Reader', 'Unknown error occured')
		else:
			messagebox.showerror('Moonlight PDF Reader', 'Password is too short')

	def decrypt_pdf(self):
		# remove the password protection from pdf file if its password protected
		filepath = self.choose_saveasname('Decrypted')
		if filepath:
			if filepath != self.filepath:
				status = self.miner.decrypt_pdf_file(filepath)
				if status:
					messagebox.showinfo('Moonlight PDF Reader', 'Decrypted successfully')
				else:
					messagebox.showerror('Moonlight PDF Reader', 'Unknown error occured')
			else:
				messagebox.showerror('Moonlight PDF Reader', 'File with this name already exist')

	def split_pdf(self):
		# split this pdf pages and save into a new pdf file
		from_ = self.from_.get()
		to_ = self.to_.get()
		if 0<=from_<self.numPages and 0<=to_<self.numPages:
			filepath = self.choose_saveasname('Splitted')
			if filepath:
				if filepath != self.filepath:
					status = self.miner.split_pdf_file(from_, to_, filepath)
					if status:
						messagebox.showinfo('Moonlight PDF Reader', 'Splitted successfully')
					else:
						messagebox.showerror('Moonlight PDF Reader', 'Unknown error occured')
				else:
					messagebox.showerror('Moonlight PDF Reader', 'File with this name already exist')

			self.from_.set(0)
			self.to_.set(0)
		else:
			messagebox.showerror('Moonlight PDF Reader','Page Index out of range')

	def merge_pdf(self):
		# merge this pdf file / page with at the end of another pdf file
		if self.other_filepath:
			from_ = self.from_.get()
			to_ = self.to_.get()

			if 0<=from_<self.numPages and 0<=to_<self.numPages:
				filepath = self.choose_saveasname('Merged')
				if filepath:
					if filepath != self.filepath:
						status = self.miner.merge_pdf_file(self.other_filepath, from_ , to_, filepath)
						if status:
							messagebox.showinfo('Moonlight PDF Reader', 'Merged successfully')
						else:
							messagebox.showerror('Moonlight PDF Reader', 'Unknown error occured')
					else:
						messagebox.showerror('Moonlight PDF Reader', 'File with this name already exist')

				self.from_.set(0)
				self.to_.set(0)
			else:
				messagebox.showerror('Moonlight PDF Reader','Page Index out of range')
		else:
			messagebox.showerror('Moonlight PDF Reader', 'Select a file first')

	def watermark_pdf(self):
		# watermark the pdf file with selected images under the selected region
		if self.other_filepath:
			x1 = self.x1.get()
			y1 = self.x1.get()
			x2 = self.x2.get()
			y2 = self.x2.get()

			pdfname = os.path.basename(self.filepath)[:-4]
			filename = pdfname + ' - Page ' + str(self.current_page + 1) + 'watermarked.pdf'
			filetypes = [('PDF', '*.pdf')]
			filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
								filetypes=filetypes)

			if filepath:
				if filepath != self.filepath:
					coords = (x1,y1,x2,y2)
					status = self.miner.watermark_pdf_file(self.current_page, self.other_filepath,
											 coords, filepath)
					if status:
						messagebox.showinfo('Moonlight PDF Reader', 'Watermarked successfully')
					else:
						messagebox.showerror('Moonlight PDF Reader', 'Unknown error occured')
				else:
					messagebox.showerror('Moonlight PDF Reader', 'File with this name already exist')

	def root_unbind(self, event):
		# unbind these events from master window
		self.content_list.focus_set()
		self.master.bind('<Left>', self.do_nothing)
		self.master.bind('<Up>', self.do_nothing)
		self.master.bind('<Right>', self.do_nothing)
		self.master.bind('<Down>', self.do_nothing)

	def root_bind(self, event):
		# bind these events again with the master window
		self.master.focus_set()
		self.master.bind('<Left>', self.prev_page)
		self.master.bind('<Up>', self.prev_page)
		self.master.bind('<Right>', self.next_page)
		self.master.bind('<Down>', self.next_page)

	def do_nothing(self, event):
		# this function does nothing still useful
		pass

	def get_text(self):
		# extract text out of pdf page
		text = self.miner.get_text(self.current_page, 'text')
		pdfname = os.path.basename(self.filepath)[:-4]
		filename = pdfname + ' - Page ' + str(self.current_page + 1) + '.txt'
		filetypes = [('Text', '*.txt')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
							filetypes=filetypes)

		if filepath:			
			with open(filepath, 'w', encoding='utf-8') as file:
				file.write(text)

	def get_html(self):
		# get html file out of pdf page content
		text = self.miner.get_text(self.current_page, 'html')
		pdfname = os.path.basename(self.filepath)[:-4]
		filename = pdfname + ' - Page ' + str(self.current_page + 1) + '.html'
		filetypes = [('HTML', '*.html')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
							filetypes=filetypes)

		if filepath:			
			with open(filepath, 'w', encoding='utf-8') as file:
				file.write(text)

	def get_xml(self):
		# get xml file out of pdf page content
		text = self.miner.get_text(self.current_page, 'xml')
		pdfname = os.path.basename(self.filepath)[:-4]
		filename = pdfname + ' - Page ' + str(self.current_page + 1) + '.xml'
		filetypes = [('XML', '*.xml')]
		filepath = filedialog.asksaveasfilename(initialdir=cwd, initialfile=filename, 
							filetypes=filetypes)

		if filepath:			
			with open(filepath, 'w', encoding='utf-8') as file:
				file.write(text)

	def add_to_recents(self):
		# add currently opened file to recents text file
		with open('files/recents.txt', 'r') as file:
			data = file.readlines()

		access_time = MoonlightMiner.current()
		content = self.filepath + ';' + self.size
		regex = re.compile(f'^{content}')
		for entry in range(len(data)):
			if re.match(regex, data[entry]):
				del data[entry]
				break
		content += (';' + access_time + '\n')
		data.insert(0, content)
		data = data[:6]

		with open('files/recents.txt', 'w') as file:
			file.writelines(data)


if __name__ == '__main__':
	cwd = os.getcwd()
	MoonlightMiner.configuration()

	# master window
	root = tk.Tk()
	root.state('zoomed')
	root.resizable(0,0)
	root.title('Moonlight PDF Reader')
	root.iconbitmap('icons/moonlight.ico')

	moonlight = PhotoImage(file='files/home.png')

	# icons used in Moonlight
	up_icon = PhotoImage(file='icons/up.png')
	down_icon = PhotoImage(file='icons/down.png')
	zoom_in_icon = PhotoImage(file='icons/zoom_in.png')
	zoom_out_icon = PhotoImage(file='icons/zoom_out.png')
	search_icon = PhotoImage(file='icons/search.png')
	back_icon = PhotoImage(file='icons/back.png')
	clip_icon = PhotoImage(file='icons/clip.png')

	app = PDFReader(master=root)
	app.mainloop()