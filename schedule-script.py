import argparse
import os
import re
import time
from os import path

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


def run_task(task_file):
    if not validate_task(task_file):
        log(f"Execution skipped")
        return
    os.system(task_file)


def validate_task(task_file):
    """ Validates task file """
    valid = path.exits(task_file) and path.isfile(task_file)
    if not valid:
        log(f"File {task_file} does not exists!!")


def validate_weekdays(weekdays):
    """ Validates weekdays format """
    result = re.match("^0?1?2?3?4?5?6?$", weekdays) is not None
    if not result:
        log(f"Invalid weekdays format: {weekdays}!!")
    return result

def validate_time(time):
    """ Validates time format """
    try:
        time.strptime(input, '%H:%M')
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

    job = schedule.every()
    if SUNDAY in weekdays:
        job = job.sunday()
    if MONDAY in weekdays:
        job = job.monday()
    if TUESDAY in weekdays:
        job = job.tuesday()
    if WEDNESDAY in weekdays:
        job = job.wednesday()
    if THURSDAY in weekdays:
        job = job.thursday()
    if FRIDAY in weekdays:
        job = job.friday()
    if SATURDAY in weekdays:
        job = job.saturday()
    job.at(time).do(task)


def parse_arguments():
    """ Digests arguments """
    parser = argparse.ArgumentParser(description="Runs a script or executable with the given schedule.")
    parser.add_argument("task", nargs='?', help="Path to the script or application to run.")
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
        exit(-1)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
