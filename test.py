import telebot
import requests
import json
from data import myToken
from data import myApiWeather

global lat,lon

bot = telebot.TeleBot(myToken)


@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id,'Здравствуйте! Введите координаты')
  send_lat(message)

# ! Создать еще один message_hendler к lat присваивается значение /старт нужно все разделить  

def send_lat(message):
  bot.send_message(message.chat.id,'Введите широту ==>')
  global lat,lon
  lat = message.text
  bot.register_next_step_handler(message, send_lon)

def send_lon(message):
  global lat,lon
  bot.send_message(message.chat.id,'Введите долготу ==>')
  lon = message.text
  bot.register_next_step_handler(message, send_data)



def send_data(message):
  global lat,lon
  print(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}=metric')
  req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}=metric')
  #todo/-/  в конце url для выдачи в градусах ==> &units=metric 
  weather_data = json.loads(req.text)
  temperature = weather_data['list'][0]['main']['temp']
  bot.send_message(message.chat.id, temperature)

bot.polling(none_stop=True)