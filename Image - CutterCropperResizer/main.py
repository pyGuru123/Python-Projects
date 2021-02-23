import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ALL, EventType
from tkinter import filedialog

from cutter import ImageProcessor

cwd = os.getcwd()

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.grid()

		self.filepath = None
		self.zoom_val = tk.IntVar()
		self.zoom_val.set(100)
		self.crop_option = tk.IntVar()
		self.options = {'Divide by TileSize':1, 'Divide in Rows & Columns':2, 'Custom Cropping':3,
						'Rectangular Selection' : 4}
		self.image = None
		self.lines = []

		self.x = tk.IntVar()
		self.y = tk.IntVar()
		self.tilewidth = tk.IntVar()
		self.tileheight = tk.IntVar()
		self.tilewidth.set(24)
		self.tileheight.set(24)
		self.rows = tk.IntVar()
		self.columns = tk.IntVar()

		self.draw_frames()
		self.draw_canvas()
		self.draw_options_frame()
		self.draw_header_frame()
		self.draw_menu_frame()

		self.master.bind('<Up>', self._go_up)
		self.master.bind('<Down>', self._go_down)
		self.master.bind('<Enter>', self._bound_to_mousewheel)
		self.master.bind('<Leave>', self._unbound_to_mousewheel)

	def draw_frames(self):
		self.canvas_frame = tk.Frame(self, width=600, height=500, bg='white')
		self.canvas_frame.grid(row=0, column=1, rowspan=2)
		self.canvas_frame.grid_propagate(False)

		self.editor_frame = tk.Frame(self, width=200, height=400, bg='green')
		self.editor_frame.grid(row=0, column=2)
		self.editor_frame.grid_propagate(False)

		self.options_frame = tk.Frame(self, width=200, height=100, bg='white')
		self.options_frame.grid(row=1, column=2)
		self.options_frame.grid_propagate(False)

		self.header_frame = tk.Frame(self.editor_frame, width=200, height=50, bg='white')
		self.header_frame.grid(row=0, column=0)
		self.header_frame.grid_propagate(False)

		self.menu_frame = tk.Frame(self.editor_frame, width=200, height=110, bg='white')
		self.menu_frame.grid(row=1, column=0)
		self.menu_frame.grid_propagate(False)

		self.variable_frame = tk.Frame(self.editor_frame, width=200, height=100, bg='white')
		self.variable_frame.grid(row=2, column=0)
		self.variable_frame.grid_propagate(False)

	def draw_canvas(self):
		self.scrolly = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
		self.scrolly.grid(row=0, column=1, sticky='ns')

		self.scrollx = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)
		self.scrollx.grid(row=1, column=0, sticky='we')

		self.canvas = tk.Canvas(self.canvas_frame, width=580, height=480, bg='#242424',
						yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)
		self.canvas.grid(row=0, column=0)

		self.scrolly.configure(command=self.canvas.yview)
		self.scrollx.configure(command=self.canvas.xview)

		self.canvas.bind('<ButtonPress-1>', lambda event: self.canvas.scan_mark(event.x, event.y))
		self.canvas.bind("<B1-Motion>", lambda event: self.canvas.scan_dragto(event.x, event.y, gain=1))

	def draw_options_frame(self):
		self.open = ttk.Button(self.options_frame, text='Open', width=12, command=self.open_img)
		self.open.grid(row=0, column=0, padx=(5,0), pady=(4,0))

		self.resize = ttk.Button(self.options_frame, text='Resize', width=12, state=tk.DISABLED)
		self.resize.grid(row=0, column=1, padx=(5,0), pady=(4,0))

		self.crop = ttk.Button(self.options_frame, text='Crop', width=12, state=tk.DISABLED)
		self.crop.grid(row=1, column=0, padx=(5,0), pady=(4,0))

		self.save = ttk.Button(self.options_frame, text='Save Sprites', width=12, state=tk.DISABLED,
					command=self.do_zoom)
		self.save.grid(row=1, column=1, padx=(5,0), pady=(4,0))

		self.scaler = ttk.Scale(self.options_frame, from_=5, to=160, orient=tk.HORIZONTAL)
		self.scaler['variable'] = self.zoom_val
		self.scaler.set(100)
		self.scaler.bind("<ButtonRelease-1>", self.do_zoom)
		self.scaler.grid(row=2, column=0, columnspan=2, pady=5)
		self.scaler.grid_forget()

	def draw_header_frame(self):
		self.header = tk.Label(self.header_frame, bg='#242424', fg='#fff', width=27)
		self.header.grid(row=0, column=0)

		self.size = tk.Label(self.header_frame, bg='#242424', fg='#fff', width=27)
		self.size.grid(row=1, column=0)

	def draw_menu_frame(self):
		r = 0
		for text, value in self.options.items():
			ttk.Radiobutton(self.menu_frame, text=text, variable=self.crop_option,
					value=value, command=self.draw_variable_frame,
					width=25).grid(row=r, column=0, padx=10, pady=2)
			r += 1

		self.crop_option.set(1)
		self.draw_variable_frame()

	def draw_variable_frame(self):
		for widget in self.variable_frame.winfo_children():
			widget.destroy()

		opt = self.crop_option.get()

		if opt == 1:
			self.tilewidth.set(24)
			self.tileheight.set(24)

			tk.Label(self.variable_frame, text='Tile Width', width=12).grid(row=0, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.tilewidth
						).grid(row=0, column=1, padx=15, pady=5)
			tk.Label(self.variable_frame, text='Tile Height', width=12).grid(row=1, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.tileheight
						).grid(row=1, column=1, padx=15, pady=5)

			ttk.Button(self.variable_frame, text='Draw Tiles', command=self.draw_tiles).grid(
							row=2,column=0, columnspan=2)
		if opt == 2:
			tk.Label(self.variable_frame, text='Num Rows', width=12).grid(row=0, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.rows
						).grid(row=0, column=1, padx=15, pady=5)
			tk.Label(self.variable_frame, text='Num Columns', width=12).grid(row=1, column=0, padx=5)
			ttk.Entry(self.variable_frame, width=5,textvariable=self.columns
						).grid(row=1, column=1, padx=15, pady=5)

			ttk.Button(self.variable_frame, text='Draw Rows & Columns', command=self.draw_rc).grid(
							row=2,column=0, columnspan=2)

		if opt == 3:
			self.x.set(0)
			self.y.set(0)
			self.tilewidth.set(24)
			self.tileheight.set(24)

			tk.Label(self.variable_frame, text='x', width=8).grid(row=0, column=0)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.x
						).grid(row=0, column=1)
			tk.Label(self.variable_frame, text='y', width=8).grid(row=0, column=2)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.y
						).grid(row=0, column=3)

			tk.Label(self.variable_frame, text='width', width=8).grid(row=1, column=0)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.tilewidth
						).grid(row=1, column=1)
			tk.Label(self.variable_frame, text='height', width=8).grid(row=1, column=2)
			ttk.Entry(self.variable_frame, width=4,textvariable=self.tileheight
						).grid(row=1, column=3)

			ttk.Button(self.variable_frame, text='Draw Rect', command=self.draw_rect).grid(
							row=2,column=0, columnspan=4)

	def open_img(self):
		filetypes = (("Images","*.png .jpg"),)
		path = filedialog.askopenfilename(initialdir=cwd, filetypes=filetypes)
		if path:
			self.filepath = path
			self.imobject = ImageProcessor(self.filepath)
			self.image, size = self.imobject.display_image()
			self.canvas.create_image(0, 0, anchor='nw', image=self.image)

			self.header['text'] = os.path.basename(self.filepath)
			self.size['text'] = f'{size[0]}x{size[1]}'

			region = self.canvas.bbox(tk.ALL)
			self.canvas.configure(scrollregion=region)

			self.resize.config(state=tk.NORMAL)
			self.crop.config(state=tk.NORMAL)
			self.save.config(state=tk.NORMAL)

			self.scaler.grid(row=2, column=0, columnspan=2, pady=5)

	def do_zoom(self, event=None):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		factor = self.zoom_val.get()
		self.image = self.imobject.zoom(factor)
		self.canvas.create_image(0, 0, anchor='nw', image=self.image)

		region = self.canvas.bbox(tk.ALL)
		self.canvas.configure(scrollregion=region)

	def show_option(self):
		print(self.tilewidth.get())
		print(self.self.tileheight.get())

	def draw_tiles(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		tile_width = self.tilewidth.get()
		tile_height = self.tileheight.get()

		if (tile_width or tile_height) and self.image:
			im_width = self.image.width()
			im_height = self.image.height()

			x, y = 0, 0

			if tile_height:
				rows = int(im_height / tile_height)
				for _ in range(rows+1):
					id_ = self.canvas.create_line(0,y,im_width, y, fill='dodgerblue3')
					self.lines.append(id_)
					y += tile_height
			if tile_width:
				cols = int(im_width / tile_width)
				for _ in range(cols+1):
					id_ = self.canvas.create_line(x,0,x, im_height, fill='dodgerblue3')
					self.lines.append(id_)
					x += tile_width

	def draw_rc(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		rows = self.rows.get()
		cols= self.columns.get()
		print(rows,cols)

		if (rows or cols) and self.image:
			im_width = self.image.width()
			im_height = self.image.height()

			x, y = 0, 0

			if rows:
				r = int(im_height / rows)
				for _ in range(rows+1):
					id_ = self.canvas.create_line(0,y,im_width, y, fill='dodgerblue3')
					self.lines.append(id_)
					y += r
			if cols:
				c = int(im_width / cols) 
				for _ in range(cols+1):
					id_ = self.canvas.create_line(x,0,x, im_height, fill='dodgerblue3')
					self.lines.append(id_)
					x += c

	def draw_rect(self):
		if self.lines:
			for id_ in self.lines:
				self.canvas.delete(id_)
			self.lines.clear()

		x = self.x.get()
		y = self.y.get()
		width_ = self.tilewidth.get()
		height = self.tileheight.get()

		id_ = self.canvas.create_rectangle(x,y, x+width_, y+height, outline='dodgerblue3', width=2)
		self.lines.append(id_)

	def _bound_to_mousewheel(self, event):
		self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

	def _unbound_to_mousewheel(self, event):
		self.canvas.unbind_all("<MouseWheel>") 

	def _on_mousewheel(self, event):
		self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

	def _go_up(self, event):
		self.canvas.yview_scroll(-1, "units")

	def _go_down(self, event):
		self.canvas.yview_scroll(1, "units")

	def _yview(self, *args):
		if self.canvas.yview() == (0.0, 1.0):
			return self.canvas.yview(*args)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('800x500+200+100')
	root.title('Sprite Cutter')

	app = Application(master=root)
	app.mainloop()