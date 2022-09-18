import params
import Db.db as db

connection = db.connection

salon_info = {}
services = {}
masters = {}
address = {}
times = {}

with connection:
    with connection.cursor() as cursor:

        token = params.getToken()
        cur = connection.cursor()
        cur.execute("SELECT * FROM user WHERE status = 10 AND tg_token = %s", token)
        user_tg = cur.fetchall()[0]
        user_id = user_tg['id']
        
        # Установка текста о компании
        tg_info_text = user_tg['tg_info_text']
        contents = tg_info_text.replace(r'\n', '\n')
        salon_info['name'] = {contents}

        # Установка времени по умолчанию
        times['time_1'] = {'name': user_tg['time_1']}
        if user_tg['time_2'] != "":
            times['time_2'] = {'name': user_tg['time_2']}
        if user_tg['time_3'] != "":
            times['time_3'] = {'name': user_tg['time_3']}
        if user_tg['time_4'] != "":
            times['time_4'] = {'name': user_tg['time_4']}
        if user_tg['time_5'] != "":
            times['time_5'] = {'name': user_tg['time_5']}

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

        # Установка филиалов
        cur = connection.cursor()
        cur.execute("SELECT * FROM address WHERE is_delete = 0 AND user_id = %s", user_id)
        all_address_db = cur.fetchall()
        for address_db in all_address_db:
            key_address = str(address_db['id'])
            name_address = str(address_db['name'])
            address[key_address] = {
                'name': name_address,
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