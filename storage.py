storage = {}

# Структура собираемых данных
def init_storage(chat_id):
    storage[chat_id] = dict(
        user_nickname=dict(value='Нет'),
        user_name=dict(value='Нет'),
        user_service=dict(value='Нет'),
        user_date=dict(value='Нет'),
        user_comment=dict(value='Нет'),
    )

# Установить значение по ключу
def set_storage_data(chat_id, key, value):
    storage[chat_id][key] = dict(value=value)

# Получить значение по ключу
def get_storage_data(chat_id, key):
    return storage[chat_id][key].get('value')