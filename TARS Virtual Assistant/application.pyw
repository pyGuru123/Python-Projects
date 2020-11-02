#! python3
"""
@created: 2020-09-25 07:36:35
@author: Prajjwal Pathak ( pyGuru )

TARS Virtual Assistant

-------------------------------------------------------------------------------
Dependencies:

* requests, beautifulsoup4, pillow, speechrecognition, pypiwin32, pyaudio

-------------------------------------------------------------------------------
Description : 
TARS Virtual Assistant is a simple python tkinter based virtual assistant 
application which can do quick google searches for you, along with retrieving
images, telling you a joke, random facts, give meanings of words
"""

import re
import services
import tkinter as tk
from time import sleep
from tkinter import PhotoImage

import speech_recognition as sr 
from win32com.client import constants, Dispatch

r = sr.Recognizer()
mic = sr.Microphone(device_index=1)
speaker = Dispatch("SAPI.SpVoice")

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master=master)
		self.master = master
		self.pack()

		self.response = ''
		self.initialized = True

		self.main_frame()

	def main_frame(self):
		self.scroll = tk.Scrollbar(self, orient = tk.VERTICAL)
		self.scroll.grid(row=0, column=4, sticky='ns', padx=0)

		self.output = tk.Text(self, fg='blue')
		if self.initialized:
			self.output.insert(tk.END, f"Hello {services.get_name('user')}\n")
			self.output.insert(tk.END, f'Execute --help to get help')
			self.initialized = False
		self.output.configure(width=34, height=19, state='disabled')
		self.output.grid(row=0, column=0, columnspan=3)

		self.output.config(yscrollcommand=self.scroll.set)
		self.output.bind("<Up>",  lambda event: self.output.yview_scroll( -3, "units"))
		self.output.bind("<Down>",  lambda event: self.output.yview_scroll( 3, "units"))
		self.scroll.config(command = self.output.yview)

		self.input = tk.Label(self, fg='green', anchor='e')
		self.input.configure(width=35)
		self.input.grid(row=1, column=0, columnspan=3, pady=(10,0))

		self.msg_box = tk.Text(self)
		self.msg_box.focus()
		self.msg_box.configure(width=25, height=2)
		self.msg_box.bind('<Return>', lambda x : self.send_message())
		self.msg_box.grid(row=2, column=0, pady=(15,2), padx=(5,0))

		self.enter = tk.Button(self, image=send)
		self.enter['command'] = self.send_message
		self.enter.grid(row=2, column=1, pady=(15,2), padx=(5,1))

		self.voice = tk.Button(self, image=voice_search)
		self.voice['command'] = self.voice_message
		self.voice.grid(row=2, column=2, pady=(15,2))

	def send_message(self):
		self.query = self.msg_box.get('1.0', tk.END).strip('\n').lower()
		self.msg_box.delete(1.0, tk.END)
		self.get_result()
		self.text2speech()

	def voice_message(self):
		try:
			with mic as source:
				audio = r.listen(source)

			self.query = r.recognize_google(audio)
			self.input['text'] = self.query
			self.get_result()
		except:
			self.output.configure(state='normal')
			self.clear_output()
			self.output.insert('1.0', 'No internet connection')
			self.output.configure(state='disabled')
		self.text2speech()

	def text2speech(self):
		self.msg = self.output.get(1.0, tk.END).strip('\n')
		if (self.msg != '' and not self.msg.startswith('*-----')):
			speaker.speak(self.msg[:200])

	def get_result(self):
		# details
		my_name = re.compile(r'my name|who am i', re.I)
		your_name = re.compile(r'your name|who are you|call you', re.I)

		# offilne
		time = re.compile(r'time', re.I)
		date = re.compile(r'date', re.I)
		calculator = re.compile(r'calculator', re.I)
		calc = re.compile(r'calc', re.I)
		calendar = re.compile(r'calendar', re.I)

		# search functions
		google = re.compile(r'^google :|search :', re.I)
		wiki = re.compile(r'^wiki :|wikipedia :', re.I)

		# requires internet connection
		joke = re.compile(r'joke|funny|fun', re.I)
		quote = re.compile(r'quote|thought|thoughts', re.I)
		weather = re.compile(r'weather|temperature|temp', re.I)
		country = re.compile(r'country|cninfo', re.I)
		query = re.compile(r'question|who|what|when|why|where|which', re.I)
		math = re.compile(r'math|numbers', re.I)
		animal = re.compile(r'dog|cat|panda|fox|bird|koala|kangaroo|racoon|elephant|giraffe|whale', re.I)
		meme = re.compile(r'meme', re.I)
		history = re.compile(r'history', re.I)
		image = re.compile(r'^image|^pic|^photo', re.I)
		meaning = re.compile(r'^meaning|^dict', re.I)

		news = re.compile(r'news|headline|update', re.I)
		sci_news = re.compile(r'science', re.I)
		tech_news = re.compile(r'technology|geek|tech', re.I)
		ent_news = re.compile(r'entertainment|bollywood|movie|film', re.I)

		# help on TARS
		help_ = re.compile(r'--help|--h', re.I)
		commands_ = re.compile(r'--commands|--c', re.I)
		libraries_ = re.compile(r'--libraries|--l', re.I)

		anim = re.search(animal, self.query)

		self.input.config(fg='dodger blue')
		self.input['text'] = self.query + '  ✓'
		self.msg_box.focus()
		self.update()

		if self.query != '':
			# details expressions
			if re.search(my_name, self.query):
				self.response = services.get_name('user')
			elif re.search(your_name, self.query):
				self.response = services.get_name('tars')

			# offline
			elif re.search(time, self.query):
				self.response = services.get_time()
			elif re.search(date, self.query):
				self.response = services.get_date()
			elif re.search(calculator, self.query):
				self.response = 'Opening Calculator'
				services.run_calculator()
			elif re.search(calc, self.query):
				text = self.query.split(':')
				self.response = str(eval(text[1].strip()))
			elif re.search(calendar, self.query):
				text = self.query.split(':')[1]
				args = text.strip().split()
				if len(args) == 1:
					self.response = services.get_calendar(int(text.strip()))
				elif len(args) == 2:
					month, year = args
					self.response = services.get_calendar(int(year), month)

			# search functions
			elif re.search(google, self.query):
				self.response = 'Lets search on google'
				text = self.query.split(':')
				services.google_search(text[1].strip())
			elif re.search(wiki, self.query):
				text = self.query.split(':')
				self.response = services.wiki_search(text[1].strip())

			# requires internet connection
			elif re.search(joke, self.query):
				self.response = services.random_joke()
			elif re.search(meaning, self.query):
				text = self.query.split(':')
				self.response = services.get_meaning(text[1].strip())
			elif re.search(news, self.query):
				if re.search(sci_news, self.query):
					self.response = services.newsapi('science')
				elif re.search(ent_news, self.query):
					self.response = services.newsapi('entertainment')
				elif re.search(tech_news, self.query):
					self.response = services.newsapi('technology')
				else:
					self.response = services.get_news()
			elif re.search(image, self.query):
				text = self.query.split(':')
				self.response = services.get_images(text[1].strip())
			elif re.search(quote, self.query):
				self.response = services.randome_quote()
			elif re.search(weather, self.query):
				text = self.query.split(':')
				city = text[1].strip()
				self.response = services.get_weather(city)
			elif re.search(history, self.query):
				self.response = services.history_today()
			elif re.search(country, self.query):
				text = self.query.split(':')
				cn = text[1].strip()
				self.response = services.get_country(cn)
			elif re.search(query, self.query):
				self.query = self.query.replace('question','')
				self.response = services.wolfram_alpha(self.query)
			elif re.search(math, self.query):
				self.response = services.math_fact()
			elif anim:
				self.response = services.random_facts(anim.group())
			elif re.search(meme, self.query):
				self.response = services.get_memes()

			# TARS Help Commands
			elif re.search(help_, self.query):
				self.response = services.get_appdata(1)
			elif re.search(commands_, self.query):
				self.response = services.get_appdata(2)
			elif re.search(libraries_, self.query):
				self.response = services.get_appdata(3)		
			else:
				self.response = services.chatbot(self.query)

			# output configuration
			self.output.configure(state='normal')
			self.clear_output()
			if self.response == 'image':
				self.img = tk.PhotoImage(file='resized.png')
				self.output.image_create(tk.END, image = self.img)
			else:
				self.output.insert(tk.END, self.response.capitalize())
			self.input.config(fg='green')
			self.input['text'] = self.query + '  ✓✓'
			self.output.configure(state='disabled')
			self.update()

	def clear_output(self):
		self.output.delete(1.0, tk.END)	

# Driver Function ------------------------------------------------------------
if __name__ == '__main__':
	root = tk.Tk()
	root.geometry('300x400')
	root.resizable(0,0)
	root.wm_title('T.A.R.S.')
	root.iconbitmap('icons/TARS.ico')

	voice_search = PhotoImage(file='icons/voice_search.gif')
	send = PhotoImage(file='icons/send.gif')

	app = Application(master=root)
	app.mainloop()