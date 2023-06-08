#! python
import sys
import random
import datetime
import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
from tkinter import ttk

import requests
from PIL import Image
from PIL import ImageTk

api_key = "f3d5bb64b5f26365f0d033f3e4e0ef96"


class CustomFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        width = kwargs.get("width", 90)
        height = kwargs.get("height", 130)
        self.configure(width=width, height=height, padx=10)


class CustomLabel(tk.Label):
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, **kwargs)

        width = kwargs.get("width", 90)
        height = kwargs.get("height", 130)
        bg = kwargs.get("bg", "Gray92")
        fg = kwargs.get("fg", "black")
        self.configure(
            width=width,
            height=height,
            bg=bg,
            compound=tk.TOP,
            font=("Arial", 13),
            wraplength=100,
        )


# class AutocompleteEntry(tk.Entry):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # self.suggestions = suggestions
#         self.matches = []  # hold suggestions that match entered txt
#         self.current_match = tk.StringVar()  # stores currently selected suggestion
#         self.current_match.set("")

#         self.bind("<KeyRelease>", self.autocomplete)
#         self.bind(
#             "<Down>", self.cycle_matches
#         )  # allows cycling through the available matches.

#     def autocomplete(self, event):
#         entered_text = self.get().lower()
#         self.matches = [
#             suggestion
#             for suggestion in self.suggestions
#             if suggestion.lower().startswith(entered_text)
#         ]

#         if self.matches:
#             self.current_match.set(self.matches[0])
#             self.icursor(tk.END)
#             self.select_range(len(entered_text), tk.END)
#         else:
#             self.current_match.set("")

#     def cycle_matches(self, event):
#         if self.matches:
#             current_index = self.matches.index(self.current_match.get())
#             next_index = (current_index + 1) % len(self.matches)
#             self.current_match.set(self.matches[next_index])

#     def set_suggestions(self, suggestions):
#         self.suggestions = suggestions


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.master = master
        self.grid()

        self.label_frame = tk.Frame(self)
        self.label_frame.grid(row=0, column=0)
        self.label_frame.grid_propagate(False)
        self.label = tk.Label(self, image=bg_image)
        self.label.grid(row=0, column=0)
        self.label.grid_propagate(False)

        self.date = self.current_date()
        self.label_bg = "Gray92"
        self.city = tk.StringVar()
        self.city.set("")

        self.draw_frames()
        self.draw_widgets()
        self.current_time()

        self.master.bind("<Return>", self.get_weather)

    def draw_frames(self):
        self.top = CustomFrame(self.label, width=490, height=50, bg="DodgerBlue2")
        self.top.grid(row=0, column=0, columnspan=3)
        self.top.grid_propagate(False)

        self.search_frame = CustomFrame(
            self.label, width=490, height=40, bg="DodgerBlue2"
        )
        self.search_frame.grid(row=1, column=0, columnspan=3, pady=(2, 0))
        self.search_frame.grid_propagate(False)

        self.datetime_frame = CustomFrame(
            self.label, width=145, height=95, bg="DodgerBlue2"
        )
        self.datetime_frame.grid(row=0, column=3, rowspan=2, padx=3)
        self.datetime_frame.grid_propagate(False)

        # windspeed frame
        self.windspeed = CustomFrame(self.label, bg=self.label_bg)
        self.windspeed.grid(row=2, column=3, pady=(100, 20))
        self.windspeed_lbl = CustomLabel(
            self.windspeed, image=wind_icon, text="\nWindspeed"
        )
        self.windspeed_lbl.grid(row=0, column=0, padx=(5, 2), sticky="S")

        # weather frame
        self.weather = CustomFrame(self.label, bg=self.label_bg)
        self.weather.grid(row=3, column=0)
        self.weather_lbl = CustomLabel(
            self.weather, image=clear_weather_icon, text="\nWeather"
        )
        self.weather_lbl.grid(row=0, column=0)

        # temperature frame
        self.temperature = CustomFrame(self.label, bg=self.label_bg)
        self.temperature.grid(row=3, column=1)
        self.temperature_lbl = CustomLabel(
            self.temperature, image=high_temp_icon, text="\nTemperature"
        )
        self.temperature_lbl.grid(row=0, column=0, padx=(5, 2))

        # humidity frame
        self.humidity = CustomFrame(self.label, bg=self.label_bg)
        self.humidity.grid(row=3, column=2)
        self.humidity_lbl = CustomLabel(
            self.humidity, image=humidity_icon, text="\nHumidity"
        )
        self.humidity_lbl.grid(row=0, column=0, padx=(5, 10))

        # pressure frame
        self.pressure = CustomFrame(self.label, bg=self.label_bg)
        self.pressure.grid(row=3, column=3)
        self.pressure_lbl = CustomLabel(
            self.pressure, text="\nPressure", image=pressure_icon
        )
        self.pressure_lbl.grid(row=0, column=0, padx=(5, 2))

    def draw_widgets(self):
        # self.top
        self.app_label = tk.Label(
            self.top,
            text="Weather Report",
            font=("Algerian", 20),
            bg="DodgerBlue2",
            fg="white",
        )
        self.app_label.grid(row=0, column=0, ipady=10, ipadx=10)

        # self.datetime_frame
        self.date_label = tk.Label(
            self.datetime_frame,
            text=self.date,
            font=("Arial", 15, "bold"),
            bg="DodgerBlue2",
            fg="white",
            anchor="w",
        )
        self.date_label.grid(row=0, column=0, ipady=14, ipadx=0)

        self.time_label = tk.Label(
            self.datetime_frame,
            font=("Calibri", 14),
            bg="DodgerBlue2",
            fg="white",
            anchor="w",
        )
        self.time_label.grid(row=1, column=0, ipady=0, ipadx=0)

        # self.search_frame
        self.search_label = tk.Label(
            self.search_frame,
            text="Search City : ",
            bg="DodgerBlue2",
            fg="white",
            anchor="w",
            font=("Arial", 11),
        )
        self.search_label.grid(row=0, column=0, ipady=8, padx=(10, 2))

        # autocomplete_suggestions = [
        #     "New York",
        #     "London",
        #     "Lucknow" "Paris",
        #     "Tokyo",
        #     "New Delhi",
        # ]
        # self.entry = AutocompleteEntry(
        #     self.search_frame,  # dont change this affects pos of search bar
        #     autocomplete_suggestions,
        #     textvariable=self.city,  # Use self.city as textvariable
        #     width=20,  # Set the desired widt
        # )
        # self.entry.bind("<Return>", self.get_weather)
        # self.entry.set_suggestions(autocomplete_suggestions)
        city_names = ["New York", "Los Angeles", "London", "Paris", "Tokyo"]

        self.entry = ttk.Combobox(
            self.search_frame,
            textvariable=self.city,
            values=city_names,
        )

        def on_search(event):
            entered_text = self.city.get()
            suggestions = []
            for city in city_names:
                if city.lower().startswith(entered_text.lower()):
                    suggestions.append(city)
            self.entry["values"] = suggestions

        self.entry.autocomplete = True
        self.entry.bind("<<ComboboxSelected>>", on_search)
        self.entry.bind("<KeyRelease>", on_search)
        self.entry.focus_set()
        self.entry.grid(row=0, column=1, ipady=2)

        self.search = tk.Button(
            self.search_frame,
            image=search_icon,
            command=self.weather_search,  # wjen button is called this func has to be called
            relief=tk.FLAT,
            bg="DodgerBlue2",
        )
        self.search.grid(row=0, column=2, padx=5, ipady=1)

        self.city_label = tk.Label(
            self.search_frame,
            text="",
            bg="DodgerBlue",
            fg="white",
            anchor="c",
            font=("Arial", 10, "bold"),
            width=19,
        )
        self.city_label.grid(row=0, column=3, ipady=3, padx=(41, 0))

    # root = tk.Tk()
    # search_var = tk.StringVar()
    # search_combobox = ttk.Combobox(root, textvariable=search_var)

    # def on_search(event, search_var, search_combobox, xity_names):
    #     entered_text = search_var.get()
    #     suggestions = []
    #     for city in city_names:
    #         if city.lower().startswith(entered_text.lower()):
    #             suggestions.append(city)
    #     search_combobox["values"] = suggestions

    # city_names = ["New York", "Los Angeles", "London", "Paris", "Tokyo"]
    # search_combobox.autocomplete = True
    # search_combobox.bind("<<ComboboxSelected>>", on_search)
    # search_combobox.bind(
    #     "<KeyRelease>", on_search
    # )  # Optionally trigger on each key release
    # search_combobox["values"] = city_names
    # root.mainloop()

    def current_time(self):
        dt = datetime.datetime.now()
        self.time_label["text"] = dt.strftime("%I:%M:%S %p")
        self.time_label.after(1000, self.current_time)

    def current_date(self):
        dt = datetime.datetime.today()
        return dt.strftime("%d %b, %Y")

    def weather_search(self):
        self.get_weather()
        # city_prefix = self.city.get()
        # if len(city_prefix) > 2:
        #     autocomplete_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_prefix}&limit=5&appid={api_key}"
        # try:
        #     response = requests.get(autocomplete_url)
        #     suggestions = [city["name"] for city in response.json()]
        #     self.entry["values"] = suggestions
        #     self.entry.event_generate("<Down>")  # Show dropdown suggestions
        # except:
        #     messagebox.showerror(
        #         "Weatherzilla", "Failed to fetch autocomplete suggestions"
        #     )

    def get_weather(self, event=None):
        city = self.entry.get()
        if len(city) > 2:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            try:
                self.update()
                r = requests.get(url)
                data = r.json()

                weather = data["weather"][0]["description"]
                weather = weather.lower()
                temp = round(data["main"]["temp"] - 273.15, 2)
                if len(weather.split()) == 1:
                    weather = "\n" + weather
                else:
                    weather = "\n".join(weather.split())
                self.weather_lbl["text"] = f"{weather}"
                self.temperature_lbl["text"] = f"\n{temp} C"
                self.windspeed_lbl["text"] = f"\n{data['wind']['speed']} m/s"
                self.humidity_lbl["text"] = f"\n{data['main']['humidity']} %"
                self.pressure_lbl["text"] = f"\n{data['main']['pressure']} hPa"

                if temp <= 18:
                    self.temperature_lbl["image"] = low_temp_icon
                else:
                    self.temperature_lbl["image"] = high_temp_icon

                if "thunder" in weather:
                    self.weather_lbl["image"] = thunderstorm_icon
                elif "cloud" in weather:
                    self.weather_lbl["image"] = cloudy_icon
                elif "snow" in weather:
                    self.weather_lbl["image"] = snow_icon
                elif "drizzle" in weather or "rain" in weather:
                    self.weather_lbl["image"] = drizzle_icon
                elif (
                    "mist" in weather
                    or "haze" in weather
                    or "fog" in weather
                    or "smoke" in weather
                ):
                    self.weather_lbl["image"] = mist_icon
                elif "hail" in weather:
                    self.weather_lbl["image"] = hail_icon
                else:
                    self.weather_lbl["image"] = clear_weather_icon

                self.city_label["text"] = f"Weather in {city.capitalize()}"

            except KeyError:
                messagebox.showerror("Weatherzilla", "No such city in database")
            except:
                messagebox.showerror("Weatherzilla", "No internet Connection")

            self.entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Weatherzilla")

    if not api_key:
        root.withdraw()
        messagebox.showerror(
            "Weatherzilla", "OpenWeatherMap Api Key is required\n to use this App"
        )
        sys.exit(0)
    import os

    bg_path = r"C:\project\Python-Projects\Weatherzilla - Weather App\wallpapers"
    bg_list = [os.path.join(bg_path, filename) for filename in os.listdir(bg_path)]
    bg_r = random.choice(bg_list)
    bg = Image.open(bg_r)
    bg_image = ImageTk.PhotoImage(bg)

    search_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\search.png"
    )

    clear_weather_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\clear.png"
    )
    clouds = Image.open(
        "C:\project\Python-Projects\Weatherzilla - Weather App\icons\clear.png"
    )
    cloudy_icon = ImageTk.PhotoImage(clouds)
    high_temp_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\high_temp.png"
    )
    low_temp_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\low_temp.png"
    )
    humidity_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\humidity.png"
    )
    pressure_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\pressure.png"
    )
    wind_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\wind.png"
    )
    thunderstorm_icon = PhotoImage(
        file="C:/project/Python-Projects/Weatherzilla - Weather App/icons/thunderstorm.png"
    )
    snow_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\snow.png"
    )
    drizzle_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\drizzle.png"
    )
    mist_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\mist.png"
    )
    hail_icon = PhotoImage(
        file="C:\project\Python-Projects\Weatherzilla - Weather App\icons\hail.png"
    )

    app = Application(master=root)
    app.mainloop()
