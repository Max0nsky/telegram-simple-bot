storage = {}

# Структура собираемых данных
def init_storage(message):
    storage[message.from_user.id] = dict(user_name=None, user_service=None, user_date=None)

# Установить значение по ключу
def set_storage_data(message, key, value):
    storage[message.from_user.id][key] = dict(value=value)

# Получить значение по ключу
def get_storage_data(message, key):
    return storage[message.from_user.id][key].get('value')
