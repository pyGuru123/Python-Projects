#! python3
"""
@created: 2020-10-12 07:36:35
@author: Prajjwal Pathak ( pyGuru )

Covid Tracker

-------------------------------------------------------------------------------
Dependencies:

* Requests, BeautifulSoup4, Pandas and Matplotlib

-------------------------------------------------------------------------------
Description : 
Covid Tracker is a python tkinter based covid tracking application which can give
you covid stats from all around the world.
"""

import os, sys
import shelve
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox

from covid_scraper import todays_date, scrape_data

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()

		self.var = tk.StringVar()
		self.plot_type = 'bar'
		self.plot_active = True

		self.create_frames()
		self.update_widgets()
		self.chart_type_widgets()
		self.searchbar_widgets()
		self.controls_widgets()
		self.graph_widgets()

		self.master.bind('<Return>', self.searchData)

	def create_frames(self):
		self.updates = tk.LabelFrame(self, text='Updates', 
					font=("times new roman",15,"bold"),
					bg="slate gray",fg="white",bd=5,relief=tk.GROOVE)
		self.updates.config(width=700,height=100)
		self.updates.grid(row=0, column=0, columnspan=5)

		self.chart_type = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",fg="white", bd=0)
		self.chart_type.config(width=190,height=50)
		self.chart_type.grid(row=1, column=0, pady=5)

		self.searchbar = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",fg="white")
		self.searchbar.config(width=500,height=70)
		self.searchbar.grid(row=1, column=1, pady=5, columnspan=5)

		self.controls = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="salmon1",fg="white",bd=5)
		self.controls.config(width=190,height=405)
		self.controls.grid(row=2, column=0, pady=10, rowspan=2)

		self.graph = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",fg="white",bd=5,relief=tk.GROOVE)
		self.graph.config(width=260,height=400)
		self.graph.grid(row=2, column=1, columnspan=5, padx=10)


	def update_widgets(self):
		self.total = tk.Label(self.updates, font=("times new roman",16,"bold"),
						bg="brown2",fg="white")
		self.total.config(width=11, height=2, padx=2)
		self.total.grid(row=0, column=0)

		self.active = tk.Label(self.updates, font=("times new roman",16,"bold"),
						bg="dodger blue",fg="white")
		self.active.config(width=11, height=2, padx=5)
		self.active.grid(row=0, column=1)

		self.recovered = tk.Label(self.updates, font=("times new roman",16,"bold"),
						bg="forest green",fg="white")
		self.recovered.config(width=11, height=2, padx=5)
		self.recovered.grid(row=0, column=2)

		self.deaths = tk.Label(self.updates, font=("times new roman",16,"bold"),
						bg="red3",fg="white")
		self.deaths.config(width=11, height=2, padx=5)
		self.deaths.grid(row=0, column=3)

		self.todays = tk.Label(self.updates, font=("times new roman",16,"bold"),
						bg="DarkOrange2",fg="white")
		self.todays.config(width=12, height=2, padx=8)
		self.todays.grid(row=0, column=4)

		self.get_world_info()

	def chart_type_widgets(self):
		self.bar = tk.Button(self.chart_type, bg='blue', fg='white', font=10)
		self.bar['text'] = 'Bar'
		self.bar['command'] = self.bar_chart
		self.bar.config(width=5, height=1)
		self.bar.grid(row=0, column=0, pady=4, padx=15)

		self.pie = tk.Button(self.chart_type, bg='green', fg='white', font=10)
		self.pie['text'] = 'Pie'
		self.pie['command'] = self.pie_chart
		self.pie.config(width=5, height=1)
		self.pie.grid(row=0, column=1, pady=4, padx=15)

	def searchbar_widgets(self):
		self.searchtext = tk.Label(self.searchbar, text='Country name',
			font=("times new roman",10,"bold"))
		self.searchtext.grid(row=0, column=0)
		self.cname = tk.Entry(self.searchbar)
		self.cname['textvariable'] = self.var
		self.cname.config(width=40)
		self.cname.grid(row=0, column=1, padx=(5,25))

		self.search = tk.Button(self.searchbar, bg='green', fg='white', font=10)
		self.search['text'] = 'Search'
		self.search['command'] = self.searchData
		self.search.config(width=12)
		self.search.grid(row=0, column=2, padx=(0,5))

	def controls_widgets(self):
		self.info = tk.Label(self.controls, image=virus)
		self.info.grid(row=0, column=0, pady=8, columnspan=2)

		self.date = tk.Label(self.controls, font=("times new roman",16,"bold"),
						bg="salmon1",fg="white")
		self.date['text'] = f'Covid-19 \n Stats Tracker \n {todays_date()}'
		self.date.config(width=12, height=3, padx=12)
		self.date.grid(row=1, column=0, columnspan=2)

		self.refresh = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.refresh['text'] = 'Refresh'
		self.refresh['command'] = self.refresh_stats
		self.refresh.config(width=12, height=1)
		self.refresh.grid(row=2, column=0, pady=8, columnspan=2)

		self.world = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.world['text'] = 'World'
		self.world['command'] = self.get_world_info
		self.world.config(width=12, height=1)
		self.world.grid(row=3, column=0, pady=8, columnspan=2)

		self.top10 = tk.Button(self.controls, bg='green', fg='white', font=10)
		self.top10['text'] = 'Top 10'
		self.top10['command'] = self.top_ten_countries
		self.top10.config(width=12, height=1)
		self.top10.grid(row=4, column=0, pady=8, columnspan=2)

	def graph_widgets(self):
		self.canvas = tk.Canvas(self.graph)

		self.figure = Figure(figsize=(5.6, 4), dpi=100)
		self.can = FigureCanvasTkAgg(self.figure, self.canvas)
		self.can.get_tk_widget().grid(row=0, column=0, padx=10)

	def change_label_data(self):
		self.total['text'] = f'Total Cases\n {self.data[0]}'
		self.active['text'] = f'Active \n {self.data[1]}'
		self.recovered['text'] = f'Recovered \n {self.data[2]}'
		self.deaths['text'] = f'Deaths \n {self.data[3]}'
		self.todays['text'] = f'Today \n {self.data[4]}'

	def get_world_info(self):
		self.data = get_world()
		self.var.set('')
		self.change_label_data()
		self.plot_graph(self.plot_type)

	def searchData(self, event=None):
		self.value = self.var.get()
		if self.value == '':
			print('Enter country name first')
		else:
			if self.value.upper() in ['USA', 'UK', 'UAE', 'CAR']:
				self.data = get_country(self.value.upper())
			else:
				self.data = get_country(self.value.capitalize())
			if self.data is not None:
				self.change_label_data()
				self.plot_graph(self.plot_type)

	def refresh_stats(self):
		ret = scrape_data()
		if ret is None:
			messagebox.showerror('no internet', 'No internet connection')
		else:
			read_stats_file()
			self.get_world_info()

	def top_ten_countries(self):
		self.data, self.table = top10()
		self.var.set('')
		self.change_label_data()
		self.create_table()

	def plot_graph(self, plt_type):
		if self.plot_active is False:
			self.delete_graph()
			self.plot_active = True
			cname = 'Top 10 Countries'
		else:
			if self.var.get() == '':
				cname = 'World'
			else:
				cname = self.var.get()
		self.figure = get_plot(self.data, cname, plt_type)

		self.can = FigureCanvasTkAgg(self.figure, self.graph)
		self.can.get_tk_widget().grid(row=0, column=0, padx=10)

	def bar_chart(self):
		self.plot_type = 'bar'
		self.bar['bg'] = 'blue'
		self.pie['bg'] = 'green'
		self.plot_graph(self.plot_type)

	def pie_chart(self):
		self.plot_type = 'pie'
		self.pie['bg'] = 'blue'
		self.bar['bg'] = 'green'
		self.plot_graph(self.plot_type)

	def create_table(self):
		self.delete_graph()
		self.plot_active = False

		total_rows, total_columns = len(self.table), len(self.table[0])
		for i in range(total_rows): 
			for j in range(total_columns):   
				self.e = tk.Text(self.graph) 
				if i == 0:
					self.e['fg'] = 'brown'
					self.e['font'] =('Arial',10,'bold')
				else:
					self.e['fg'] = 'blue'
					self.e['font'] = ('Arial',9,'bold')
				self.e.config(width=10, height=2)
				self.e.grid(row=i, column=j) 
				self.e.insert(tk.END, self.table[i][j])

	def delete_graph(self):
		self.graph.destroy()
		self.graph = tk.LabelFrame(self, text='', 
					font=("times new roman",15,"bold"),
					bg="white",fg="white",bd=5,relief=tk.GROOVE)
		self.graph.config(width=260,height=400)
		self.graph.grid(row=2, column=1, columnspan=5, padx=10)

def download_csv():
	print('Fetching data from internet .....')
	ret = scrape_data()
	if ret is None:
		root.withdraw()
		messagebox.showerror('no internet', 'Connect with internet \nand run the app again')
		sys.exit(0)

if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('750x550')
	root.wm_title('Covid Tracker')

	shelf_file = 'files/date.dat'

	if not os.path.exists(shelf_file):
		date = todays_date()
		with shelve.open(shelf_file) as file:
			file['date'] = date

	with shelve.open(shelf_file) as file:
		date = todays_date()
		if file['date'] != date:
			print(f'Fetching Covid data for {date}')
			download_csv()
			file['date'] = date

	if not os.path.exists('files/corona-cases.csv'):
		download_csv()

	from covid_analyser import get_world, top10, get_country, read_stats_file
	from covid_visualizer import get_plot 

	virus = PhotoImage(file='files/virus.gif')

	app = Application(master=root)
	app.mainloop()