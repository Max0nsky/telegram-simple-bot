storage = {}

EMPTY_VALUE = 'Нет'

# Структура собираемых данных
def init_storage(chat_id):
    storage[chat_id] = dict(
        user_nickname       = EMPTY_VALUE,
        user_name           = EMPTY_VALUE,
        user_master         = EMPTY_VALUE,
        user_master_key     = EMPTY_VALUE,
        user_address        = EMPTY_VALUE,
        user_service        = EMPTY_VALUE,
        user_service_key    = EMPTY_VALUE,
        user_date           = EMPTY_VALUE,
        user_time           = EMPTY_VALUE,
        user_comment        = EMPTY_VALUE,
    )

# Установить значение по ключу
def set_storage_data(chat_id, key, value):
    storage[chat_id][key] = value

# Получить значение по ключу
def get_storage_data(chat_id, key):
    return storage[chat_id][key]