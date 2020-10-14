# Covid Tracker

Covid Tracker is a simple python based covid cases tracking application made using the  tkinter and requests library. The data is scraped from the [worldometers.info](https://www.worldometers.info/coronavirus/) website.

![Alt text](app.png?raw=true "Covid Tracker")

You can search for individual country stats by writing the country name in the entry and then either clicking search or pressing enter key. You can also check top 10 country stats from the button at the left bottom part of the app

## How to Download

Download this project from here [Download Covid Tracker](https://downgit.github.io/#/home?url=https:%2F%2Fgithub.com%2FpyGuru123%2FPython-Projects%2Ftree%2Fmaster%2FCovid%20Tracker)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following libraries : 
* requests
* beautifulsoup
* matplotlib
* pandas

```bash
pip install requests
pip install beautifulsoup4
pip install matplotlib
pip install pandas
```

## Usage

Double click the application.py to open the GUI application, it requires an active internet connection to fetch data from the internet, so make sure you are connected with internet. You can obtain a bar/pie chart by clicking the respective buttons at the top left, a table of top 10 country stats by clicking top 10 at the bottom left. The top ribbon gives total cases, active cases, recovered cases, deaths and cases reported today

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
