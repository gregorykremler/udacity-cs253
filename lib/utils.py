"""
Aplication utility functions.
"""


import re
import hmac
import random
import string
import hashlib


# Validation utilities for Birthday and ROT13 forms
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']

abbrev_to_month = {m[:3].lower(): m for m in months}

def valid_month(month):
    """Return month if valid Gregorian calendar month."""
    if month:
        short_month = month[:3].lower()
        return abbrev_to_month.get(short_month)


def valid_day(day):
    """Return day if in range 1-31 inclusive."""
    if day and day.isdigit():
        day = int(day)
        if day > 0 and day <= 31:
            return day


def valid_year(year):
    """Return year if in range 1900-2020 inclusive."""
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year < 2020:
            return year


def rot13(text):
    """Encode text with ROT13 cipher."""
    rot13 = ''
    if text:
        s = str(text)
        rot13 = s.encode('rot13')
    return rot13


# Validation utilities for user signup
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    """Return True if username match."""
    return username and USER_RE.match(username)


PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    """Return True if password match."""
    return password and PASS_RE.match(password)


EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    """Return True if either no email or email match."""
    return not email or EMAIL_RE.match(email)


# Cookie hashing utitlities
SECRET = 'imsosecret'
def hash_str(s):
    """Return HMAC bitstring of s."""
    return hmac.new(SECRET, s).hexdigest()


def make_secure_val(val):
    """Return val|hash of val."""
    return "%s|%s" % (val, hash_str(val))


def check_secure_val(secure_val):
    """Return val if val of secure_val matches hash(val)."""
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val


# Datastore hashing utilties
def make_salt(length=5):
    """Return randomly generated salt str."""
    return ''.join(random.choice(string.letters) for x in xrange(length))


def make_pw_hash(name, pw, salt=None):
    """Return hash,salt of name, pw, salt."""
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return "%s,%s" % (h, salt)


def valid_pw_hash(name, pw, h):
    """Return True if h matches hash(name, pw, salt)."""
    salt = h.split(',')[1]
    return h == make_pw_hash(name, pw, salt)

