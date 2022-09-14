# -*- coding: utf-8 -*-
import telebot
import params
import datetime
import Storage.storage as storage
import Data.data as data
import Db.insert as insert

from telebot import types
from Keyboards.keyboards import Keyboard
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

# Настройки бота
token = params.getToken()
bot = telebot.TeleBot(token)

# Настройки календаря
calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_rec = CallbackData('calendar_rec', 'action', 'year', 'month', 'day')
now = datetime.datetime.now()


# Стартовая команда при первом запуске
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Добро пожаловать ✌️", reply_markup=Keyboard.default())


# Обработка сообщений
@bot.message_handler()
def start(message):
    storage.init_storage(message.from_user.id)
    if message.text in ['Запись 📝', 'Запись', 'запись']:
        making_user_record(message)
    elif message.text in ['О салоне 🗺', 'О салоне', 'о салоне']:
        send_information_about(message)
    elif message.text in ['Мастера 🙎‍♀️', 'Мастера', 'мастера']:
        send_masters_list(message)
    elif message.text in ['Консультация ❔', 'Консультация', 'консультация']:
        making_user_consultation(message)
    else:
        bot.reply_to(message, "Не знаю что на это ответить:", reply_markup=Keyboard.default())


# Вывод списка мастеров
def send_masters_list(message):
    list_masters = data.get_masters_list()
    for key in list_masters.keys():
        caption = list_masters[key]['name']
        image = open(list_masters[key]['image'], 'rb')
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Записаться", callback_data=key)
        keyboard.add(callback_button)
        bot.send_photo(message.chat.id, image, caption=caption, reply_markup=keyboard)


# Вывод информации о салоне
def send_information_about(message):
    bot.send_message(message.chat.id, data.salon_info['name'] ,parse_mode='HTML', reply_markup=Keyboard.default())
    

# Начало №1: Создание записи на услугу
def making_user_record(message):
    bot.send_message(message.chat.id, "✏️ Введите ваше имя:", reply_markup=Keyboard.cancel())
    bot.register_next_step_handler(message, plus_name)


# Шаг 1 - запись имени
def plus_name(message):
    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
    else:
        storage.set_storage_data(message.from_user.id, "user_nickname", message.from_user.username)
        storage.set_storage_data(message.from_user.id, "user_name", message.text)
        bot.reply_to(message, "Приятно познакомиться! Выберите филиал:", reply_markup=Keyboard.address())
        bot.register_next_step_handler(message, plus_address)


# Шаг 2 - запись филиала
def plus_address(message):
    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
    else:
        storage.set_storage_data(message.from_user.id, "user_address", message.text)
        user_master_key = storage.get_storage_data(message.from_user.id, "user_master_key")
        bot.reply_to(message, "✔️ Супер! Теперь выберите услугу:", reply_markup=Keyboard.service(user_master_key))
        bot.register_next_step_handler(message, plus_service)


# Шаг 3 - запись услуги
def plus_service(message):
    user_master_key = storage.get_storage_data(message.from_user.id, "user_master_key")
    storage.set_storage_data(message.from_user.id, "user_service", message.text)

    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
    elif message.text == 'Подробнее':
        list_services = data.get_services_list()
        list_masters = data.get_masters_list()
        if user_master_key == storage.EMPTY_VALUE:
            for service in list_services.values():
                text_service = service['name'] + ":\n" + service['description']
                bot.send_message(message.chat.id, text_service, reply_markup=Keyboard.service(user_master_key))
        else:
            for service in list_masters[user_master_key]['services']:
                text_service = list_services[service]['name'] + ":\n" + list_services[service]['description']
                bot.send_message(message.chat.id, text_service, reply_markup=Keyboard.service(user_master_key)) 
        bot.register_next_step_handler(message, plus_service)
    else:
        bot.send_message(message.chat.id, "🗓 Интерактивный календарь для выбора даты:", reply_markup=calendar.create_calendar(name=calendar_rec.prefix, year=now.year, month=now.month))
        plus_date(message)


# Шаг 4 - выбор даты
def plus_date(message):
    user_date = storage.get_storage_data(message.from_user.id, "user_date")
    if user_date == storage.EMPTY_VALUE:
        if message.text == 'Отмена':
            delete_user_record(message.from_user.id)
        else:
            bot.send_message(message.chat.id, "Выберите дату из меню выше", reply_markup=Keyboard.cancel())
            bot.register_next_step_handler(message, plus_date)
    else:
        plus_time(message)

    
# Шаг 4.1 - обработка календаря
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_rec.prefix))
def callback_inline(call: types.CallbackQuery):
    chat_id = call.from_user.id
    name, action, year, month, day = call.data.split(calendar_rec.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
    
    if action == 'DAY':
        storage.set_storage_data(chat_id, "user_date", date.strftime("%d.%m.%Y"))
        bot.send_message(chat_id, text=f'Вы выбрали {date.strftime("%d.%m.%Y")}. Теперь выберите время:', reply_markup=Keyboard.times())
    elif action == 'CANCEL':
        delete_user_record(chat_id)


# Шаг 5 - выбор времени, запись комментария
def plus_time(message):
    storage.set_storage_data(message.from_user.id, "user_time", message.text)
    bot.send_message(message.from_user.id, text="Как мы можем с вами связаться? 🤔\nМожете оставить телефон или комментарий:", reply_markup=Keyboard.cancel())
    bot.register_next_step_handler(message, make_result)


# Обработка callback_inline
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    list_masters = data.get_masters_list()
    callback_data = call.data
    message = call.message
    
    if callback_data in list_masters:
        storage.set_storage_data(message.chat.id, "user_master", list_masters[callback_data]['name'])
        storage.set_storage_data(message.chat.id, "user_master_key", callback_data)
        making_user_record(message)


# Результат записи на услугу
def make_result(message):
    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
        return

    storage.set_storage_data(message.from_user.id, "user_comment", message.text)
    bot.reply_to(message, "Запись завершена", reply_markup=Keyboard.default())
    
    chat_id = message.from_user.id
    user_name = storage.get_storage_data(message.from_user.id, "user_name")
    user_master = storage.get_storage_data(message.from_user.id, "user_master")
    user_master_key = storage.get_storage_data(message.from_user.id, "user_master_key")
    user_address = storage.get_storage_data(message.from_user.id, "user_address")
    user_service = storage.get_storage_data(message.from_user.id, "user_service")
    user_service_key = storage.get_storage_data(message.from_user.id, "user_service_key")
    user_date = storage.get_storage_data(message.from_user.id, "user_date")
    user_time = storage.get_storage_data(message.from_user.id, "user_time")
    user_nickname = storage.get_storage_data(message.from_user.id, "user_nickname")
    user_comment = storage.get_storage_data(message.from_user.id, "user_comment")

    insert.create_order(chat_id, user_nickname, user_name, user_master, user_master_key, user_address, user_service, user_service_key, user_date, user_time, user_comment)

    text = (
    f"""
    Большое спасибо! 👍
    Ваше имя: {user_name}
    Мастер: {user_master}
    Адрес: {user_address}
    Услуга: {user_service}
    Дата: {user_date}
    Время: {user_time}
    Комментарий: {user_comment}
    Пользователь: @{user_nickname}
    """
    )
    
    bot.send_message(message.chat.id, text)
    


# Начало №2: Создание записи на консультацию
def making_user_consultation(message):
    bot.send_message(message.chat.id, "✏️ Введите ваше имя:", reply_markup=Keyboard.cancel())
    bot.register_next_step_handler(message, plus_consultation_name)


# Шаг 1 - запись имени, комментария
def plus_consultation_name(message):
    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
        return
    
    storage.set_storage_data(message.from_user.id, "user_nickname", message.from_user.username)
    storage.set_storage_data(message.from_user.id, "user_name", message.text)
    bot.reply_to(message, "Как мы можем с вами связаться? 🤔\nМожете оставить телефон или комментарий::", reply_markup=Keyboard.cancel())
    bot.register_next_step_handler(message, make_result_consultation)


# Результат записи на консультацию
def make_result_consultation(message):
    if message.text == 'Отмена':
        delete_user_record(message.from_user.id)
        return

    storage.set_storage_data(message.from_user.id, "user_comment", message.text)
    bot.reply_to(message, "Запись на консультацию завершена", reply_markup=Keyboard.default())
    
    chat_id = message.from_user.id
    user_name = storage.get_storage_data(message.from_user.id, "user_name")
    user_nickname = storage.get_storage_data(message.from_user.id, "user_nickname")
    user_comment = storage.get_storage_data(message.from_user.id, "user_comment")

    insert.create_order_consultation(chat_id, user_nickname, user_name, user_comment)

    text = (
    f"""
    Запись на консультацию! 🧐
    Ваше имя: {user_name}
    Комментарий: {user_comment}
    Пользователь: @{user_nickname}
    """
    )
    
    bot.send_message(message.chat.id, text)


# Отмена записи
def delete_user_record(chat_id):
    storage.init_storage(chat_id)
    bot.send_message(chat_id, "Запись отменена", reply_markup=Keyboard.default())


# Конец скрипта
if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()