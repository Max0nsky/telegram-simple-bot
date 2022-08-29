# -*- coding: utf-8 -*-
from unicodedata import name
import telebot
import params
import datetime
import Storage.storage as storage
import Masters.masters as masters

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
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}! Добро пожаловать ✌️", reply_markup=Keyboard.v1())


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
    else:
        bot.reply_to(message, "Не знаю что на это ответить:", reply_markup=Keyboard.v1())


# Вывод списка мастеров
def send_masters_list(message):
    list_masters = masters.get_masters_list()
    for key in list_masters.keys():
        caption = list_masters[key]['name']
        image = open(list_masters[key]['image'], 'rb')
        bot.send_photo(message.chat.id, image, caption=caption, reply_markup=Keyboard.v1())


# Вывод информации о салоне
def send_information_about(message):
    bot.send_message(message.chat.id, "🙋‍♀️<b>Привет! Меня зовут Фамилия Имя Отчество!</b>\n Краткое описание вида деятельности\n Краткое описание услуг и т.д.\n\n <a href='https://yandex.ru/maps/-/CCUVIMELcD'>🗺 Воронеж, ул.Пушкина, д.40</a>" ,parse_mode='HTML', reply_markup=Keyboard.v1())
    
        
# Создание записи на услугу
def making_user_record(message):
    storage.set_storage_data(message.from_user.id, "user_nickname", message.from_user.username)
    bot.send_message(message.chat.id, "✏️ Введите ваше имя:", reply_markup=Keyboard.delete())
    bot.register_next_step_handler(message, plus_name)


# Шаг 1 - запись имени
def plus_name(message):
    storage.set_storage_data(message.from_user.id, "user_name", message.text)
    bot.reply_to(message, "✔️ Приятно познакомиться! Выберите услугу:", reply_markup=Keyboard.v2())
    bot.register_next_step_handler(message, plus_service)


# Шаг 2 - запись услуги
def plus_service(message):
    storage.set_storage_data(message.from_user.id, "user_service", message.text)
    bot.send_message(message.chat.id, "🗓 Интерактивный календарь для выбора даты:", reply_markup=calendar.create_calendar(name=calendar_rec.prefix, year=now.year, month=now.month))
    plus_date(message)


# Шаг 3 - выбор даты
def plus_date(message):
    user_date = storage.get_storage_data(message.from_user.id, "user_date")
    if user_date == storage.EMPTY_VALUE:
        bot.send_message(message.chat.id, "Выберите дату из меню выше", reply_markup=Keyboard.delete())
        bot.register_next_step_handler(message, plus_date)
        return
    elif message.text in ['Отмена', 'отмена']:
        delete_user_record(message.from_user.id)
    else:
        make_result(message)


# Шаг 4 - обработка календаря 
@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_rec.prefix))
def callback_inline(call: types.CallbackQuery):
    chat_id = call.from_user.id
    name, action, year, month, day = call.data.split(calendar_rec.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
    
    if action == 'DAY':
        storage.set_storage_data(chat_id, "user_date", date.strftime("%d.%m.%Y"))
        bot.send_message(chat_id, text=f'Вы выбрали {date.strftime("%d.%m.%Y")}. Как мы можем с вами связаться? 🤔\n'
                                        'Можете оставить номер телефона или комментарий:', reply_markup=Keyboard.delete())
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

    text = (
        f"""
        Большое спасибо! 👍
        Ваше имя: {user_name}
        Услуга: {user_service}
        Дата: {user_date}
        Комментарий: {user_comment}
        Пользователь: @{user_nickname}
        """
    )
    bot.send_message(message.chat.id, text)

# Отмена записи
def delete_user_record(chat_id):
    storage.init_storage(chat_id)
    bot.send_message(chat_id, "Запись отменена", reply_markup=Keyboard.v1())


# Конец скрипта
if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()