import datetime

def get_academic_year(month, year):
    if month >=9:
        return str(year)+'-'+str(year+1)
    else:
        return str(year-1)+'-'+str(year)

def get_current_academic_year():
    today = datetime.date.today()
    year = today.year
    month = today.month
    return get_academic_year(month, year)

def get_year_range():
    """Return list of last and current academic years, used to display minutes.
        e.g. 11/2019 -> ['2018-2019', '2019-2020']"""
    today = datetime.date.today()
    year = today.year
    month = today.month
    years_list = [get_academic_year(month, year-1), get_academic_year(month, year)]
    return years_list
