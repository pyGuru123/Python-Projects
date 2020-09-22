from covid_analyser import cvt_to_integer
from matplotlib.figure import Figure 

def get_plot(data, name, type='bar'):
	data = [cvt_to_integer(i) for i in data]

	figure = Figure(figsize=(5.6, 4), dpi=100)
	plot = figure.add_subplot(111)
	plot.set_title(f'Covid stats in {name}')

	if type == 'bar':
		x = ['Total', 'Active', 'Recovered', 'Deaths']

		plot.bar(x, data[:4])

		plot.set_xlabel('parameters')
		plot.set_ylabel('stats')

	elif type == 'pie':
		labels = ['Active', 'Recovered', 'Deaths']
		explode = (0,0,0.1)
		plot.pie(data[1:4], labels=labels, autopct='%1.2f%%', explode=explode)

	return figure

if __name__ == '__main__':
	print("This file isn't supposed to run")
	print('run covid_app.py')