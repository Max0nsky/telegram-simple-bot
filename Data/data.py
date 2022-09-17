import params
import Db.db as db

connection = db.connection

services = {}
masters = {}

with connection:
    with connection.cursor() as cursor:

        token = params.getToken()
        cur = connection.cursor()
        cur.execute("SELECT * FROM user WHERE status = 10 AND tg_token = %s", token)
        user_tg = cur.fetchall()
        user_id = user_tg[0]['id']

        # Установка услуг
        cur = connection.cursor()
        cur.execute("SELECT * FROM services WHERE is_delete = 0 AND user_id = %s", user_id)
        services_db = cur.fetchall()
        for service in services_db:
            key_service = str(service['id'])
            
            services[key_service] = {
                'name': service['name'],
                'description': service['description'],
            }

        # Установка мастеров
        cur = connection.cursor()
        cur.execute("SELECT * FROM masters WHERE is_delete = 0 AND user_id = %s", user_id)
        masters_db = cur.fetchall()
        for master in masters_db:
            key_master = str(master['id'])
            
            masters[key_master] = {
                'name': master['name'],
                'image': master['image_path'],
                'description': master['description'],
                'services': {}
            }
            
        # Установка услуг мастеров
        cur = connection.cursor()
        cur.execute("SELECT * FROM masters_services")
        masters_services_db = cur.fetchall()
        for masters_service in masters_services_db:
            key_master = str(masters_service['master_id'])
            key_service = str(masters_service['service_id'])
            if key_master in masters:
                masters[key_master]['services'][key_service] = key_service

# TODO - доделать
# Филиалы
address = {
    "address_1": {
        "name": "Воронеж, ул. Сорокина, д. 5",
    },
    "address_2": {
        "name": "Воронеж, ул. Лермонтова, д. 10",
    },
    "address_3": {
        "name": "Воронеж, ул. Маяковского, д. 15",
    },
}

# TODO - доделать
# Рабочее время
times = {
    "time_1": {
        "name": "09:00 - 12:00",
    },
    "time_2": {
        "name": "12:00 - 18:00",
    },
    "time_3": {
        "name": "18:00 - 21:00",
    },
}

# TODO - доделать
# Информация о салоне
salon_info = {
    "name": {
        "🙋‍♀️<b>Привет! Меня зовут Фамилия Имя Отчество!</b>\n Краткое описание вида деятельности\n Краткое описание услуг и т.д.\n\n <a href='https://yandex.ru/maps/-/CCUVIMELcD'>🗺 Воронеж, ул.Пушкина, д.40</a>",
    },
}

def get_masters_list():
    return masters

def get_services_list():
    return services

def get_address_list():
    return address

def get_times_list():
    return times

def get_salon_info():
    return salon_info