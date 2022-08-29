from telebot import types

class Keyboard:

    # Удаление клавиатуры
    @staticmethod
    def delete():
        return types.ReplyKeyboardRemove()

    # Стандартная клавиатура записи
    @staticmethod
    def v1():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["Запись 📝"])
        keyboard.add(*["О салоне 🗺", "Мастера 🙎‍♀️"])
        return keyboard

    # Клавиатура со списком услуг
    @staticmethod
    def v2():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*["✔️ Услуга 1"])
        keyboard.add(*["✔️ Услуга 2"])
        keyboard.add(*["✔️ Услуга 3"])
        keyboard.add(*["✔️ Услуга 4"])
        return keyboard