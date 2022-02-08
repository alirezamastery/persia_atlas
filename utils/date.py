import datetime as dt

from khayyam import JalaliDate


def current_year_j_first_day():
    today = JalaliDate.today()
    return JalaliDate(today.year, 1, 1)


def current_year_first_day():
    today = JalaliDate.today()
    return JalaliDate(today.year, 1, 1).todate()


def current_year_j_last_day():
    today = JalaliDate.today()
    j_next_year_first_day = JalaliDate(today.year + 1, 1, 1)
    return j_next_year_first_day - dt.timedelta(days=1)


def current_year_last_day():
    today = JalaliDate.today()
    j_next_year_first_day = JalaliDate(today.year + 1, 1, 1)
    j_year_last_day = j_next_year_first_day - dt.timedelta(days=1)
    return j_year_last_day.todate()


def month_first_day(j_year, j_month):
    return JalaliDate(j_year, j_month, 1).todate()


def month_last_day(j_year, j_month):
    if j_month == 12:
        next_month_first_day = JalaliDate(j_year + 1, 1, 1)
    else:
        next_month_first_day = JalaliDate(j_year, j_month + 1, 1)
    j_last_day = next_month_first_day - dt.timedelta(days=1)
    return j_last_day.todate()
