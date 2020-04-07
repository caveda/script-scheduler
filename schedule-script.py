import argparse
import os
import re
import time
from os import path
from datetime import datetime
import schedule
from logger import init_logging, log

LOG_FILENAME = "schedule-script.log"
SUNDAY = "0"
MONDAY = "1"
TUESDAY = "2"
WEDNESDAY = "3"
THURSDAY = "4"
FRIDAY = "5"
SATURDAY = "6"
EVERY_DAY = SUNDAY + MONDAY + TUESDAY + WEDNESDAY + THURSDAY + FRIDAY + SATURDAY


def run_task(task):
    if not validate_task(task):
        log("Execution skipped")
        return
    log(f"Executing {task}")
    result = os.system(task)
    log(f"Execution result: {result}")


def validate_task(task_file):
    """ Validates task file """
    valid = path.exists(task_file) and path.isfile(task_file)
    if not valid:
        log(f"File {task_file} does not exists!!")
    return valid


def validate_weekdays(weekdays):
    """ Validates weekdays format """
    result = re.match("^0?1?2?3?4?5?6?$", weekdays) is not None
    if not result:
        log(f"Invalid weekdays format: {weekdays}!!")
    return result


def validate_time(time):
    """ Validates time format """
    try:
        datetime.strptime(time, '%H:%M')
        return True
    except ValueError:
        log(f"Invalid time format: {time}!!")
        return False


def set_schedule(time, weekdays, task):
    """ Sets the schedule passed as arguments"""
    if not validate_task(task) or \
            not validate_weekdays(weekdays) or \
            not validate_time(time):
        return False

    if weekdays == EVERY_DAY:
        schedule.every().day.at(time).do(run_task, task)
    else:
        schedule_only_some_days(task, time, weekdays)
    return True


def schedule_only_some_days(task, time, weekdays):
    """ Schedule the task only some specific days """
    if SUNDAY in weekdays:
        schedule.every().sunday.at(time).do(run_task, task)
    if MONDAY in weekdays:
        schedule.every().monday.at(time).do(run_task, task)
    if TUESDAY in weekdays:
        schedule.every().tuesday.at(time).do(run_task, task)
    if WEDNESDAY in weekdays:
        schedule.every().wednesday.at(time).do(run_task, task)
    if THURSDAY in weekdays:
        schedule.every().thursday.at(time).do(run_task, task)
    if FRIDAY in weekdays:
        schedule.every().friday.at(time).do(run_task, task)
    if SATURDAY in weekdays:
        schedule.every().saturday.at(time).do(run_task, task)


def parse_arguments():
    """ Digests arguments """
    parser = argparse.ArgumentParser(description="Runs a script or executable with the given schedule.")
    parser.add_argument("task", help="Path to the script or application to run.")
    parser.add_argument("time", help="Time when the script shall be executed expressed in format: HH:MM")
    parser.add_argument("--weekdays", help="Weeks of the day to execute the task expressed in numbers [0-6] where: \
                        0 is Sunday, 1 is Monday, and so forth.  e.g. 024 means Sundays,\
                        Tuesdays and Thursdays. Default value is 0123456 which means Everyday.",
                        default=EVERY_DAY)
    return parser.parse_args()


def main():
    """ Main function """
    init_logging()
    args = parse_arguments()
    if not set_schedule(args.time, args.weekdays, args.task):
        log("Arguments are not valid. Exit")
        exit(-1)
    log("Task scheduled")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
