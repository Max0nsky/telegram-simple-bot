storage = {}

# Структура собираемых данных
def init_storage(chat_id):
    storage[chat_id] = dict(
        user_nickname=dict(value='Не выбрано'),
        user_name=dict(value='Не выбрано'),
        user_service=dict(value='Не выбрано'),
        user_date=dict(value='Не выбрано'),
        user_comment=dict(value='Не выбрано'),
    )

# Установить значение по ключу
def set_storage_data(chat_id, key, value):
    storage[chat_id][key] = dict(value=value)

# Получить значение по ключу
def get_storage_data(chat_id, key):
    return storage[chat_id][key].get('value')