# coding=utf-8

import logging
from apscheduler.schedulers.background import BackgroundScheduler
from install_data import install_bulk_data

log = logging.getLogger('schedule_job')


def daily_job():
    install_bulk_data()
    clean_func()

def schedule_job():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(tick, 'interval', seconds=3)
    # scheduler.add_job(tick, 'date', run_date='2016-02-14 15:01:05')
    scheduler.add_job(daily_job, 'cron', day="*", hour='1')
    '''
        year (int|str) – 4-digit year
        month (int|str) – month (1-12)
        day (int|str) – day of the (1-31)
        week (int|str) – ISO week (1-53)
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        hour (int|str) – hour (0-23)
        minute (int|str) – minute (0-59)
        second (int|str) – second (0-59)

        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

        *    any    Fire on every value
        */a    any    Fire every a values, starting from the minimum
        a-b    any    Fire on any value within the a-b range (a must be smaller than b)
        a-b/c    any    Fire every c values within the a-b range
        xth y    day    Fire on the x -th occurrence of weekday y within the month
        last x    day    Fire on the last occurrence of weekday x within the month
        last    day    Fire on the last day within the month
        x,y,z    any    Fire on any matching expression; can combine any number of any of the above expressions
    '''
    scheduler.start()


def clean_func(path):

    import os
    dirs = os.listdir(path)
    count = 0
    for fn in dirs:
        count += 1
    if count > 7:
        date_list = []
        for dir in dirs:
            date_list.append(dir)
        if len(date_list) > 7:
            date_list.sort(reverse=True)
            tmp = date_list[7:]
            for i in tmp:
                os.rmdir(path + '/' + i)



if __name__ == '__main__':
    path = "/data_server/data/CAAS"
    clean_func(path)
