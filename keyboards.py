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
        keyboard.add(*["Запись 📝", "Контакты 🗺"])
        return keyboard

    # Клавиатура со списком услуг
    @staticmethod
    def v2():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("✔️ Услуга 1"))
        keyboard.add(types.KeyboardButton("✔️ Услуга 2"))
        keyboard.add(types.KeyboardButton("✔️ Услуга 3"))
        keyboard.add(types.KeyboardButton("✔️ Услуга 4"))
        return keyboard