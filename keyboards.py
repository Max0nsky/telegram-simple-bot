from telebot import types


class Keyboard:

    @staticmethod
    def delete():
        return types.ReplyKeyboardRemove()
    
    @staticmethod
    def v1():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Запись"))
        return keyboard

    @staticmethod
    def v2():
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton("Услуга 1"))
        keyboard.add(types.KeyboardButton("Услуга 2"))
        keyboard.add(types.KeyboardButton("Услуга 3"))
        keyboard.add(types.KeyboardButton("Услуга 4"))
        return keyboard