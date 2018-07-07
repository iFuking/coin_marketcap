"""
Config imported by flask_mysql.py
"""
import os

dbhost = os.environ['DB_URL']
dbuser = os.environ['DB_USER_NAME']
dbpass = os.environ['DB_PASSWORD']
dbname = os.environ['FLASK_DB']
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' + dbname
