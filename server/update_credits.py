#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0, current_dir)
import time
import configparser
import logging
from datetime import datetime, date, timedelta
import mysql.connector
from mysql.connector import errorcode

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s\t%(levelname)s\t[%(name)s: %(funcName)s]\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("logs/update_credits.log"), logging.StreamHandler()])

# setting of global minimum logging level
logging.disable(logging.DEBUG)

# set-up for logging of main. Level options: DEBUG, INFO, WARNING, ERROR, CRITICAL
loglevel = logging.DEBUG
logtitle = 'main'
logger = logging.getLogger(logtitle)
logger.setLevel(loglevel)

logger.info('started at '+time.strftime('%d.%m.%y, %H:%M'))



CHECK_TIMEDELTA = 3590 #seconds






def get_setting(db, name):
    try:
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT value FROM settings WHERE name = '"+str(name)+"'")
    except mysql.connector.Error as e:
        print(e)
        return None
    return (cursor.fetchone())[0]

def set_setting(db, name, value):
    try:
        cursor = db.cursor(buffered=True)
        cursor.execute("UPDATE settings SET value = '"+str(value)+"' WHERE name = '"+str(name)+"'")
        db.commit()
    except mysql.connector.Error as e:
        print(e)
        return None
    return

def update_credits(db, credits):
    try:
        cursor = db.cursor(buffered=True)
        cursor.execute("UPDATE users SET credits = '"+str(credits)+"'")
        db.commit()
    except mysql.connector.Error as e:
        print(e)
        return None
    return


config = configparser.SafeConfigParser()
config.read('settings.ini')


try:
  dbcn = mysql.connector.connect(user=str(config['general']['mysql_user']), password=str(config['general']['mysql_password']), host='localhost', database='vcs_automat')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logger.error("Username or password wrong")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logger.error("Database does not exist")
    else:
        print(err)
    sys.exit()

db = dbcn.cursor()



next_reset = int(get_setting(dbcn, 'next_reset'))
logger.info('Next reset is set to '+str(next_reset)+' corresponding to '+time.strftime('%d.%m.%Y, %H:%M', time.localtime(next_reset)))

last_reset = int(get_setting(dbcn, 'last_reset'))
logger.info('Last reset is set to '+str(last_reset)+' corresponding to '+time.strftime('%d.%m.%Y, %H:%M', time.localtime(last_reset)))

reset_interval = int(get_setting(dbcn, 'reset_interval'))*24*3600 #convert to seconds
logger.info('Reset interval is set to '+str(reset_interval))


if next_reset is not last_reset + reset_interval:
    next_reset = last_reset + reset_interval
    logger.info('Next reset does not correspond to last reset + reset interval, updating it to '+str(next_reset)+' corresponding to '+time.strftime('%d.%m.%Y, %H:%M', time.localtime(next_reset)))


if(int(time.time()) < next_reset - CHECK_TIMEDELTA):
    logger.info('No reset necessary. Dismissing.')
    dbcn.close()
    sys.exit()


logger.info('Reset is necessary. Processing database update.')

credits = int(get_setting(dbcn, 'standard_credits'))
update_credits(dbcn, credits)



upcoming_reset = next_reset + reset_interval
# current_reset = int(time.time())
current_reset = next_reset

logger.info('Changed next reset to '+str(upcoming_reset)+' corresponding to '+time.strftime('%d.%m.%Y, %H:%M', time.localtime(upcoming_reset)))

set_setting(dbcn, 'last_reset', current_reset)
set_setting(dbcn, 'next_reset', upcoming_reset)

dbcn.close()
