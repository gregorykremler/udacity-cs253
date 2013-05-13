import cgi


def escape_html(s):
    return cgi.escape(s, quote=True)


months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

abbrev_to_month = dict((m[:3].lower(), m) for m in months)


def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return abbrev_to_month.get(short_month)


def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day


def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year < 2020:
            return year


def rot13(text):
    rot13 = ''
    if text:
        s = str(text)
        rot13 = s.encode('rot13')
    return rot13
