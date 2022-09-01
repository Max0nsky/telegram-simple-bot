from telebot import types
import Data.data as data

class Keyboard:

    # Удаление клавиатуры
    @staticmethod
    def delete():
        return types.ReplyKeyboardRemove()

    # Кнопка отмены
    @staticmethod
    def cancel():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Отмена"])
        return keyboard


    # Стандартная клавиатура записи
    @staticmethod
    def default():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Запись 📝"])
        keyboard.add(*["О салоне 🗺", "Консультация ❔", "Мастера 🙎‍♀️"])
        return keyboard


    # Клавиатура со списком услуг
    @staticmethod
    def service(master_key = None):
        list_masters = data.get_masters_list()
        list_services = data.get_services_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if master_key in list_masters:
            # Динамическая клавиатура услуг мастера
            for service in list_masters[master_key]['services']:
                keyboard.add(*[list_services[service]['name']])
        else:
            # Клавиатура услуг по умолчанию
            for service in list_services.values():
                keyboard.add(*[service['name']])

        keyboard.add(*["Подробнее", "Отмена"])

        return keyboard


    # Клавиатура со списком адресов
    @staticmethod
    def address():
        list_address = data.get_address_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for address in list_address.values():
            keyboard.add(*[address['name']])
        keyboard.add(*["Отмена"])
        return keyboard


    # Клавиатура со списком временных промежутков
    @staticmethod
    def times():
        list_times = data.get_times_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for times in list_times.values():
            keyboard.add(*[times['name']])
        keyboard.add(*["Отмена"])
        return keyboard


    # Клавиатура со списком мастеров (перебор из masters)
    @staticmethod
    def masters():
        list_masters = data.get_masters_list()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for masters in list_masters.values():
            keyboard.add(*[masters['name']])
        return keyboard