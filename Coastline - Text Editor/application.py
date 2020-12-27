#! python3
"""
@created: 2020-10-24 07:33:35
@author: Prajjwal Pathak ( pyGuru )

Coastline Text Editor

-------------------------------------------------------------------------------
Dependencies:

No external package is required

-------------------------------------------------------------------------------
Description : 
Coastline Text Editor is a python tkinter based text editor lashed with many of the 
advanced text editing features
"""

import re
import os, sys
import datetime
import win32api
import win32print
import webbrowser
import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog
from tkinter import font, messagebox, PhotoImage
from tkinter import colorchooser, filedialog

cwd = os.getcwd()

class CustomButton(tk.Button):
	def __init__(self, parent, *args,  **kwargs):
		tk.Button.__init__(self, parent, *args,  **kwargs)
		self.parent = parent
		self.is_clicked = False

		self.configure(relief=tk.FLAT, cursor='hand2', bg='white', border=2)
		self.bind('<Button-1>', self.on_click)

	def on_click(self, event):
		if not self.is_clicked:
			self.configure(bg='cyan3')
			self.is_clicked = True
		else:
			self.configure(bg='white')
			self.is_clicked = False

class TextEditor(tk.Tk):
	def __init__(self):
		super().__init__()

		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()

		self['bg'] = 'red'

		self._attributes()
		self.load_icons()
		self.draw_menu()
		self.draw_frames()
		self.draw_widgets()
		self.add_bindings()
		self.set_tracing()
		self.set_tags()
		self.create_dictionaries()

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=0)
		self.grid_rowconfigure(0, weight=0)
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=0)

		self.bind('<Control-Key-n>', self.new_file)
		self.bind('<Control-Key-o>', self.open_file)
		self.bind('<Control-Key-s>', self.save_file)
		self.bind('<Control-Shift-Key-S>', self.save_as_file)
		self.bind('<Control-Key-p>', self.print_file)
		self.bind('<Control-Key-f>', self.find)
		self.bind('<Control-Key-h>', self.find_and_replace)
		self.bind('<Control-Key-r>', self.find_regex)
		self.bind('<Return>', self.find_text)
		self.bind('<F11>', self.toggleFullScreen)
		self.bind('<Escape>', self.quitFullScreen)

	# Attributes -----------------------------------------------------------------------------

	def _attributes(self):
		self.file_is_saved = False
		self.font_family = tk.StringVar()
		self.font_family.set('Arial')
		self.font_size = tk.IntVar()
		self.font_size.set(12)
		self.align = 'left'

		self.filename = '*untitled'
		self.filepath = ''

		self.isFullscreen = False
		self.yetToSearch = True
		self.search_term = tk.StringVar()

		self.find_from_menu = False
		self.initial_len = 0

		self.boldOn = False
		self.italicOn = False
		self.underlineOn = False
		self.overstrikeOn = False

	def load_icons(self):
		self.new_icon = PhotoImage(file='icons/new.png')
		self.open_icon = PhotoImage(file='icons/open.png')
		self.save_icon = PhotoImage(file='icons/save.png')
		self.save_as_icon = PhotoImage(file='icons/save_as.png')
		self.print_icon = PhotoImage(file='icons/print.png')
		self.exit_icon = PhotoImage(file='icons/exit.png')

		self.cut_icon = PhotoImage(file='icons/cut.png')
		self.copy_icon = PhotoImage(file='icons/copy.png')
		self.paste_icon = PhotoImage(file='icons/paste.png')
		self.select_all_icon = PhotoImage(file='icons/select_all.png')
		self.clear_all_icon = PhotoImage(file='icons/clear_all.png')
		self.undo_icon = PhotoImage(file='icons/undo.png')
		self.redo_icon = PhotoImage(file='icons/redo.png')

		self.sum_icon = PhotoImage(file='icons/sum.png')
		self.avg_icon = PhotoImage(file='icons/avg.png')
		self.count_icon = PhotoImage(file='icons/count.png')
		self.datetime_icon = PhotoImage(file='icons/calendar.png')

		self.help_icon = PhotoImage(file='icons/help.png')
		self.coastline_icon = PhotoImage(file='icons/coastline_icon.png')

		self.bold_icon = PhotoImage(file='icons/bold.png')
		self.italic_icon = PhotoImage(file='icons/italic.png')
		self.underline_icon = PhotoImage(file='icons/underline.png')
		self.strikethrough_icon = PhotoImage(file='icons/strikethrough.png')
		self.highlight_icon = PhotoImage(file='icons/highlight.png')
		self.fontfg_icon = PhotoImage(file='icons/fontfg.png')

		self.align_left_icon = PhotoImage(file='icons/align_left.png')
		self.align_center_icon = PhotoImage(file='icons/align_center.png')
		self.align_right_icon = PhotoImage(file='icons/align_right.png')

		self.shortcut_icon = PhotoImage(file='icons/shortcuts.png')
		self.search_icon = PhotoImage(file='icons/search.png')
		self.find_icon = PhotoImage(file='icons/find.png')
		self.find_replace_icon = PhotoImage(file='icons/find_replace.png')

		self.default_theme_icon = PhotoImage(file='icons/default.png')
		self.dark_theme_icon = PhotoImage(file='icons/dark.png')
		self.sunny_theme_icon = PhotoImage(file='icons/sunny.png')
		self.sunset_theme_icon = PhotoImage(file='icons/sunset.png')


	# widgets -----------------------------------------------------------------------------------

	def draw_menu(self):
		self.menu = tk.Menu(self)
		file_menu = tk.Menu(self.menu, tearoff=False)
		self.edit_menu = tk.Menu(self.menu, tearoff=False, postcommand=self.enable_selection)
		lambda_menu = tk.Menu(self.menu, tearoff=False)
		themes_menu = tk.Menu(self.menu, tearoff=False)
		help_menu = tk.Menu(self.menu, tearoff=False)

		# file_menu
		file_menu.add_command(label='New', accelerator='Ctrl+N', compound=tk.LEFT, image=self.new_icon, command=self.new_file)
		file_menu.add_command(label='Open', accelerator='Ctrl+O', compound=tk.LEFT, image=self.open_icon, command=self.open_file)
		file_menu.add_command(label='Save', accelerator='Ctrl+S', compound=tk.LEFT, image=self.save_icon, command=self.save_file)
		file_menu.add_command(label='Save As...', accelerator='Ctrl+Shift+S', compound=tk.LEFT, image=self.save_as_icon, command=self.save_as_file)
		file_menu.add_separator()
		file_menu.add_command(label='Print Page', accelerator='Ctrl+P', compound=tk.LEFT, image=self.print_icon, command=self.print_file)
		file_menu.add_separator()
		file_menu.add_command(label='Exit', accelerator='Ctrl+Q', compound=tk.LEFT, image=self.exit_icon,
							  command=self.quit)

		# edit_menu
		self.edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound=tk.LEFT, image=self.cut_icon, command=self.cut_text)
		self.edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound=tk.LEFT, image=self.copy_icon, command=self.copy_text)
		self.edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound=tk.LEFT, image=self.paste_icon, command=self.paste_text)
		self.edit_menu.add_command(label='Select All', accelerator='Ctrl+A', compound=tk.LEFT, image=self.select_all_icon, command=self.select_all)
		self.edit_menu.add_command(label='Clear All', accelerator='Delete', compound=tk.LEFT, image=self.clear_all_icon, command=self.clear_all)
		self.edit_menu.add_separator()
		self.edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound=tk.LEFT, image=self.undo_icon, command=self.undo)
		self.edit_menu.add_command(label='Redo', accelerator='Ctrl+Y', compound=tk.LEFT, image=self.redo_icon, command=self.redo)


		# functions_menu
		lambda_menu.add_command(label='Sum', compound=tk.LEFT, image=self.sum_icon, command=self.find_sum)
		lambda_menu.add_command(label='Avg', compound=tk.LEFT, image=self.avg_icon, command=self.find_average)
		lambda_menu.add_command(label='Count', compound=tk.LEFT, image=self.count_icon, command=self.count_occurence)
		lambda_menu.add_separator()
		lambda_menu.add_command(label='Find', accelerator='Ctrl+F', compound=tk.LEFT, image=self.find_icon, command=self.find)
		lambda_menu.add_command(label='Find & Replace', accelerator='Ctrl+H', compound=tk.LEFT, image=self.find_replace_icon, command=self.find_and_replace)
		lambda_menu.add_separator()
		lambda_menu.add_command(label='Time/Date', compound=tk.LEFT, image=self.datetime_icon, command=self.current_date_time)

		# themes menu
		themes_menu.add_command(label=' Default', compound=tk.LEFT, image=self.default_theme_icon, command=self.default_theme)
		themes_menu.add_command(label=' Dark', compound=tk.LEFT, image=self.dark_theme_icon, command=self.dark_theme)
		themes_menu.add_command(label=' Sunny', compound=tk.LEFT, image=self.sunny_theme_icon, command=self.sunny_theme)
		themes_menu.add_command(label=' Sunset', compound=tk.LEFT, image=self.sunset_theme_icon, command=self.sunset_theme)

		# help_menu
		help_menu.add_command(label='Help on Coastline', compound=tk.LEFT, image=self.help_icon, command=get_help)
		help_menu.add_command(label='Shortcut Keys', compound=tk.LEFT, image=self.shortcut_icon, command=show_shortcuts)
		help_menu.add_command(label='About Coastline', compound=tk.LEFT, image=self.coastline_icon, command=show_about)

		self.menu.add_cascade(label='File', menu=file_menu)
		self.menu.add_cascade(label='Edit', menu=self.edit_menu)
		self.menu.add_cascade(label='Lambda', menu=lambda_menu)
		self.menu.add_command(label='Regex', command=self.find_regex)
		self.menu.add_cascade(label='Themes', menu=themes_menu)
		self.menu.add_cascade(label='Help', menu=help_menu)
		self.config(menu=self.menu)

		self.context_menu = tk.Menu(self, tearoff=0, postcommand=self.enable_selection)
		self.context_menu.add_command(label='Cut', command=self.cut_text)
		self.context_menu.add_command(label='Copy', command=self.copy_text)
		self.context_menu.add_command(label='Paste', command=self.paste_text)
		self.context_menu.add_command(label='Delete', command=self.clear_all)
		self.context_menu.add_command(label='Select All', command=self.select_all)
		self.context_menu.add_separator()
		self.context_menu.add_command(label='Undo', command=self.undo)
		self.context_menu.add_command(label='Redo', command=self.redo)

	def draw_frames(self):
		self.ribbon = tk.Frame(self, height=40, bg='gray98')
		self.ribbon.grid(row=0, column=0, columnspan=2, sticky='WENS')
		self.ribbon.grid_propagate(False)

		self.ribbon.grid_columnconfigure(0,weight=0)
		self.ribbon.grid_columnconfigure(1,weight=0)
		self.ribbon.grid_columnconfigure(2,weight=0)
		self.ribbon.grid_columnconfigure(3,weight=1)

		self.font_box = tk.Frame(self.ribbon, width=350, height=40, bg='gray95')
		self.font_box.grid(row=0, column=0, sticky='W', padx=2)
		self.font_box.grid_propagate(False)

		self.style_box = tk.Frame(self.ribbon, width=220, height=40, bg='gray95')
		self.style_box.grid(row=0, column=1, sticky='W', padx=3)
		self.style_box.grid_propagate(False)

		self.align_box = tk.Frame(self.ribbon, width=120, height=40, bg='gray95')
		self.align_box.grid(row=0, column=2, sticky='W', padx=2)
		self.align_box.grid_propagate(False)

		self.search_box = tk.Frame(self.ribbon, height=40, bg='gray95')
		self.search_box.grid(row=0, column=3, sticky='WE')
		self.search_box.grid_propagate(False)

		self.search_box.columnconfigure(0, weight=1)
		self.search_box.columnconfigure(1, weight=0)
		self.search_box.columnconfigure(2, weight=0)

		# Textbox

		self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL)

		self.textbox = tk.Text(self, yscrollcommand=self.scroll.set, relief=tk.FLAT,
						font=(self.font_family.get(), self.font_size.get()), wrap='word',
						undo=True, autoseparators=True, maxundo=-1)
		self.textbox.focus_set()
		self.textbox.grid(row=1, column=0, sticky='WENS')
		
		self.scroll.config(command=self.textbox.yview)
		self.scroll.grid(row=1, column=1, sticky='NS', padx=0)

		# Statusbar

		self.status = tk.Label(self, bg='gray70', height=1, anchor='w')
		self.status.grid(row=2, column=0, columnspan=2, sticky='WE')

	def draw_widgets(self):
		self.font_tuple = tk.font.families()
		self.font_combo = ttk.Combobox(self.font_box, width=28, textvariable=self.font_family, state='readonly')
		self.font_combo['values'] = self.font_tuple
		self.font_combo.current(self.font_tuple.index(self.font_family.get()))
		self.font_combo.grid(row=0, column=0, padx=2, pady=8)

		self.size_tuple = tuple(range(8,80,4))
		self.size_combo = ttk.Combobox(self.font_box, width=20, textvariable=self.font_size, state='readonly')
		self.size_combo['values'] = self.size_tuple
		self.size_combo.current(self.size_tuple.index(self.font_size.get()))
		self.size_combo.grid(row=0, column=1, padx=5, pady=8)

		self.bold = CustomButton(self.style_box, image=self.bold_icon, 
								command=lambda : self.configure_text('bold'))
		self.bold.grid(row=0, column=0, sticky='W', padx=2, pady=3)

		self.italic = CustomButton(self.style_box, image=self.italic_icon, 
								command=lambda : self.configure_text('italic'))
		self.italic.grid(row=0, column=1, sticky='W', padx=2, pady=3)

		self.underline = CustomButton(self.style_box, image=self.underline_icon, 
								command=lambda : self.configure_text('underline'))
		self.underline.grid(row=0, column=2, sticky='W', padx=2, pady=3)

		self.strikethrough = CustomButton(self.style_box, image=self.strikethrough_icon,
								command=lambda : self.configure_text('strikethrough'))
		self.strikethrough.grid(row=0, column=3, sticky='W', padx=2, pady=3)

		self.highlight = CustomButton(self.style_box, image=self.highlight_icon,
								command=lambda : self.configure_text('highlight'))
		self.highlight.grid(row=0, column=4, sticky='W', padx=2, pady=3)

		self.fontfg = tk.Button(self.style_box, image=self.fontfg_icon, command=self.change_color,
					 relief=tk.FLAT, cursor='hand2', bg='white',)
		self.fontfg.grid(row=0, column=5, sticky='W', padx=2, pady=3)

		self.align_left = CustomButton(self.align_box, image=self.align_left_icon, command=lambda : self.align_text('left'))
		self.align_left.grid(row=0, column=1, sticky='W', padx=(8,2), pady=3)

		self.align_center = CustomButton(self.align_box, image=self.align_center_icon, command=lambda : self.align_text('center'))
		self.align_center.grid(row=0, column=2, sticky='W', padx=2, pady=3)

		self.align_right = CustomButton(self.align_box, image=self.align_right_icon, command=lambda : self.align_text('right'))
		self.align_right.grid(row=0, column=3, sticky='W', padx=2, pady=3)

		self.search_entry = tk.Entry(self.search_box, bg='gray92', textvariable=self.search_term)
		self.search_entry.grid(row=0, column=1, pady=10, padx=10)

		self.submit = tk.Button(self.search_box, image=self.search_icon, bg='gray95', relief=tk.FLAT,
								command=self.find_text)
		self.submit.grid(row=0, column=2, padx=5)

	def add_bindings(self):
		self.textbox.bind("<Up>",  lambda event: self.textbox.yview_scroll( -3, "units"))
		self.textbox.bind("<Down>",  lambda event: self.textbox.yview_scroll( 3, "units"))
		self.textbox.bind('<KeyPress>', self._on_keyboard_input)
		self.textbox.bind('<KeyRelease>', self._on_keyboard_input)
		self.textbox.bind('<Button-3>', self.show_popup)

	def set_tracing(self):
		self.font_family.trace_add('write', self.change_font)
		self.font_size.trace_add('write', self.change_font)

	def set_tags(self):
		self.textbox.tag_configure('bold', font=(self.font_family.get(), 22, 'bold'))
		self.textbox.tag_configure('italic', font=(self.font_family.get(), self.font_size.get(), 'italic'))
		self.textbox.tag_configure('underline', underline=1)
		self.textbox.tag_configure('strikethrough', overstrike=1)
		self.textbox.tag_configure('highlight', background='yellow')
		self.textbox.tag_configure('left', justify = tk.LEFT)
		self.textbox.tag_configure('center', justify = tk.CENTER)
		self.textbox.tag_configure('right', justify = tk.RIGHT)
		self.textbox.tag_configure('find', foreground='red')
		self.textbox.tag_configure('regex', foreground='red')

	def create_dictionaries(self):
		self.alignments = {
			'left' : self.align_left,
			'center' : self.align_center,
			'right' : self.align_right
		}

		self.styles = {
			'bold' : self.bold,
			'italic' : self.italic,
			'underline' : self.underline,
			'strikethrough' : self.strikethrough,
			'highlight' : self.highlight
		}

	# functions --------------------------------------------------------------------------------

	def toggleFullScreen(self, event):
		if self.isFullscreen == False:
			self.isFullscreen = True
			self.state('zoomed')

	def quitFullScreen(self, event):
		if self.isFullscreen == True:
			self.isFullscreen = False
			self.state('normal')

	def _on_keyboard_input(self, event=None):
		string = self.textbox.get('1.0', 'end-1c')
		new_line_less = string.replace('\n', ' ')
		characters = len(string)
		words = len(new_line_less.split())
		self.status['text'] = f'Characters : {characters} Words : {words}'

		if characters != self.initial_len:
			self.textbox_modified()
			self.initial_len = characters
	
	def change_font(self, var, indx, mode):
		self.textbox.configure(font=(self.font_family.get(), self.font_size.get()))

		self.align_text(self.align)

		if self.boldOn:
			self.configure_text('bold')
		if self.italicOn:
			self.configure_text('italic')
		if self.underlineOn:
			self.configure_text('underline')
		if self.overstrikeOn:
			self.configure_text('strikethrough')

	def change_font_style(self, type):
		self.textbox.configure(font=(self.font_family.get(), self.font_size.get(), type))

	def change_color(self):
		color = colorchooser.askcolor()[1]
		self.textbox['fg'] = color

	def delete_content(self):
		self.textbox.delete('1.0', tk.END)

	def configure_text(self, tag):
		selection = self.textbox.tag_ranges(tk.SEL)
		if selection:
			current_tags = self.textbox.tag_names("sel.first")
			if tag == 'bold':
				self.textbox.tag_configure('bold', font=(self.font_family.get(), self.font_size.get(), 'bold'))
			if tag == 'italic':
				self.textbox.tag_configure('italic', font=(self.font_family.get(), self.font_size.get(), 'italic'))

			if tag in current_tags:
				self.textbox.tag_remove(tag, "sel.first", "sel.last")
			else:
				self.textbox.tag_add(tag, "sel.first", "sel.last")
		else:
			text_property = tk.font.Font(font = self.textbox['font'])
			if tag == 'bold':
				if text_property.actual()['weight'] =='normal':
					self.change_font_style('bold')
					self.boldOn = True
					self.bold['bg'] = 'cyan3'
				if text_property.actual()['weight'] =='bold':
					self.change_font_style('normal')
					self.boldOn = False
					self.bold['bg'] = 'white'
			elif tag == 'italic':
				if text_property.actual()['slant'] =='roman':
					self.change_font_style('italic')
					self.italicOn = True
					self.italic['bg'] = 'cyan3'
				if text_property.actual()['slant'] =='italic':
					self.change_font_style('roman')
					self.italicOn = False
					self.italic['bg'] = 'white'
			elif tag == 'underline':
				if text_property.actual()['underline'] ==0:
					self.change_font_style('underline')
					self.underlineOn = True
					self.underline['bg'] = 'cyan3'
				if text_property.actual()['underline'] ==1:
					self.change_font_style('normal')
					self.underlineOn = False
					self.underline['bg'] = 'white'
			elif tag == 'strikethrough':
				if text_property.actual()['overstrike'] ==0:
					self.change_font_style('overstrike')
					self.overstrikeOn = True
					self.strikethrough['bg'] = 'cyan3'
				if text_property.actual()['overstrike'] ==1:
					self.change_font_style('normal')
					self.overstrikeOn = False
					self.strikethrough['bg'] = 'white'

	def align_text(self, align):
		self.align = align

		alignments = self.alignments.copy()
		alignment = alignments.get(align)
		alignment['bg'] = 'cyan3'
		del alignments[align]
		for key in alignments:
			alignments[key].configure(bg='white')

		content = self.textbox.get(1.0, 'end')
		self.textbox.delete(1.0, tk.END)
		self.textbox.insert(tk.INSERT, content, align)
		self.remove_find_tag()

	def textbox_modified(self, event=None):
		self.file_is_saved = False
		self.change_wm_title()

	def change_wm_title(self, event=None):	
		if self.file_is_saved:
			self.filename = self.filename.strip('*')
		else:
			if not self.filename.startswith('*'):
				self.filename = '*' + self.filename

		self.title(self.filename + ' - Coastline')

	def new_file(self, event=None):
		self.file_is_saved = False
		self.filename = '*untitled'
		self.filepath = ''
		self.initial_len = 0
		self.delete_content()
		self.textbox_modified()

	def open_file(self, event=None):
		self.filepath = filedialog.askopenfilename(initialdir=cwd, filetypes=(("Text","*.txt"), ))
		self.filename = os.path.basename(self.filepath)
		if self.filepath:
			self.delete_content()
			with open(self.filepath) as file:
				content = file.read()
				self.textbox.insert(tk.END, content)

				self.file_is_saved = True
				self.initial_len = len(content)
				self.change_wm_title()

			self._on_keyboard_input()

	def save_file(self, event=None):
		content = self.textbox.get('1.0','end-1c')
		if content:
			if self.filepath:
				with open(self.filepath, 'w', encoding = "utf-8") as file:
					file.write(content)
					self.file_is_saved = True
					self.change_wm_title()
			else:
				self.save_as_file()
		else:
			messagebox.showerror('Coastline', 'Empty content')

	def save_as_file(self, event=None):
		content = self.textbox.get('1.0','end-1c')
		if content:
			self.filepath = filedialog.asksaveasfilename(initialdir=cwd, filetypes = (('Text Files', '*.txt'),),
												defaultextension='.txt')
			if self.filepath:
				self.filename = os.path.basename(self.filepath)
				with open(self.filepath, 'w', encoding = "utf-8") as file:
					file.write(content)

				self.file_is_saved = True
				self.change_wm_title()
		else:
			messagebox.showerror('Coastline', 'Empty content')

	def print_file(self, event=None):
		content = self.textbox.get('1.0','end-1c')
		if content:
			filename = 'Coastline.txt'
			with open(filename, "w") as file:
				file.write(content)
			win32api.ShellExecute(0,"print",filename,'"%s"' % win32print.GetDefaultPrinter (),
					".",0)

	def enable_selection(self):
		state_selection = tk.ACTIVE if self.textbox.tag_ranges(tk.SEL) else tk.DISABLED
		state_clipboard = tk.ACTIVE

		try:
			self.clipboard_get()
		except tk.TclError:
			state_clipboard = tk.DISABLED

		self.context_menu.entryconfig(0, state=state_selection) # Cut
		self.context_menu.entryconfig(1, state=state_selection) # Copy
		self.context_menu.entryconfig(2, state=state_clipboard) # Paste
		self.context_menu.entryconfig(3, state=state_selection) # Delete

		self.edit_menu.entryconfig(0, state=state_selection) # Cut
		self.edit_menu.entryconfig(1, state=state_selection) # Copy
		self.edit_menu.entryconfig(2, state=state_clipboard) # Paste
		self.edit_menu.entryconfig(4, state=state_selection) # Delete

	def show_popup(self, event):
		self.context_menu.post(event.x_root, event.y_root)

	def copy_text(self, event=None):
		self.textbox.event_generate("<<Copy>>")
		self._on_keyboard_input()

	def cut_text(self, event=None):
		self.textbox.event_generate("<<Cut>>")
		self._on_keyboard_input()

	def paste_text(self, event=None):
		self.textbox.event_generate("<<Paste>>")
		self._on_keyboard_input()

	def select_all(self, event=None):
		self.textbox.event_generate("<<SelectAll>>")
		self._on_keyboard_input()

	def clear_all(self, event=None):
		self.textbox.event_generate("<<Clear>>")
		self._on_keyboard_input()

	def undo(self, event=None):
		try:
			self.textbox.edit_undo()
			self._on_keyboard_input()
		except:
			pass

	def redo(self, event=None):
		try:
			self.textbox.edit_redo()
			self._on_keyboard_input()
		except:
			pass

	def remove_find_tag(self):
		self.textbox.tag_remove('find', '1.0', tk.END)
		self.textbox.tag_remove('regex', '1.0', tk.END)
		self.search_entry.delete(0, tk.END)
		self.submit.configure(image=self.search_icon)
		self.submit.configure(command=self.find_text)

	def find(self, event=None):
		text = tkinter.simpledialog.askstring('Coastline', 'Enter text to find')
		if text:
			self.find_from_menu = True
			self.search_entry.delete(0, tk.END)
			self.search_entry.insert(tk.END, text)
			self.find_text(text)

	def find_text(self, text=None):
		self.textbox.tag_remove('find', '1.0', tk.END)
		if not self.find_from_menu:
			text = self.search_entry.get()
		if text:
			current_index = '1.0'
			while True:
				current_index = self.textbox.search(text, current_index, nocase=1, stopindex=tk.END)
				if not current_index:
					break
				last_index = '% s+% dc' % (current_index, len(text))
				self.textbox.tag_add('find', current_index, last_index)
				current_index = last_index

			self.submit.configure(image=self.exit_icon)
			self.submit.configure(command=self.remove_find_tag)
			self.find_from_menu = False

	def find_regex(self, event=None):
		regex = tkinter.simpledialog.askstring('Coastline', 'Enter regular expression\nto find')
		if regex:
			regex = regex.lstrip("r'").rstrip("'")
			string = self.textbox.get('1.0', 'end-1c')
			self.search_entry.delete(0, tk.END)
			self.search_entry.insert(tk.END, regex)

			lst = re.findall(fr'{regex}', string)
			i = 0
			current_index = '1.0'
			while True:
				current_index = self.textbox.search(fr'{regex}', current_index, nocase=1, stopindex=tk.END, regexp=True)
				if not current_index:
					break
				last_index = '% s+% dc' % (current_index, len(lst[i]))
				i += 1
				self.textbox.tag_add('regex', current_index, last_index)
				current_index = last_index

			self.submit.configure(image=self.exit_icon)
			self.submit.configure(command=self.remove_find_tag)
			messagebox.showinfo('Coastline', f'{len(lst)} matches found')

	def find_and_replace(self, event=None):
		find_text, replace_text = find_and_replace_window()
		if find_text and replace_text:
			current_index = '1.0'
			while True:
				current_index = self.textbox.search(find_text, current_index, nocase=1,
									stopindex=tk.END)
				if not current_index:
					break
				last_index = '% s+% dc' % (current_index, len(find_text))
				self.textbox.delete(current_index, last_index)
				self.textbox.insert(current_index, replace_text)

				last_index = '% s+% dc' % (current_index, len(replace_text))
				current_index = last_index

	def current_date_time(self):
		dt = datetime.datetime.now()
		self.textbox.insert('insert',dt.strftime('%b %d, %Y %I:%M %p'))

	def find_integers(self):
		regex = re.compile(r'\d+')
		string = self.textbox.get('1.0', 'end-1c')
		nums = re.findall(regex, string)
		return nums
	
	def find_sum(self):
		nums = self.find_integers()
		if nums:
			sum_total = sum(int(num) for num in nums)
			messagebox.showinfo('Coastline', f'Sum of {len(nums)} numbers\nfound is {sum_total}')
		else:
			messagebox.showinfo('Coastline', 'No number found')

	def find_average(self):
		nums = self.find_integers()
		if nums:
			sum_total = sum(int(num) for num in nums)
			avg = sum_total / len(nums)
			messagebox.showinfo('Coastline', f'Average of {len(nums)} numbers\nfound is {avg}')
		else:
			messagebox.showinfo('Coastline', 'No number found')

	def count_occurence(self):
		term = tkinter.simpledialog.askstring('Coastline', 'Enter term to count\nits occurence')
		if term:
			regex = re.compile(term)
			string = self.textbox.get('1.0', 'end-1c')
			nums = re.findall(regex, string)
			if nums:
				messagebox.showinfo('Coastline', f'{term} occurs {len(nums)} times in the string')
			else:
				messagebox.showinfo('Coastline', 'No occurence found')

	def default_theme(self):
		self.textbox['bg'] = 'white'
		self.textbox['fg'] ='black'
		self.textbox['insertbackground'] = 'black'
		self.status['bg'] = 'gray70'
		self.status['fg'] = 'black'

	def dark_theme(self):
		self.textbox['bg'] = 'gray12'
		self.textbox['fg'] = 'white'
		self.textbox['insertbackground'] = 'white'
		self.status['bg'] = 'gray20'
		self.status['fg'] = 'snow'

	def sunny_theme(self):
		self.textbox['bg'] = 'SkyBlue1'
		self.textbox['fg'] = 'blue4'
		self.textbox['insertbackground'] = 'blue2'
		self.status['bg'] = 'LightSkyBlue3'
		self.status['fg'] = 'dark green'

	def sunset_theme(self):
		self.textbox['bg'] = 'coral1'
		self.textbox['fg'] = 'white'
		self.textbox['insertbackground'] = 'white'
		self.status['bg'] = 'sienna1'
		self.status['fg'] = 'white'


# def custom functions --------------------------------------------------------------------

def find_and_replace_window():
		win = tk.Toplevel()
		win.wm_title('Coastline')
		win.geometry('230x110+150+150')
		win.iconbitmap('icons/coastline.ico')
		win.wm_resizable(0,0)

		find = tk.StringVar()
		replace = tk.StringVar()

		l1 = tk.Label(win, text='Find text', anchor='e')
		e1 = tk.Entry(win, textvariable=find)
		l2 = tk.Label(win, text='Replace with', anchor='e')
		e2 = tk.Entry(win, textvariable=replace)
		btn = tk.Button(win, text='Find and Replace', bg='DodgerBlue2', command=win.destroy)

		l1.grid(row=0, column=0, padx=5, pady=5)
		e1.grid(row=0, column=1, padx=5, pady=5)
		l2.grid(row=1, column=0, padx=5, pady=5)
		e2.grid(row=1, column=1, padx=5, pady=5)
		btn.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
		
		e1.focus_set()
		win.wait_window()
		return find.get(), replace.get()

def show_about():
	win = tk.Toplevel()
	win.wm_title('Coastline')
	win.iconbitmap('icons/coastline.ico')
	win.wm_resizable(0,0)

	label = tk.Label(win, text='Coastline - A modern day text Editor', fg='red',
				font=('Calibri', 12))
	label.grid(row=0, column=0)
	text = tk.Text(win, width=30, height=4)
	text.insert(tk.END, 'Author : Prajjwal Pathak \n')
	text.insert(tk.END, 'Version : 1.0.01 \n')
	text.insert(tk.END, 'Build : 1107')
	text.grid(row=1, column=0)
	text.configure(state='disabled')

def show_shortcuts():
	with open('files/shortcuts.txt') as file:
			shortcuts = file.readlines()

	win = tk.Toplevel()
	win.wm_title('Coastline')
	win.iconbitmap('icons/coastline.ico')
	win.wm_resizable(0,0)

	header = tk.Label(win, text='Shortcut keys for Coastline')
	header.grid(row=0, column=0, columnspan=2)
	for row in range(len(shortcuts)):
		short = shortcuts[row].strip('*').split(':')
		key = tk.Label(win, text=short[0].strip(), anchor='e')
		key.grid(row=row+1, column=0)
		func = tk.Label(win, text=short[1].strip(), anchor='w')
		func.grid(row=row+1, column=1)

def get_help():
	url = 'https://github.com/pyGuru123/Python-Projects/blob/master/Coastline%20-%20Text%20Editor/readme.md'
	webbrowser.open(url)

if __name__ == '__main__':
	app = TextEditor()
	app.title('Coastline - Text Editor')
	app.geometry('1000x640+5+5')
	app.iconbitmap('icons/coastline.ico')
	app.mainloop()