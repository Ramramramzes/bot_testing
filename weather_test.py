import telebot
import requests
import json

from dotenv import load_dotenv
import os
load_dotenv()
myToken = os.getenv('myToken')
myApiWeather = os.getenv('myApiWeather')


global lat,lon

bot = telebot.TeleBot(myToken)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id,'Здравствуйте! Введите координаты')
  bot.send_message(message.chat.id,'Введите широту ==>')
  bot.register_next_step_handler(message, send_lat)


# ! Создать еще один message_hendler к lat присваивается значение /старт нужно все разделить  
@bot.message_handler()
def send_lat(message):
  global lat,lon
  bot.send_message(message.chat.id,'Введите долготу ==>')
  lat = message.text
  bot.register_next_step_handler(message, send_lon)

def send_lon(message):
  global lat,lon
  lon = message.text
  send_data(message)

def send_data(message):
  global lat,lon
  # print(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}&units=metric')
  req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}&units=metric')
  # #todo/-/  в конце url для выдачи в градусах ==> &units=metric 
  weather_data = json.loads(req.text)
  temperature = weather_data['list'][0]['main']['temp']
  bot.send_message(message.chat.id, str(temperature) + ' °C')

bot.polling(none_stop=True)