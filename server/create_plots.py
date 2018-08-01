#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import configparser
import logging
import numpy as np
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mysql.connector
from mysql.connector import errorcode

import locale
for lang in ('de_DE', 'de_DE.utf8', 'de_CH', 'de_CH.utf8'):
    try:
        locale.setlocale(locale.LC_ALL, lang)
        break
    except Exception:
        pass


import random

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s\t%(levelname)s\t[%(name)s: %(funcName)s]\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler("logs/create_plots.log"), logging.StreamHandler()])

# setting of global minimum logging level
logging.disable(logging.DEBUG)

# set-up for logging of main. Level options: DEBUG, INFO, WARNING, ERROR, CRITICAL
loglevel = logging.DEBUG
logtitle = 'main'
logger = logging.getLogger(logtitle)
logger.setLevel(loglevel)

logger.info('started at '+time.strftime('%d.%m.%y, %H:%M'))







config = configparser.SafeConfigParser()
config.read('settings.ini')


try:
  dbcn = mysql.connector.connect(user=str(config['general']['mysql_user']), password=str(config['general']['mysql_password']), host='localhost', database='vcs_automat')
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Username or password wrong")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    sys.exit()

db = dbcn.cursor()
db.execute("SELECT unixtime FROM archive")

raw_data = [unixtime for (unixtime,) in db]

dbcn.close()



YEAR = datetime.now().year
SIZE = (6, 4.5)
COLOR = 'gray'


def set_title(plt, text):
    plt.suptitle(text)
    plt.title('aktualisiert '+time.strftime('%d.%m.%y, %H:%M'), fontdict={'fontsize': 8}, color='gray')




months = mdates.MonthLocator()
monthsFmt = mdates.DateFormatter('1. %b')

data = [{'hour': int(i.strftime('%H')), 'weekday': int(i.strftime('%w')), 'week': int(i.strftime('%W')), 'year': int(i.strftime('%Y'))} for i in map(datetime.fromtimestamp, raw_data)]

hours = np.array([sum(entry.get('hour') == i for entry in data) for i in range(0,23+1)])
weekdays = np.array([sum(entry.get('weekday') == i for entry in data) for i in range(0,6+1)])
weeks = np.array([sum(entry.get('year') == YEAR and entry.get('week') == j for entry in data) for j in range(0,56+1)])



#
# BASED ON WEEKDAYS
#
fig, ax = plt.subplots()
fig.set_size_inches(SIZE)
weekdays_title = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
ax.bar(weekdays_title, weekdays/sum(weekdays)*100, color=COLOR)
fig.autofmt_xdate()
plt.ylabel('relativer Konsum [%]')
set_title(plt, 'Durchschnittlicher Konsum nach Wochentag')
plt.savefig('img/weekday.svg', transparent=True)
plt.close()


#
# BASED ON HOUR OF THE DAY
#
fig, ax = plt.subplots()
fig.set_size_inches(SIZE)
ax.bar(range(0,23+1), hours/sum(hours)*100, align='edge', color=COLOR)
ax.set_xlim(0, 24)
ax.set_xticks([1,2,4,5,7,8,10,12,14,16,17,19,20,22,23], minor=True)
plt.xticks((0,3,6,9,12,15,18,21,24))
plt.ylabel('relativer Konsum [%]')
set_title(plt, 'Durschnittlicher Konsum nach Uhrzeit')
plt.savefig('img/hour.svg', transparent=True)
plt.close()


#
# WEEKLY CONSUMPTION THIS YEAR
#
fig, ax = plt.subplots()
fig.set_size_inches(SIZE)

first_day = date(YEAR, 1, 1)
last_day = date(YEAR, 12, 31)
monday_of_week_zero = first_day - timedelta(days = first_day.weekday())
weeknumber_start = 0 if first_day.weekday() > 0 else 1
weeknumber_end = int(last_day.strftime('%W'))

x = range(int(mdates.date2num(monday_of_week_zero)), int(mdates.date2num(last_day))+1, 7)
y = weeks[weeknumber_start:weeknumber_end+1]
ax.bar(x, y, width=6, align='edge', color=COLOR)

ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('1. %b'))
fig.autofmt_xdate()

ax.set_xlim(int(mdates.date2num(datetime(YEAR, 1, 1))), int(mdates.date2num(datetime(YEAR, 12, 31))))
plt.ylabel('Gesamtkonsum')
set_title(plt, 'Wöchentlicher Konsum in '+str(YEAR))
plt.savefig('img/year_'+str(YEAR)+'.svg', transparent=True)
plt.close()
