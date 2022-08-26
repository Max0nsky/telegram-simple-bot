# -*- coding: utf-8 -*-
import telebot
import params
import storage

from keyboards import Keyboard

token = params.getToken()
bot = telebot.TeleBot(token)
    
# Стартовая команда при первом запуске
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, {0.first_name}! Добро пожаловать ✌️".format(message.from_user), reply_markup=Keyboard.v1())

# Обработка сообщений
@bot.message_handler()
def start(message):
    storage.init_storage(message)

    if message.text in ['Запись', 'запись']:
        making_user_record(message)
    elif message.text in ['Информация', 'информация']:
        bot.send_message(
            message.chat.id, "Какая-то информация...")
    else:
        bot.send_message(
            message.chat.id, "Не знаю что на это ответить")


# Создание записи на услугу
def making_user_record(message):
    bot.send_message(message.chat.id, "Введите ваше имя:", reply_markup=Keyboard.delete())
    bot.register_next_step_handler(message, plus_name)

# Шаг 1 - имя
def plus_name(message):
    storage.set_storage_data(message, "user_name", message.text)
    bot.reply_to(message, "Отлично! Выберите услугу:", reply_markup=Keyboard.v2())
    bot.register_next_step_handler(message, plus_service)

# Шаг 2 - услуга
def plus_service(message):
    storage.set_storage_data(message, "user_service", message.text)
    bot.reply_to(message, "Теперь выберите подходящую дату:", reply_markup=Keyboard.delete())
    bot.register_next_step_handler(message, plus_date)

# Шаг 3 - дата
def plus_date(message):
    storage.set_storage_data(message, "user_date", message.text)
    bot.reply_to(message, "Запись завершена", reply_markup=Keyboard.v1())
    make_result(message)

# Результат записи на услугу
def make_result(message):
    user_name = storage.get_storage_data(message, "user_name")
    user_service = storage.get_storage_data(message, "user_service")
    user_date = storage.get_storage_data(message, "user_date")
    username = message.from_user.username

    text = f"Большое спасибо! 👍 \nВаше имя: {user_name} \nУслуга: {user_service} \nДата: {user_date} \nПользователь: @{username}"
    bot.send_message(message.chat.id, text)

# Конец скрипта
if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()