import tkinter as tk

class CustomButton(tk.Button):
	def __init__(self, parent, *args, **kwargs):
		tk.Button.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		width = kwargs.get('width', 15)
		height = kwargs.get('height', 2)
		font = kwargs.get('font', ('TkDefaultFont', 11))
		anchor= kwargs.get('anchor','w')

		self.configure(bg='gray18', fg='white', relief=tk.FLAT, borderwidth=1,
						width=width, height=height, compound=tk.LEFT, anchor=anchor, 
						font=font, cursor='hand2')
		self.bind('<Enter>', self.on_enter)
		self.bind('<Leave>', self.on_leave)

	def on_enter(self, event):
		self.configure(bg='gray15', font=('TkDefaultFont', 12) )

	def on_leave(self, event):
		self.configure(bg='gray18', font=('TkDefaultFont', 11))

class RecentButton(tk.Button):
	def __init__(self, parent, *args, **kwargs):
		tk.Button.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.configure(bg='gray19', fg='white', relief=tk.FLAT, borderwidth=1,
						width=30, height=2, compound=tk.LEFT, anchor='w', 
						font=('TkDefaultFont', 9), cursor='hand2')
		self.bind('<Enter>', self.on_enter)
		self.bind('<Leave>', self.on_leave)

	def on_enter(self, event):
		self.configure(bg='gray15', font=('TkDefaultFont', 10), width=31 )

	def on_leave(self, event):
		self.configure(bg='gray19', font=('TkDefaultFont', 9), width=30) 
		
class CustomLabel(tk.Label):
	def __init__(self, parent, *args, **kwargs):
		tk.Label.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		text = kwargs['text']

		anchor = kwargs.get('anchor', 'w')
		width = kwargs.get('width', 30)
		height = kwargs.get('height', 1)
		bg = kwargs.get('bg', 'gray18')
		self.configure(width=width, height=height, bg=bg, fg='white', anchor=anchor, text=text,
						font=('TkDefaultFont', 10))

class CustomFrame(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		bg = kwargs.get('bg', 'gray18')

		self.configure(bg=bg, highlightthickness=0.5, highlightbackground='gray16')
		self.grid_propagate(0)