import datetime
import random as rnd
import re
from collections import namedtuple
import requests

DollarDate = namedtuple("Dollar_date", ["dollar_rate", "last_update"])
# solve the url part
DOLLAR_RATE_URL = 'thats for you to solve'


def get_dollar_rate():
    # Extracting currency rate and last update date.
    r = requests.get(DOLLAR_RATE_URL)
    start_pos = r.text.index(">")
    end_pos = r.text.index("^")
    match = re.search("\d{2}/\d{2}/\d{4}", r.text)
    return DollarDate(float(r.text[start_pos + 1: end_pos]),
                      datetime.datetime.strptime(match.group(), '%d/%m/%Y').date())


def get_money_interval(diff_level, nis_amount):
    lower_bound = max(nis_amount - (5 - diff_level), 0)
    upper_bound = nis_amount + (5 - diff_level)
    return lower_bound, upper_bound


# validate that number is digit


def get_guess_from_user(usd_amount):  # todo error handling
    user_guess = float(input(f' take a wild guess, how much shekels does {usd_amount} worth ? '))
    return user_guess


def guess_in_range(user_guess, lower_bound, upper_bound):
    if not (lower_bound <= user_guess <= upper_bound):
        return False
    return True


def play(diff_level):
    dollar_date = get_dollar_rate()
    usd_amount = rnd.randint(1, 100)
    nis_amount = usd_amount * dollar_date.dollar_rate
    lower_bound, upper_bound = get_money_interval(int(diff_level), nis_amount)
    user_guess = get_guess_from_user(usd_amount)
    msg = guess_in_range(user_guess, lower_bound, upper_bound)
    if msg:
        return f'Congrats , you are correct! the real value is {nis_amount} and you said {user_guess}'
    return f'Not a great guess, the real value is {nis_amount} update to {dollar_date.last_update}'
