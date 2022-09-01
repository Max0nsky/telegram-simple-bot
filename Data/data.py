# Мастера
masters = {
    "master_1": {
        "name": "Имя Первого Мастера",
        "image": "images/master_1.png",
        "services": {
            "service_1",
            "service_2",
        },
    },
    "master_2": {
        "name": "Имя Второго Мастера",
        "image": "images/master_2.png",
        "services": {
            "service_1",
            "service_3",
        },
    },
    "master_3": {
        "name": "Имя Третьего Мастера",
        "image": "images/master_3.png",
        "services": {
            "service_2",
            "service_4",
        },
    },
}

# Услуги
services = {
    "service_1": {
        "name": "✔️ Услуга 1",
        "description": "Описание услуги 1",
    },
    "service_2": {
        "name": "✔️ Услуга 2",
        "description": "Описание услуги 2",
    },
    "service_3": {
        "name": "✔️ Услуга 3",
        "description": "Описание услуги 3",
    },
    "service_4": {
        "name": "✔️ Услуга 4",
        "description": "Описание услуги 4",
    },
}

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