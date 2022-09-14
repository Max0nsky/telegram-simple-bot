import pymysql.cursors

connection = pymysql.connect(host='localhost', user='root', password='', database='cms-telegram', cursorclass=pymysql.cursors.DictCursor)