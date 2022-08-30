from telebot import types
import Masters.masters as masters

class Keyboard:

    # Удаление клавиатуры
    @staticmethod
    def delete():
        return types.ReplyKeyboardRemove()


    # Стандартная клавиатура записи
    @staticmethod
    def default():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Запись 📝"])
        keyboard.add(*["О салоне 🗺", "Мастера 🙎‍♀️"])
        return keyboard


    # Клавиатура со списком услуг
    @staticmethod
    def service(master_key = None):
        list_masters = masters.get_masters_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if master_key in list_masters:
            # Динамическая клавиатура услуг мастера
            for service in list_masters[master_key]['services']:
                keyboard.add(*[service])
        else:
            # Клавиатура услуг по умолчанию
            keyboard.add(*["✔️ Услуга 1"])
            keyboard.add(*["✔️ Услуга 2"])
            keyboard.add(*["✔️ Услуга 3"])
            keyboard.add(*["✔️ Услуга 4"])
        return keyboard


    # Клавиатура со списком адресов
    @staticmethod
    def address():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Воронеж, ул. Сорокина, д. 5"])
        keyboard.add(*["Воронеж, ул. Лермонтова, д. 10"])
        keyboard.add(*["Воронеж, ул. Маяковского, д. 15"])
        return keyboard


    # Клавиатура со списком временных промежутков
    @staticmethod
    def times():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["09:00 - 12:00"])
        keyboard.add(*["12:00 - 18:00"])
        keyboard.add(*["18:00 - 21:00"])
        return keyboard


    # Клавиатура со списком мастеров (перебор из masters)
    @staticmethod
    def masters():
        list_masters = masters.get_masters_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for key in list_masters.keys():
            keyboard.add(*[list_masters[key]['name']])
        return keyboard