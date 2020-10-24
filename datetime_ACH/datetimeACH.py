import datetime as dt

class Date_Time():
    """
    This class is used to structure the date and time formatting required for ACH files
    """

    def __init__(self):
        pass

    def create_date(self):
        # YYMMDD
        return dt.date.today().strftime('%y%m%d')

    def fh_create_time(self):
        # HHMM
        return dt.datetime.now().strftime('%H%M')

    def effective_date(self):
        pass
