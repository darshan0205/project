import datetime as dt
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil import rrule
import calendar
from datetime import date



def mkdate(d):
    return_date = ""
    if type(d) is str:
        if d == "today":
            return_date = dt.date.today()
        elif d == "yesterday":
            return_date = dt.date.today() - relativedelta(days=1)
        elif d == "day before yesterday":
            return_date = dt.date.today() - relativedelta(days=2)
        else:
            return_date = parse(d, dayfirst=True).date()
    elif type(d) == dt.datetime:
        return_date = d.date()
    elif type(d) == dt.date:
        return d
    else:
        raise DateFormatError("wrong date format %s" % str(d))
    return return_date

def usable_date(d):
    return mkdate(d)

def get_date_range(frm, to, skip_dates=[]):
    frm = usable_date(frm)
    to = usable_date(to)
    datelist = []
    for date in rrule.rrule(rrule.DAILY, dtstart=frm, until=to, byweekday=[0, 1, 2, 3, 4]):
        datelist.append(date.date())
    return datelist



class CopyNotAvailableError(Exception):
    pass

class DateFormatError(Exception):
    pass




to_date = dt.date.today()
from_date = dt.date.today()+dt.timedelta(-30)


DownloadPath = "C:/Users/91789/Desktop/stocks3"