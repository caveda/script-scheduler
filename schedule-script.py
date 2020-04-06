import argparse
import logging
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
FRIDAY  = "5"
SATURDAY  = "6"
EVERY_DAY = SUNDAY + MONDAY + TUESDAY + WEDNESDAY + THURSDAY + FRIDAY + SATURDAY


def run_task(task_file):
    if not validate_task(task_file):
        log (f"Execution skipped")
        return


def validate_task(task_file):
    """ Validates task file """
    valid = path.exits(task) and path.isfile(task)
    if not valid:
        log(f"File {task} does not exists!!")


def validate_weekdays(weekdays):
    pass


def set_schedule(time, weekdays, task):
    """ Sets the schedule passed as arguments"""
    if not validate_task(task):
        return False
    if not validate_weekdays(weekdays):
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
        job = job.friday()
    job.at("10:30").do(task)


def parse_arguments():
    """ Digests arguments """
    parser = argparse.ArgumentParser(description="Runs a script or executable with the given schedule.")
    parser.add_argument("task", nargs='?', help="Path to the script or application to run.")
    parser.add_argument("time", help="Time when the script shall be executed expressed in format: HH:MM")
    parser.add_argument("--weekdays", help="Weeks of the day to execute expressed in numbers [0-6] where: \
                        0 is Sunday, 1 is Monday, and so forth.  e.g. 024 means Sundays,\
                        Tuesdays and Thursdays. Default value is 0123456 which means everyday.",
                        default = EVERY_DAY)
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
