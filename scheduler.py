# This program will activate the script to run once a day at noon.
import os
import schedule
import time

def script():
    os.system('python get_jobs.py')

schedule.every().day.at("14:00").do(script)

while 1:
    schedule.run_pending()
    time.sleep(1)