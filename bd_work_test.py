import telebot
import sqlite3
from data import myToken
bot = telebot.TeleBot(myToken)
name = ''
bot_msg = 0
@bot.message_handler(commands=['start'])
def start(message):
    global bot_msg
    user_id = message.from_user.id
    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER , name varchar(50), pass varchar(50))')
    cur.execute('SELECT id FROM users WHERE id = ?', (user_id,))
    existing_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if existing_user:
        if message.from_user.id != 606593563:
            bot.send_message(message.chat.id, 'Вы уже зарегались')
            bot.delete_message(message.chat.id, message.id)
        else:
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
            bot_msg = bot.send_message(message.chat.id,'Здарова админ',reply_markup=markup)
            bot.delete_message(message.chat.id, message.id)

    else:
        bot_msg = bot.send_message(message.chat.id, 'Сейчас зарегистрируем\nВведите имя')
        bot.delete_message(message.chat.id, message.id)
        bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    global bot_msg
    name = message.text.strip()

    bot.delete_message(message.chat.id, bot_msg.message_id)
    bot_msg = bot.send_message(message.chat.id, 'Введите пароль')
    bot.delete_message(message.chat.id, message.id)

    bot.register_next_step_handler(message,user_pass)

def user_pass(message):
    global bot_msg
    password = message.text.strip()

    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO users (id, name, pass) VALUES ('%s','%s', '%s')" % (message.from_user.id,name,password))

    conn.commit()
    cur.close()
    conn.close()

    bot.delete_message(message.chat.id, bot_msg.message_id)
    bot_msg = bot.send_message(message.chat.id,'Пользователь зарегистрирован',)
    bot.delete_message(message.chat.id, message.id)
@bot.callback_query_handler(func=lambda call: call.data == 'users')
def users(call):
    global bot_msg

    conn = sqlite3.connect('data.sql')
    cur = conn.cursor()

    cur.execute('SELECT id, name, pass FROM users')
    data = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    if data:
        user_list = "\n".join([f"===============\nID: {row[0]}\nName: {row[1]}\nPassword: {row[2]}\n" for row in data])
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton('Назад', callback_data='adm_list'))
        bot.send_message(call.message.chat.id, user_list,reply_markup=markup)
        bot.delete_message(call.message.chat.id, bot_msg.message_id)

    else:
        bot.send_message(call.message.chat.id, 'Пользователей нет')

@bot.callback_query_handler(func=lambda call: call.data == 'adm_list')
def adm_list(call):
    global bot_msg

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot_msg = bot.send_message(call.message.chat.id, 'Здарова админ', reply_markup=markup)
    bot.delete_message(call.message.chat.id, call.message.id)

bot.polling(none_stop=True)