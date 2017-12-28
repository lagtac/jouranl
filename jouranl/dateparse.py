''' 
Input is like:
2m, 2w, 2d, 2h
2 weeks
120 years
today, yesterday
2017-10-1
2017/10/1
2017-10/1
October
Oct 10
2013
2013, jan 12
13 jan, 2013

Output is a valid datetime object.
'''
from datetime import timedelta, date, datetime
import re


months = 'january|february|march|april|may|june|july|august|september|october|november|december'
months_short = '|'.join([m[0:3] for m in months.split('|')])
months_all = '|'.join([months, months_short])
months_array = months_all.split('|')

spans = 'y(ear(s)?)?|m(onth(s)?)?|w(eek(s)?)?|d(ay(s)?)?|h(our(s)?)?'

expressions_dict = {'span': '^(?P<span>(?P<span_factor>\d{1,5})\s?(?P<span_duration>' + spans + '))$',  # 2y | 1m | 3w | 10d | 10h | 15m | 60s
                    # today | yesterday
                    'word': '^(?P<word>today|yesterday)$',
                    # 2017-12-31
                    'iso': '^(?P<iso>(?P<iso_y>\d{4})[-/](?P<iso_m>\d{1,2})[-/](?P<iso_d>\d{1,2}))$',
                    'year': '^(?P<year>\d{4})$',   # 2017
                    'month': '^(?P<month>' + months_all + ')$',   # 2017
                    # October 13[[,] 2013]
                    'mdy': '^(?P<mdy>(?P<mdy_m>' + months_all + ')\s+(?P<mdy_d>\d{1,2})((,?\s*)(?P<mdy_y>\d{4}))?)$',
                    # October 2013 [13]
                    'myd': '^(?P<myd>(?P<myd_m>' + months_all + ')\s+(?P<myd_y>\d{4})(\s+(?P<myd_d>\d{1,2}))?)$',
                    # 13 october[[,] 2013]
                    'dmy': '^(?P<dmy>(?P<dmy_d>\d{1,2})(\s+(?P<dmy_m>' + months_all + '))((,?\s*)(?P<dmy_y>\d{4}))?)$',
                    # 2013[,] october [13]
                    'ymd': '^(?P<ymd>(?P<ymd_y>\d{4})((,?\s+)(?P<ymd_m>' + months_all + '))(\s+(?P<ymd_d>\d{1,2}))?)$',
                    # 2013, 13 october
                    'ydm': '^(?P<ydm>(?P<ydm_y>\d{4})((,?\s+)(?P<ydm_d>\d{1,2}))(\s+(?P<ydm_m>' + months_all + ')))$'
                    }


def get_month_ordinal(name):
    return months_array.index(name) % 12 + 1


def parse(exp):
    # print(exp)
    name, matches = parse_date_exp(exp)
    return resolve_date_exp(name, matches)


def parse_date_exp(exp):
    ''' Parse the input expression.
        Return a dictionary of the named groups in the matched expression.

        >>> parse_date_exp('jan 12, 2017')
        ('mdy', {'mdy': 'jan 12, 2017', 'mdy_m': 'jan', 'mdy_d': '12', 'mdy_y': '2017')
    '''
    matched = re.fullmatch('|'.join(expressions_dict.values()),
                           exp, re.RegexFlag.IGNORECASE)
    if matched:
        groups = matched.groupdict()
        name, parts = matched.lastgroup, dict(
            [(k, v) for (k, v) in groups.items() if k.startswith(matched.lastgroup)])
        return name, parts


def resolve_date_exp(name, matches):
    ''' Accept the result of parse_date_exp and calculate the required date.         
        Return a datetime object.

        >>> resolve_date_exp('iso', {'iso': '2017-12-29', 'iso_y': '2017', 'iso_m': '12', 'iso_d': '29'})
        datetime.datetime(2017, 12, 29, 0, 0)

        >>> resolve_date_exp('mdy', {'mdy': 'oct 12, 2009', 'mdy_y': '2009', 'mdy_m': 'oct', 'mdy_d': '12'})
        datetime.datetime(2009, 10, 12, 0, 0)
    '''

    result = None
    today = datetime.today()

    if name == 'span':
        result = span_to_date(
            int(matches['span_factor']), matches['span_duration'])

    if name == 'month':
        result = datetime(today.year, get_month_ordinal(matches['month']), 1)

    if name == 'year':
        result = datetime(int(matches['year']), 1, 1)

    if name == 'word':
        # today/yesterday in this context means the *start* of this or the other day
        if matches['word'] == 'today':
            result = today.replace(hour=0, minute=0, second=0, microsecond=0)
        elif matches['word'] == 'yesterday':
            result = (today - timedelta(days=1)
                      ).replace(hour=0, minute=0, second=0, microsecond=0)

    if name == 'iso':
        result = strptime(
            f"{matches['iso_y']} {matches['iso_m']} {matches['iso_d']}", '%Y %m %d')

    if name in ['mdy', 'myd', 'dmy', 'ymd', 'ydm']:
        # Year is optional in mdy and dmy
        y = matches[f'{name}_y'] or today.year
        m = matches[f'{name}_m']
        d = matches[f'{name}_d'] or '1'  # Day is optional in ymd and myd
        result = strptime(f"{y} {m} {d}", '%Y %b %d')

    return result


def span_to_date(factor, duration):
    today = datetime.now()
    dt = None
    s = duration[0]
    if s == 'y':
        dt = today.replace(year=today.year - factor)
    elif s == 'm':
        dt = today.replace(month=today.month - factor)
    elif s == 'w':
        dt = today - timedelta(weeks=factor)
    elif s == 'd':
        dt = today - timedelta(days=factor)
    elif s == 'h':
        dt = today - timedelta(hours=factor)
    return dt


def strftime(thedate, fmt=None):
    ''' see https://en.wikipedia.org/wiki/ISO_8601 '''
    fmt = fmt or '%Y%m%dT%H%M%S'
    return thedate.strftime(fmt)


def strptime(date_string, fmt=None):
    fmt = fmt or '%Y%m%dT%H%M%S'
    try:
        return datetime.strptime(date_string, fmt)
    except ValueError as err:
        return None


if __name__ == '__main__':
    while(True):
        out = input("Date expression -> ")
        print(parse(out))
