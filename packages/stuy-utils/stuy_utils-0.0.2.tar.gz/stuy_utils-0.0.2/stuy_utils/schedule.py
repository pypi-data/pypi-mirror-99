"""Functions for retriving schedule and day info of a day in the semester."""

import csv
from collections import namedtuple
from datetime import date
from datetime import datetime as dt
from datetime import time
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from stuy_utils import errors

Info = namedtuple("Info", ("cycle", "period", "testing", "event"))
Time = namedtuple("Time", ("start", "end"))

TERM_PATH = f"{Path(__file__).parent}\\data\\term_days.csv"
BELL_PATH = f"{Path(__file__).parent}\\data\\bell_schedule.csv"


with open(TERM_PATH, "r") as term_csv, open(BELL_PATH, "r") as bell_csv:
    # {"2021-01-31": Info("", "", "", "Fall Grades Due"), ...}
    TERM_DAYS = {row[0]: Info(*row[1:])
                 for row in list(csv.reader(term_csv))[1:]}

    # {"Period 1": Time(datetime.time(9, 10), datetime.time(10, 5)), ...}
    BELL_SCHEDULE = {row[0]: Time(*[time.fromisoformat(element)
                                    for element in row[1:]])
                     for row in list(csv.reader(bell_csv))[1:]}


def convert_to_isoformat(day: Union[date, dt]) -> str:
    """Convert a date object to an ISO-formatted date string.

    Convert a date or datetime object from the datetime library to a string
    formatted using the ISO 8601 format, while also checking if 'date' is a
    valid date and if it exists in the data.

    Args:
        day (Union[datetime.date, datetime.datetime]): A date or datetime
        object from the datetime library.

    Raises:
        errors.InvalidDate: Thrown if the input is not a date or a datetime
        object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        str: A date using the ISO 8601 format (yyyy-mm-dd).
    """
    if not isinstance(day, date):
        raise errors.InvalidDate(day)

    if isinstance(day, dt):
        day = day.date()  # Converts datetime to date to remove time

    iso_date = day.isoformat()

    if iso_date not in TERM_DAYS:
        raise errors.DayNotInData(iso_date)

    return iso_date


def get_day_info(day: Union[date, dt]) -> Info:
    """Returns information about a given day.

    Returns the cycle, period, testing subjects, and any events of a given
    day. If a category does not apply, an empty string will be returned.

    Args:
        day (Union[datetime.date, datetime.datetime]): A date or datetime
        object from the datetime library.

    Raises:
        errors.InvalidDate: Thrown if the input is not a date or a datetime
        object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        Info: A namedtule with fields 'cycle', 'period', 'testing', and
        'event'.
    """
    return TERM_DAYS[convert_to_isoformat(day)]


def get_next_school_day(
        day: Union[date, dt], always_same: bool = False) -> Optional[date]:
    """Returns when the next school day is.

    Returns a date object of the next school day from the given day. The given
    datetime will be returned as a date if school is still in session.

    Args:
        day (Union[datetime.date, datetime.datetime]): A date or datetime
        object from the datetime library.
        always_same (bool, optional): Whether or not to always return the given
        day if the given day is a school day. Defaults to False.

    Raises:
        errors.InvalidDate: Thrown if the input is not a datetime object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        Optional[datetime.date]: A date object with the year, month, and day
        of the next school day.
    """
    schedule_list = list(TERM_DAYS.items())
    day_index = list(TERM_DAYS).index(convert_to_isoformat(day))

    dt_ = day

    if not isinstance(dt_, dt):
        # Converts date to datetime with time 12:00 AM
        dt_ = dt.combine(dt_, time.min)

    # Loops through each day during or after the given day
    for day_ in schedule_list[day_index:]:
        # Return the same day if always_same is True, or if the given day is
        # before school is over (before AIS Tutoring ends)
        if always_same or (day_[1].cycle and dt_ <= dt.combine(
                date.fromisoformat(day_[0]),
                BELL_SCHEDULE["AIS Tutoring"].end)):
            return date.fromisoformat(day_[0])

    return None


def get_bell_schedule(day: Union[date, dt]) -> Dict[str, Time]:
    """Returns the bell periods of the next school day.

    Returns a dictionary of bell periods of the next school day. If the given
    day is a school day, then the bell schedule of that day will be returned,
    even if it is afterschool.

    Args:
        day (Union[datetime.date, datetime.datetime]): A date or datetime
        object from the datetime library.

    Raises:
        errors.InvalidDate: Thrown if the input is not a datetime object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        Dict[str, Time]: A dictionary of keys of strings of the category name
        (see data/bell_schedule.csv) and values of Time namedtuple objects with
        fields 'start' and 'end', which returns a datetime object.
    """
    return {cat[0]:  # key with category name (e.g. "Period 1")
            # Creates a Time namedtuple with the datetimes of the next school
            # day combined with the start and end times of the current category
            Time(*[dt.combine(get_next_school_day(day), time)
                   for time in cat[1]])  # Loop through the start and end times
            for cat in BELL_SCHEDULE.items()}  # Loop through the categories


def get_current_class(day: dt) -> Optional[Tuple[str, Time]]:
    """Returns information of the current class.

    Returns a tuple of information of the current class, where the first
    element is a string of the category, such as the class period, and a Time
    namedtuple object, which includes when said period starts and ends.

    Args:
        day (datetime.datetime): A datetime object from the datetime library.

    Raises:
        errors.InvalidDate: Thrown if the input is not a datetime object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        Optional[Tuple[str, Time]]: A tuple of a string of the category name
        (see data/bell_schedule.csv), and a Time namedtuple object with fields
        'start' and 'end', which returns a datetime object.
    """
    schedule = get_bell_schedule(day)

    # If school is in session, iterate and check through all of the categories
    if schedule["Period 1"].start <= day <= schedule["AIS Tutoring"].end:
        for cat in schedule.items():
            if cat[1].start <= day <= cat[1].end:
                return cat

    return None


def get_next_class(day: dt) -> Optional[Tuple[str, Time]]:
    """Returns information of the next class.

    Returns a tuple of information of the next class, where the first element
    is a string of the category, such as the class period, and a Time
    namedtuple object, which includes when said period starts and ends.

    Args:
        day (datetime.datetime): A datetime object from the datetime library.

    Raises:
        errors.InvalidDate: Thrown if the input is not a datetime object.
        errors.DayNotInData: Thrown if the inputted day is not in
        term_days.csv.

    Returns:
        Optional[Tuple[str, Time]]: A tuple of a string of the category name
        (see data/bell_schedule.csv), and a Time namedtuple object with fields
        'start' and 'end', which returns a datetime object.
    """
    current_class = get_current_class(day)

    # Checks if school is in session and there is a class after the current
    # class (anything before AIS Tutoring)
    if current_class and current_class[0] != "AIS Tutoring":
        schedule_list = list(get_bell_schedule(day).items())

        # Gets the next class in the schedule list, but skip passing periods
        next_class = schedule_list[schedule_list.index(current_class) + 1]
        return next_class if not next_class[0].startswith("Passing") \
            else schedule_list[schedule_list.index(next_class) + 1]

    # Gets the first period datetime for the next school day
    if get_next_school_day(day):
        return list(get_bell_schedule(get_next_school_day(day)).items())[0]

    return None
