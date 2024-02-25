import telebot
import datetime
import threading

TOKEN = '7172008657:AAHcU7TQuMF1MHCGJMy2aJAR1ICJQs-xndc'
bot = telebot.TeleBot(TOKEN)

users_schedule = {}

def send_message(chat_id, message):
    bot.send_message(chat_id, message)

def schedule_message(chat_id, message, time_delay):
    users_schedule[chat_id] = threading.Timer(time_delay, send_message, args=[chat_id, message])
    users_schedule[chat_id].start()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup( resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Отправить через", )
    button2 = telebot.types.KeyboardButton(text="Отправить в")
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, "Выбери один из вариантов:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    chat_id = message.chat.id
    text = message.text

    if text == "Отправить через":
        bot.send_message(chat_id, "Введите сообщение:")
        bot.register_next_step_handler(message, send_later)
    elif text == "Отправить в":
        bot.send_message(chat_id, "Введите сообщение:")
        bot.register_next_step_handler(message, send_at)
    else:
        bot.send_message(chat_id, "Выбери один из вариантов!")

def send_later(message):
    chat_id = message.chat.id
    text = message.text
    bot.send_message(chat_id, "Введите время через сколько нужно отправить сообщение в секундах:")
    bot.register_next_step_handler(message, lambda m: schedule_message(chat_id, text, int(m.text)))

def send_at(message):
    chat_id = message.chat.id
    text = message.text
    bot.send_message(chat_id, "Введите время в формате ЧЧ:ММ (например, 14:30):")
    bot.register_next_step_handler(message, lambda m: schedule_message(chat_id, text, calculate_delay(m.text)))

def calculate_delay(time_str):
    current_time = datetime.datetime.now()
    scheduled_time = datetime.datetime.strptime(time_str, '%H:%M')
    if scheduled_time < current_time:
        scheduled_time += datetime.timedelta(days=1)
    delta_t = scheduled_time - current_time
    return delta_t.total_seconds()

bot.polling()