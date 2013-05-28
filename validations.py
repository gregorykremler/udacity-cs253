import re


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


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")


def valid_username(username):
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")


def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


def valid_email(email):
    return not email or EMAIL_RE.match(email)
