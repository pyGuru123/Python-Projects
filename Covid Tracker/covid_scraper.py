# importing modules
import requests
import pandas as pd 
from bs4 import BeautifulSoup
from datetime import datetime

def todays_date():
	dt = datetime.now()
	return dt.strftime('%d %B-%Y')

def scrape_data():
	# requesting data from website
	url = 'https://www.worldometers.info/coronavirus/'

	try:
		r = requests.get(url)
	except:
		return None

	# parsing it to beautiful soup
	data = r.text
	soup = BeautifulSoup(data,'html.parser')

	# Extracting table data
	table_body = soup.find('tbody')
	table_rows = table_body.find_all('tr')

	dct = {
		'countries' : [],
		'cases' : [],
		'todays' : [],
		'deaths' : [],
		'recovered' : [],
		'active' : [],
	}

	for tr in table_rows:
		td = tr.find_all('td')
		dct['countries'].append(td[1].text)
		dct['cases'].append(td[2].text)
		dct['todays'].append(td[3].text.strip())
		dct['deaths'].append(td[4].text.strip())
		dct['recovered'].append(td[6].text.strip())
		dct['active'].append(td[8].text.strip())


	indices = [i for i in range(len(dct['countries']))]
	df = pd.DataFrame(dct,index=indices)
	df.fillna(0)
	df  = df[7:]
	df.reset_index(drop=True, inplace=True)

	filename = 'files/corona-cases.csv'
	df.to_csv(filename)

	return 1

if __name__ == '__main__':
	print("This file isn't supposed to run")
	print('run covid_app.py')