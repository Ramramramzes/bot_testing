import telebot
import requests
import json
from data import myToken
from data import myApiWeather

bot = telebot.TeleBot(myToken)


@bot.message_handler(commands=['start'])
def start(message):
    req = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={myApiWeather}&units=metric')
    #todo/-/  в конце url для выдачи в градусах ==> &units=metric 
    weather_data = json.loads(req.text)
    bot.send_message(message.chat.id, weather_data['list'][1]['dt_txt'])

bot.polling(none_stop=True)