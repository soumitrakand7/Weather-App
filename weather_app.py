import datetime
from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox

url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['api_key']['key']

e = datetime.datetime.now()


class WeatherApp:
    def __init__(self, window):
        super().__init__()
        self.city_text = StringVar()
        self.window = window
        self.weather = []
        self.frame = Frame(self.window)
        self.frame.pack()
        self.canvas = Canvas(
            self.frame,
            bg="#ffffff",
            height=682,
            width=522,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.pack()

        self.background_img = PhotoImage(file=f"background.png")
        self.background = self.canvas.create_image(
            261.0, 341.0,
            image=self.background_img)

        self.entry0_img = PhotoImage(file=f"img_textBox0.png")
        self.entry0_bg = self.canvas.create_image(
            257.0, 260.0,
            image=self.entry0_img)

        self.entry0 = Entry(
            bd=0,
            bg="#dcdbdb",
            textvariable=self.city_text,
            highlightthickness=0)

        self.entry0.place(
            x=46.0, y=244,
            width=422.0,
            height=30)

        self.img0 = PhotoImage(file=f"img0.png")
        self.b0 = Button(bg='#023c48',
                         image=self.img0,
                         activebackground='#023c48',
                         activeforeground='#023c48',
                         borderwidth=0,
                         highlightthickness=0,
                         command=self.btn_clicked,
                         relief="flat")

        self.b0.place(
            x=213, y=309,
            width=98,
            height=33
        )

    def getweather(self, city):
        result = requests.get(url.format(city, api_key))

        if result:
            json = result.json()
            city = json['name']
            temp_kelvin = json['main']['temp']
            temp_celsius = temp_kelvin-273.12
            weather1 = json['weather'][0]['main']
            icon = json['weather'][0]['icon']
            speed = json['wind']['speed']
            humidity = json['main']['humidity']
            visibility = json['visibility']
            pressure = json['main']['pressure']
            final = [city, temp_celsius,
                     icon,  weather1, speed, humidity, visibility, pressure]
            return final
        else:
            print("NO Content Found")

    def btn_clicked(self):
        city = self.city_text.get()
        self.weather = self.getweather(city)
        if self.weather:
            self.frame.pack_forget()
            self.frame1 = Frame(self.window)
            self.frame1.pack()

            self.canvas = Canvas(
                self.frame1,
                bg="#ffffff",
                height=682,
                width=522,
                bd=0,
                highlightthickness=0,
                relief="ridge")
            self.canvas.pack()
            self.background_img = PhotoImage(
                file="background1.png")
            self.background = self.canvas.create_image(
                -12.5, 310.5,
                image=self.background_img)

            self.iconImage = PhotoImage(
                file=r"icons\{}@2x.png".format(self.weather[2])).zoom(2, 2)

            self.canvas.create_image(
                400, 96, image=self.iconImage)

            self.canvas.create_text(
                146, 168,
                text='{0:.2f}'.format(self.weather[1]) + " °C",
                fill="#ffffff",
                font=("Bahnschrift", int(36)))

            self.canvas.create_text(
                130, 75,
                text=self.weather[0],
                fill="#eafff4",
                font=("Segoe Script", int(30)))

            self.canvas.create_text(
                400.0, 360.5,
                text=str(round(self.weather[7])) + " mbar",
                fill="#ffffff",
                font=("Leelawadee UI", int(18)))

            self.canvas.create_text(
                400.0, 569.5,
                text=str(round(self.weather[6])) + " m",
                fill="#ffffff",
                font=("Leelawadee UI", int(18)))

            self.canvas.create_text(
                394.5, 187.0,
                text=self.weather[3],
                fill="#ffffff",
                font=("Corbel", int(22)))

            self.canvas.create_text(
                147.5, 360.5,
                text='{0:.3g}'.format(self.weather[4]) + " m/sec",
                fill="#ffffff",
                font=("Leelawadee UI", int(18)))

            self.canvas.create_text(
                145.5, 569.5,
                text='{0:.3g}'.format(self.weather[5]) + " %",
                fill="#ffffff",
                font=("Leelawadee UI", int(18)))
        else:
            messagebox.showerror(
                'Error', "Cannot find the city {}".format(city))


if __name__ == "__main__":

    window = Tk()
    window.title('Weather App')
    window.resizable(False, False)
    window.geometry("522x682")
    app = WeatherApp(window)

    window.mainloop()
