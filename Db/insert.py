import Db.db as db
import params

from calendar import calendar
from time import time

connection = db.connection

def get_admin_id():
    connection.ping() 
    token = params.getToken()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user WHERE status = 10 AND tg_token = %s", token)
    user_tg = cursor.fetchall()
    user_id = user_tg[0]['id']
    return user_id

def create_order(chat_id, user_nickname, user_name, user_master, user_master_key, user_address, user_service, user_service_key, user_date, user_time, user_comment):
    connection.ping() 
    user_id = get_admin_id()
    cursor = connection.cursor()
    date = int(time())
    sql = "INSERT INTO `order` (`user_id`, `chat_id`, `user_nickname`, `user_name`, `user_master`, `user_master_key`, `user_address`, `user_service`, `user_service_key`, `user_date`, `user_time`, `user_comment`, `date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, chat_id, user_nickname, user_name, user_master, user_master_key, user_address, user_service, user_service_key, user_date, user_time, user_comment, date))
    connection.commit()
    cursor.close()

def create_order_consultation(chat_id, user_nickname, user_name, user_comment):
    connection.ping() 
    user_id = get_admin_id()
    cursor = connection.cursor()
    date = int(time())
    sql = "INSERT INTO `order_consultation` (`user_id`, `chat_id`, `user_nickname`, `user_name`, `user_comment`, `date`) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (user_id, str(chat_id), str(user_nickname), str(user_name), str(user_comment), date))
    connection.commit()
    cursor.close()
    
def create_or_check_user(chat_id, username, first_name, last_name):
    connection.ping() 
    user_id = get_admin_id()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_telegram WHERE user_id = %s AND chat_id = %s", (user_id, str(chat_id)))
    user_chat_tg = cursor.fetchall()
    if len(user_chat_tg) == 0:        
        cursor = connection.cursor()
        date = int(time())
        sql = "INSERT INTO `user_telegram` (`user_id`, `chat_id`, `username`, `first_name`, `last_name`, `date`) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, str(chat_id), str(username), str(first_name), str(last_name), date))
        connection.commit()
    cursor.close()