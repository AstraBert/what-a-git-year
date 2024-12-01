from datetime import datetime, timedelta
import pytz

utc=pytz.UTC

def date_is_within_one_year(date):
    """
    Finds dates within one year from the reference date.

    :param date: A datetime object to check.
    :return: True if the date is within one year, False if not.
    """
    reference_date = datetime.today()
    reference_date = reference_date.replace(tzinfo=utc)
    date = date.replace(tzinfo=utc)
    one_year_ago = reference_date - timedelta(days=365)
    one_year_ago = one_year_ago.replace(tzinfo=utc)

    if one_year_ago <= date <= reference_date:
        return True
    return False

