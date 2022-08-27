# -*- coding: utf-8 -*-
import telebot
import params
import storage
import datetime

from telebot import types
from keyboards import Keyboard
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

# Настройки бота
token = params.getToken()
bot = telebot.TeleBot(token)

# Настройки календаря
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1 = CallbackData('calendar_1', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()


# Стартовая команда при первом запуске
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Добро пожаловать ✌️", reply_markup=Keyboard.v1())


# Обработка сообщений
@bot.message_handler()
def start(message):
    storage.init_storage(message.from_user.id)
    if message.text in ['Запись 📝', 'Запись', 'запись']:
        making_user_record(message)
    else:
        bot.send_message(message.chat.id, "Не знаю что на это ответить", reply_markup=Keyboard.v1())


# Создание записи на услугу
def making_user_record(message):
    storage.set_storage_data(message.from_user.id, "user_nickname", message.from_user.username)
    bot.send_message(message.chat.id, "✏️ Введите ваше имя:", reply_markup=Keyboard.delete())
    bot.register_next_step_handler(message, plus_name)


# Шаг 1 - запись имени
def plus_name(message):
    storage.set_storage_data(message.from_user.id, "user_name", message.text)
    bot.reply_to(message, "Приятно познакомиться! Выберите услугу:", reply_markup=Keyboard.v2())
    bot.register_next_step_handler(message, plus_service)


# Шаг 2 - запись услуги
def plus_service(message):
    storage.set_storage_data(message.from_user.id, "user_service", message.text)
    bot.send_message(message.chat.id, "🗓 Интерактивный календарь:", reply_markup=calendar.create_calendar(name=calendar_1.prefix, year=now.year, month=now.month))
    plus_date(message)


# Шаг 3 - выбор даты
def plus_date(message):
    user_date = storage.get_storage_data(message.from_user.id, "user_date")
    if user_date == 'Не выбрано':
        bot.send_message(message.chat.id, "Выберите дату из меню выше", reply_markup=Keyboard.delete())
        bot.register_next_step_handler(message, plus_date)
        return
    elif message.text in ['Отмена', 'отмена']:
        delete_user_record(message.from_user.id)
    else:
        make_result(message)


# Шаг 4 - обработка календаря 
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1.prefix))
def callback_inline(call: types.CallbackQuery):
    chat_id = call.from_user.id
    name, action, year, month, day = call.data.split(calendar_1.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
    
    if action == 'DAY':
        storage.set_storage_data(chat_id, "user_date", date.strftime("%d.%m.%Y"))
        bot.send_message(chat_id, text=f'Вы выбрали {date.strftime("%d.%m.%Y")} \nЕсть ли у Вас дополнительные пожелания? 🤔', reply_markup=Keyboard.delete())
    elif action == 'CANCEL':
        delete_user_record(chat_id)
        

# Результат записи на услугу
def make_result(message):
    storage.set_storage_data(message.from_user.id, "user_comment", message.text)
    bot.reply_to(message, "Запись завершена", reply_markup=Keyboard.v1())
    
    user_name = storage.get_storage_data(message.from_user.id, "user_name")
    user_service = storage.get_storage_data(message.from_user.id, "user_service")
    user_date = storage.get_storage_data(message.from_user.id, "user_date")
    user_nickname = storage.get_storage_data(message.from_user.id, "user_nickname")
    user_comment = storage.get_storage_data(message.from_user.id, "user_comment")

    text = f"Большое спасибо! 👍 \nВаше имя: {user_name} \nУслуга: {user_service} \nДата: {user_date} \nКомментарий: {user_comment} \nПользователь: @{user_nickname}"
    bot.send_message(message.chat.id, text)


# Отмена записи
def delete_user_record(chat_id):
    bot.send_message(chat_id, "Запись отменена", reply_markup=Keyboard.v1())


# Конец скрипта
if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()