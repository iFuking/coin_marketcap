"""
Config imported by flask_mysql.py
"""
import os

dbhost = os.environ['MYSQL_URL']
dbuser = os.environ['MYSQL_USER_NAME']
dbpass = os.environ['MYSQL_PASSWORD']
dbname = os.environ['FLASK_DB']
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname
