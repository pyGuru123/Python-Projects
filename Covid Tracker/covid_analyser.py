import os
import pandas as pd

def read_stats_file():
	filename = 'files/corona-cases.csv'
	if os.path.exists(filename):
		df = pd.read_csv(filename)

	return df

df = read_stats_file()

def cvt_to_integer(x):
	value = [i for i in str(x) if i.isdigit()]
	return int(''.join(value))
	

def get_world():
	data = df.iloc[0].fillna(0)
	return (data['cases'], data['active'], data['recovered'], data['deaths'], data['todays'])

def top10():
	data = df[1:11].fillna(0)

	copy = data
	copy['cases'] = copy['cases'].apply(lambda x : cvt_to_integer(x))
	copy['active'] = copy['active'].apply(lambda x : cvt_to_integer(x))
	copy['recovered'] = copy['recovered'].apply(lambda x : cvt_to_integer(x))
	copy['deaths'] = copy['deaths'].apply(lambda x : cvt_to_integer(x))
	copy['todays'] = copy['todays'].apply(lambda x : cvt_to_integer(x))
	values = [sum(copy['cases']),
			  sum(copy['active']),
			  sum(copy['recovered']),
			  sum(copy['deaths']),
			  sum(copy['todays'])]

	arr = data.values.tolist()
	headers = ['Index', 'Country', 'Total Cases', 'Todays', 'Deaths', 'Recovered', 'Active']
	arr.insert(0, headers)

	return values, arr

def get_country(name):
	try:
		ind = df.index[df['countries'] == name][0]
		data = df.iloc[ind].fillna(0)
		return (data['cases'], data['active'], data['recovered'], data['deaths'], data['todays'])
	except:
		return None

if __name__ == '__main__':
	print("This file isn't supposed to run")
	print('run covid_app.py')