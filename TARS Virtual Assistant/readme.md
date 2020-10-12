# TARS Virtual Assistant

TARS Virtual Assistant is a simple python tkinter based virtual assistant application which can do quick google searches for you, along with retrieving images, telling you a joke, random facts, give meanings of words, calculate expressions and even getting latest news headlines for you. An option for sending voice message queries and reading response is also available

![Alt text](app.png?raw=true "TARS Virtual Assistant")

TARS can also give you weather reports, calendar, facts about several animals and memes too

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :
* requests
* beautifulsoup4
* pillow
* speechrecognition
* pypiwin32

```bash
pip install requests
pip install beautifulsoup4
pip install pillow
pip install speechrecognition
pip install pypiwin32
```

Also use this 3rd party website [Python Extension Packages by Christoph Gohlke](https://www.lfd.uci.edu/~gohlke/pythonlibs/) to download and install the binary wheel file for <code> <b> pyaudio </b> </code> package which cannot be installed from pip, check out the tutorial [here](https://www.youtube.com/watch?v=6iXnY_6hZ8Y&t=23s)

#### API Note

TARS uses these 4 api to retirve the best possible results for you, so an api key is required for these apis:
* NewsApi : to get you the latest news updates
* Wolframalpha Api : for quick one line answers
* OpenWeatherMap Api : to get weather reports
* Pixabay Api : to get images

You can get the api keys from here
* NewsApi : [Register NewsApi](https://newsapi.org/register)
* Wolfram Alpha Api : [Documentation](https://products.wolframalpha.com/short-answers-api/documentation/)
* OpenWeatherMap API : [API List](https://openweathermap.org/api) [Subscribe for free current weather data]
* Pixabay API : [Register](https://pixabay.com/accounts/login/?next=/api/docs/)

##### After collecting api keys, put them under [creds] in config.cfg file which is available in TARSdata folder.  Example:

replace following with 
> [creds]
> NewsApi = None
> OpenWeatherApi = None

with api respective api keys
> [creds]
> NewsApi = 0d48912cbe864506a076545fdfd545
> OpenWeatherApi = a3f541eba5644354343gdfdff4545

## Usage

Double click the application.pyw to open the GUI application, then start typing your query or command, press enter and TARS will try to respond you with the best possible answer, you can also use voice search for sending queries. 

[ List of T.A.R.S. Commands ]

[i] : requires internet connection
[o] : works offline

* time : get current time [o]
* date : get current date [o]
* calculator : opens windows calculator app [o]
* calc : calculates the following expression [o]
* calendar : get the calendar [o]

* joke : get random jokes [i]
* news : get latest news headlines [i]
* quote : get random quote [i]
* weather : get city weather [i]
* country : get information of a certain country [i]
* query : get short answers [i]
* math : get a random math fact / trivia [i]
* meaning : get meanings of an english word [i]
* image : get images related to your [i]
* meme : get random memes [i]
* google : make a google search in chrome browser [i]
* wiki : do a quick wikipedia search [i]
* history : get the famous historical events of the given date [i]
* animals : you can get random facts about these animals - dog,cat,panda,fox,bird,koala,kangaroo,racoon,elephant,giraffe,whale [i]

*------ Command Usage -------*

#### Offline commands

time | usage 
> what time is it

date | usage
> what date is today

calculator | usage
> open the calculator

calc  
> calc : 10 + 5 + 12
> calc : 23 * 5 / 6
> what is the sum of 50 and 60

calendar | usage
> calendar : 2020
> calendar : 2018

#### Requires internet

joke | usage
> get me a random joke or tell me something funny

news | usage
> get me todays headlines
> tell me science news
> get me entertainment updates
> get me technology news

quote | usage
> get me a quote

weather | usage
> weather : varanasi
> weather : kanpur

country | usage
> country : india
> country : japan

query | | usage
> what is the capital of india
> who is Narendra modi
> where is Niagra falls
> when did humans landed on moon
> which is the largest building in the world

math | usage
> get me a random math fact
> tell me something interesting about numbers

meaning | usage
> meaning : mango
> meaning : energy
> meaning : turmeric

image | usage
> image : sunset
> image : cat
> image : captain america

meme | usage
> get me a meme
> send a funny meme

google | usage
> google : alpha particles
> google : www.google.com

wiki | usage
> wiki : alpha particles
> wiki : narendra modi

histroy | usage
> history : 22 june
> history : 21 november

animals | usage
> tell me something about birds
> what about dogs
> ok cats

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.