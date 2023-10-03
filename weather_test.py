import telebot
import requests
import json

from dotenv import load_dotenv
import os
load_dotenv()
myToken = os.getenv('myToken')
myApiWeather = os.getenv('myApiWeather')


global lat,lon,mes_id,main_mes_id

bot = telebot.TeleBot(myToken)


@bot.message_handler(commands=['start'])
def start(message):
  global mes_id,main_mes_id
  # bot.send_message(message.chat.id,'Здравствуйте! Введите координаты')
  main_mes_id = bot.send_message(message.chat.id,'Здравствуйте! Введите координаты').message_id
  mes_id = bot.send_message(message.chat.id,'Введите широту ==>').message_id
  bot.delete_message(message.chat.id, message.id)
  bot.register_next_step_handler(message, send_lat)


# ! Создать еще один message_hendler к lat присваивается значение /старт нужно все разделить  
@bot.message_handler()
def send_lat(message):
  global lat,lon,mes_id,main_mes_id,user_msg
  bot.delete_message(message.chat.id,message_id=mes_id)
  bot.delete_message(message.chat.id,message_id=main_mes_id)
  mes_id = bot.send_message(message.chat.id,'Введите долготу ==>').message_id
  lat = message.text
  bot.delete_message(message.chat.id, message.id)
  bot.register_next_step_handler(message, send_lon)
  

def send_lon(message):
  global lat,lon
  lon = message.text
  bot.delete_message(message.chat.id,message_id=mes_id)
  send_data(message)
  bot.delete_message(message.chat.id, message.id)

def send_data(message):
  global lat,lon,user_msg
  # print(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}&units=metric')
  req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}&units=metric')
  # #todo/-/  в конце url для выдачи в градусах ==> &units=metric 
  weather_data = json.loads(req.text)
  temperature = weather_data['list'][0]['main']['temp']
  bot.send_message(message.chat.id,f'Температура по координатам:\n{lat},{lon}\n' + str(temperature) + ' °C')

bot.polling(none_stop=True)