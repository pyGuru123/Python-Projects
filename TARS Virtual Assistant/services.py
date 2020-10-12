import os
import re
import datetime
import calendar
import webbrowser
import configparser as cfg
import urllib.parse
from random import choice

import requests
from bs4 import BeautifulSoup
from PIL import Image

# configuration ------------------------------------------------
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'}

# Get config data ----------------------------------------------

def get_api_key(key):
	config = 'TARSdata/config.cfg'
	parser = cfg.ConfigParser()
	parser.read(config)
	return parser.get('creds', key)

def get_name(subject):
	config = 'TARSdata/config.cfg'
	parser = cfg.ConfigParser()
	parser.read(config)

	if subject == 'user':
		return parser.get('MasterDetails', 'name')
	elif subject == 'tars':
		return parser.get('TARSDetails', 'name')

def get_birth():
	config = 'TARSdata/config.cfg'
	parser = cfg.ConfigParser()
	parser.read(config)
	return parser.get('TARSDetails', 'dob')
		

# Custom T.A.R.S. functions ---------------------------------

def get_date():
	dt = datetime.datetime.now()
	dt = dt.date()
	return dt.strftime('%B %d, %Y')

def get_time():
	dt = datetime.datetime.now()
	dt = dt.time()
	return dt.strftime('%I:%M %p')

def run_calculator():
	os.system('calc')

def get_calendar(year, month_name=None):
	# month_name = month_name.lower()
	# months = {
	# 'jan' : 1, 'feb' : 2, 'mar' : 3, 'apr' : 4, 'may' : 5, 'jun' : 6,
	# 'jul' : 7, 'aug' : 8, 'sep' : 9, 'oct' : 10, 'nov' : 11, 'dec' : 12
	# }
	# if 
	output = '*------- Calendar --------*\n\n'
	if month_name is None:
		for i in range(1,13):
			output += calendar.month(year, i, 3, 1)
			output += '\n'
	else:
		month_num = datetime.datetime.strptime(month_name[:3], '%b').month
		output += calendar.month(year, month_num, 3, 1)

	return output

# Search online ------------------------------------------------------------

def google_search(term):
	chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
	website_re = re.compile('.com|.co|.in|.org|.net|.edu|')

	if not re.search(website_re, term):
		url = term.strip()
	else:
		base_url = "http://www.google.com/?#q="
		url = base_url + urllib.parse.quote(term)
	webbrowser.get(chrome_path).open_new(url)

def wiki_search(term):
	url = 'https://en.wikipedia.org/wiki/' + '_'.join(term.capitalize().split())
	annotations = re.compile(r'\[[^\]]*\]|\(([^\)]+)\)')
	output = ''
	try:
		r = requests.get(url, headers=header)
		html = r.text
		soup = BeautifulSoup(html, 'html.parser')
		div_ = soup.find('div', class_='mw-parser-output')
		paras = div_.find_all('p')
		for para in paras[:5]:
			output += para.text.strip().strip('\n')
		
		output = re.sub(annotations, '', output)
		return output.strip('\n')[:700]
	except:
		return "Not able to fetch data from wikipedia"

# Custom TARS functions ---------------------------------------------------------
def random_joke():
	url1 = 'https://official-joke-api.appspot.com/random_joke'
	url2 = 'https://some-random-api.ml/joke'
	url = choice([url1,url2])

	try:
		r = requests.get(url)
		if r:
			data = r.json()
			if 'setup' in data.keys():
				joke = data['setup'] + '\n'*2 + data['punchline']
			else:
				joke = data['joke']

		return joke
	except:
		return "Couldn't connect with internet"

def randome_quote():
	url = 'https://api.quotable.io/random'
	output = ''

	try:
		r = requests.get(url)
		quote = r.json()
		output += quote['content'] + '\n'
		output += f"     -{quote['author']}"

		return output
	except:
		return "Couldn't connect with internet"

def get_news():
	url = 'https://news.google.com/news/rss'
	output = ''

	try:
		r = requests.get(url)
		xml = r.text
		soup = BeautifulSoup(xml, 'xml')

		all_news = soup.find_all('item')
		for index, news in enumerate(all_news[:20]):
			output += f'{index+1} : {news.title.text}\n\n'

		return output
	except:
		return "Couldn't connect with internet"

def newsapi(type_):
	api_key = get_api_key('NewsApi')
	if api_key == 'None':
		return 'Get the api key for NewsApi for start using this service, check out readme'
	url = f"http://newsapi.org/v2/top-headlines?country=in&category={type_}&apiKey={api_key}"

	output = ''
	try:
		r = requests.get(url)
		data = r.json()
		articles = data['articles']
		for ct, article in enumerate(articles[:15]):
			output += f"{ct+1} : {article['title']} \n\n"

		return output
	except:
		return "Couldn't connect with internet"

def get_weather(city):
	api_key = get_api_key('OpenWeatherApi')
	if api_key == 'None':
		return 'Get the api key for OpenWeatherApi for start using this service, check out readme'
	url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
	output = f'Weather in {city} \n\n'

	try:
		r = requests.get(url)
		data = r.json()

		output += f"weather : {data['weather'][0]['description']} \n"
		output += f"temperature : {data['main']['temp'] - 273.15} C \n"
		output += f"pressure : {data['main']['pressure']} hPa \n"
		output += f"humidity : {data['main']['humidity']}% \n"
		output += f"windspeed : {data['wind']['speed']} m/s"

		return output
	except:
		return "Couldn't connect with internet"

def get_country(country):
	url = f'https://restcountries.eu/rest/v2/name/{country}?fullText=true'
	output = f'Search results for {country}\n\n'

	try:
		r = requests.get(url)
		data = r.json()[0]

		output += f"Name : {data['name']} \n"
		output += f"Capital : {data['capital']} \n"
		output += f"Continent : {data['region']} \n"
		output += f"Population : {data['population']} \n"
		output += f"Loc coords : {data['latlng']} \n"
		output += f"Currency : {data['currencies']} \n"

		return output
	except:
		return "Couldn't connect with internet"

def wolfram_alpha(query):
	query = '+'.join(query.split())
	api_key = get_api_key('WolframAlphaApi')
	if api_key == 'None':
		return 'Get the api key for WolframAlphaApi for start using this service, check out readme'

	url = f"http://api.wolframalpha.com/v1/result?appid={api_key}&i={query}%3f"

	try:
		r = requests.get(url)
		data = r.text
		
		if data == 'Wolfram|Alpha did not understand your input':
			return 'Couldn\'t understand the query'
		else:
			return data
	except:
		return "Couldn't connect with internet"

def math_fact():
	type_ = choice(['trivia','math'])
	url = "http://numbersapi.com/random/" + type_ + '?json'

	try:
		r = requests.get(url)
		data = r.json()
		return data['text']
	except:
		return "Couldn't connect with internet"

def random_facts(type_):
	url = 'https://some-random-api.ml/facts/' + type_
	try:
		r = requests.get(url)
		return r.json()['fact']
	except:
		return "Couldn't connect with internet"

def chatbot(msg):
	url = 'https://some-random-api.ml/chatbot'
	params = {'message' : '+'.join(msg.split())}

	try:
		r = requests.get(url, params=params)
		data = r.json()
		return data['response']
	except:
		return "Couldn't connect with internet"

def get_meaning(word):
	url = 'https://dictionary.cambridge.org/dictionary/english/' + word
	meaning = ''

	try:
		r = requests.get(url, headers=header)
		html = r.text
		soup = BeautifulSoup(html,'html.parser')

		wd = soup.find('div', class_="di-title")
		part_of_speech = soup.find('div',class_="posgram dpos-g hdib lmr-5")
		meanings = soup.find_all('div',class_='ddef_h')

		meaning += f'word : {wd.text}\n\n'
		meaning += 'Meanings :\n'
		for m in meanings:
			meaning += m.text + '\n\n'

		return meaning
	except:
		return "Couldn't connect with internet"

def history_today():
	date = datetime.datetime.today()
	month = date.strftime('%B')
	day = str(date.day)

	output = ''

	url = 'https://www.onthisday.com/day/'+ month + '/' + day
	try:
		r = requests.get(url, headers=header)
		html = r.text
		soup = BeautifulSoup(html,'html.parser')

		output += f'History : {month} {day}\n\n'

		output += 'Important Events\n'
		divs = soup.find_all('ul',class_='event-list event-list--with-advert')
		for i in divs:
			output += (i.text.strip('\n') + '\n')

		output += '\nFamous Birthdays\n\n'
		birthdays = soup.find('ul',class_='photo-list')
		bdays = birthdays.find_all('li')
		for i in bdays:
			output += (i.text.rstrip('\n') + '\n')

		check = soup.find_all('section',class_='grid__item one-half--1024')
		for i in check:
			output += (i.text.rstrip('\n') + '\n')

		did_you_know = soup.find('section',class_='section section--highlight section--did-you-know')
		output += (did_you_know.text.rstrip('\n') + '\n')

		return output
	except:
		return "Couldn't connect with internet"

# Image Downloader --------------------------------------------------------------

def download_image(image, png=True):
	if png:
		name = 'img.png'
	else:
		name = 'img.jpg'

	r = requests.get(image)
	data = r.content
	with open(name, 'wb') as f:
		f.write(data)

	img = Image.open(name)
	img.resize((260,300)).save('resized.png')
	return 'image'

def get_images(type_):
	q = '+'.join(type_.strip().split())
	api_key = get_api_key('PixabayApi')
	if api_key == 'None':
		return 'Get the api key for PixabayApi for start using this service, check out readme'
		
	url = f'https://pixabay.com/api/?key={api_key}&q={type_}&image_type=photo&per_page=200'
	name = 'img.jpg'

	try:
		r = requests.get(url)
		data = r.json()
		img = choice(data['hits'])
		img_url = img['largeImageURL']		
		return download_image(img_url)
	except:
		return "Couldn't connect with internet"

def get_memes():
	url = 'https://some-random-api.ml/meme'
	try:
		r = requests.get(url)
		data = r.json()
		img_url = data['image']
		return download_image(img_url, png=False)
	except:
		return "Couldn't connect with internet"

# https://funtranslations.com/api/?ref=apilist.fun
# https://chart.googleapis.com/chart?

# TARS DATA -----------------------------------------------------------------

def get_appdata(num):
	dct = {
		1 : 'TARSdata/help.txt',
		2 : 'TARSdata/commands.txt',
		3 : 'TARSdata/libraries.txt'
	}

	path = dct.get(num, None)
	if path is not None:
		with open(path) as f:
			data = f.read()

	return data