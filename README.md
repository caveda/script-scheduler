# script-scheduler
Python CLI tool that runs a script with the supplied schedule

## usage

```
usage: schedule-script.py [-h] [--weekdays WEEKDAYS] [task] time

Runs a script or executable with the given schedule.

positional arguments:
  task                 Path to the script or application to run.
  time                 Time when the script shall be executed expressed in
                       format: HH:MM

optional arguments:
  -h, --help           show this help message and exit
  --weekdays WEEKDAYS  Weeks of the day to execute the task expressed in
                       numbers [0-6] where: 0 is Sunday, 1 is Monday, and so
                       forth. e.g. 024 means Sundays, Tuesdays and Thursdays.
                       Default value is 0123456 which means Everyday.
```
