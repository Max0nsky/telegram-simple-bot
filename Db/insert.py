import Db.db as db

from calendar import calendar
from time import time

connection = db.connection

def create_order(chat_id, user_nickname, user_name, user_master, user_master_key, user_address, user_service, user_service_key, user_date, user_time, user_comment):
    connection.ping() 
    cursor = connection.cursor()
    date = int(time())
    sql = "INSERT INTO `order` (`chat_id`, `user_nickname`, `user_name`, `user_master`, `user_master_key`, `user_address`, `user_service`, `user_service_key`, `user_date`, `user_time`, `user_comment`, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (chat_id, user_nickname, user_name, user_master, user_master_key, user_address, user_service, user_service_key, user_date, user_time, user_comment, date))
    connection.commit()
    cursor.close()

def create_order_consultation(chat_id, user_nickname, user_name, user_comment):
    connection.ping() 
    cursor = connection.cursor()
    date = int(time())
    print(chat_id, user_nickname, user_name, user_comment, date)
    sql = "INSERT INTO `order_consultation` (`chat_id`, `user_nickname`, `user_name`, `user_comment`, `date`) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (str(chat_id), str(user_nickname), str(user_name), str(user_comment), date))
    connection.commit()
    cursor.close()