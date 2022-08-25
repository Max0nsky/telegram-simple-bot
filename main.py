import telebot
import params

from telebot import types


token = params.getToken()
bot = telebot.TeleBot(token)
storage = {}


@bot.message_handler(commands=['start'])
def start_message(message):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Запись ✏️")
    button2 = types.KeyboardButton("Информация ❓")
    keyboard.add(button1)
    keyboard.add(button2)

    bot.send_message(message.chat.id, "Привет, {0.first_name}! Добро пожаловать ✌️".format(
        message.from_user), reply_markup=keyboard)


def init_storage(user_id):
    storage[user_id] = dict(user_name=None, user_age=None)


def set_store_data(user_id, key, value):
    storage[user_id][key] = dict(value=value)


def get_element_storage(user_id, key):
    return storage[user_id][key].get('value')


@bot.message_handler()
def start(message):
    init_storage(message.from_user.id)

    list_check_record = ['Запись', 'запись', 'Запись ✏️']
    list_check_info = ['Информация', 'информация', 'Информация ❓']

    if message.text in list_check_record:
        making_user_record(message)
    elif message.text in list_check_info:
        bot.send_message(
            message.chat.id, "Какая-то информация...", parse_mode='html')
    else:
        bot.reply_to(message, "Не понимаю, вы о чём? 🤷‍♂️")
        bot.send_message(
            message.chat.id, "Введите 'Запись' для записи", parse_mode='html')


def making_user_record(message):
    bot.send_message(message.chat.id, "Введите ваше имя:", parse_mode='html')
    bot.register_next_step_handler(message, plus_name)


def plus_name(message):
    user_name = message.text
    set_store_data(message.from_user.id, "user_name", user_name)
    bot.reply_to(message, "Отлично! Теперь введите ваш возраст:")
    bot.register_next_step_handler(message, plus_age)


def plus_age(message):
    user_age = message.text

    if not user_age.isdigit():
        bot.reply_to(message, 'Попробуйте снова. Тут что-то не так 🧐')
        bot.register_next_step_handler(message, plus_age)
        return

    set_store_data(message.from_user.id, "user_age", user_age)
    make_answer(message)


def make_answer(message):
    bot.send_message(
        message.chat.id, "Передаём данные в базу данных", parse_mode='html')

    user_name = get_element_storage(message.from_user.id, "user_name")
    user_age = get_element_storage(message.from_user.id, "user_age")

    bot.send_message(
        message.chat.id, f"Большое спасибо!👍 \nВаше имя: {user_name} \nВаш возраст: {user_age} \n")


if __name__ == '__main__':
    bot.skip_pending = True
    bot.polling(none_stop=True)
    bot.infinity_polling()
