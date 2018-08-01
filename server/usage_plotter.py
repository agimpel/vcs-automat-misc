import os.path
import logging
import time
import configparser
import logging
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
                    handlers=[logging.StreamHandler()])

# setting of global minimum logging level
logging.disable(logging.NOTSET)

# set-up for logging of main. Level options: DEBUG, INFO, WARNING, ERROR, CRITICAL
loglevel = logging.DEBUG
logtitle = 'main'
logger = logging.getLogger(logtitle)
logger.setLevel(loglevel)



def monday_of_week_one(yyyy):
    REF_DAY = date(yyyy, 1, 4)
    DOW = REF_DAY.weekday()
    MONDAY = REF_DAY - timedelta(days = DOW)
    return MONDAY


def set_title(plt, text):
    plt.suptitle(text)
    plt.title('aktualisiert '+time.strftime('%d.%m.%y, %H:%M'), fontdict={'fontsize': 8}, color='gray')




months = mdates.MonthLocator()  # every month
monthsFmt = mdates.DateFormatter('1. %b')

# Load a numpy record array from yahoo csv data with fields date, open, close,
# volume, adj_close from the mpl-data/example directory. The record array
# stores the date as an np.datetime64 with a day unit ('D') in the date column.

r = []
for i in range(900):
    r.append(random.randint(1483228800,1533112129))

data = []
for i in r:
    i_date = datetime.fromtimestamp(i)
    data.append({'hour': i_date.strftime('%H'), 'weekday': i_date.strftime('%w'), 'week':i_date.strftime('%W'), 'day': i_date.strftime('%d'), 'month':i_date.strftime('%m'), 'year':i_date.strftime('%Y')})


hours = []
for i in range(0,23+1):
    hours.append(sum(int(entry.get('hour')) == i for entry in data))


weekdays_title = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
weekdays = []
for i in range(0,6+1):
    weekdays.append(sum(int(entry.get('weekday')) == i for entry in data))


weekyears = np.zeros((datetime.now().year+1-2017, 54+1))
for i in range(2017, datetime.now().year+1):
    for j in range(0,54+1):
        weekyears[i-2017, j] = sum((int(entry.get('year')) == i and int(entry.get('week')) == j) for entry in data)


fig, ax = plt.subplots()
ax.bar(weekdays_title, [x/sum(weekdays)*100 for x in weekdays])
fig.autofmt_xdate()
plt.ylabel('relativer Konsum [%]')
set_title(plt, 'Durchschnittlicher Konsum nach Wochentag')
plt.show()


fig, ax = plt.subplots()
ax.bar(range(0,23+1), [x/sum(hours)*100 for x in hours], align='edge')
ax.set_xlim(0, 24)
ax.set_xticks([1,2,4,5,7,8,10,12,14,16,17,19,20,22,23], minor=True)
plt.xticks((0,3,6,9,12,15,18,21,24))
plt.ylabel('relativer Konsum [%]')
set_title(plt, 'Durschnittlicher Konsum nach Uhrzeit')
plt.show()



for i in range(2017, datetime.now().year+1):
    fig, ax = plt.subplots()
    weeknumber_start = int(datetime(i, 1, 1).strftime('%W'))
    weeknumber_end = int(datetime(i, 12, 31).strftime('%W'))

    if weeknumber_start is 0:
        x = range(int(mdates.date2num(monday_of_week_one(i)))-7, int(mdates.date2num(datetime(i, 12, 31))), 7)
    else:
        x = range(int(mdates.date2num(monday_of_week_one(i))), int(mdates.date2num(datetime(i, 12, 31)))+7, 7)
    ax.bar(x, weekyears[i-2017, weeknumber_start:weeknumber_end+1], width=6, align='edge')

    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(monthsFmt)
    fig.autofmt_xdate()

    datemin = int(mdates.date2num(datetime(i, 1, 1)))
    datemax = int(mdates.date2num(datetime(i, 12, 31)))
    ax.set_xlim(datemin, datemax)
    plt.ylabel('Gesamtkonsum')
    set_title(plt, 'Wöchentlicher Konsum in '+str(i))
    plt.show()













