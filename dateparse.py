''' 
Input is like:
2m, 2w, 2d, 2h
today, yesterday
2017-10-1
2017/10/1
October
Oct 10

Output is valid datetime format.
'''
from datetime import timedelta, date, datetime
import re


months = 'january|february|march|april|may|june|july|august|september|october|november|december'
months_short = '|'.join([m[0:3] for m in months.split('|')])
months_all = '|'.join([months, months_short])

spans = 'y(ear(s)?)?|m(onth(s)?)?|w(eek(s)?)?|d(ay(s)?)?|h(our(s)?)?'

expressions_dict = {'span': '(?P<span>(?P<n>\d{1,5})\s?(?P<s>' + spans + '))',  # 2y | 1m | 3w | 10d | 10h | 15m | 60s
                    # today | yesterday
                    'word': '(?P<word>today|yesterday)',
                    'iso': '(?P<iso>(\d{4})([-/]\d{1,2}){2}$)',   # 2017-12-31
                    # [Oo]ct[ober] [13, [2013]]
                    'mdy': '(?P<mdy>(?P<mdy_m>' + months_all + ')(\s+(?P<mdy_d>\d{1,2}))?((,?\s+)(?P<mdy_y>\d{4}))?)',
                    # 2013[, october [13]]
                    'ymd': '(?P<ymd>(?P<ymd_y>\d{4})((,?\s+)(?P<ymd_m>' + months_all + '))(\s+(?P<ymd_d>\d{1,2}))?)',
                    # 13 october[[,] 2013]
                    'dmy': '(?P<dmy>(?P<dmy_d>\d{1,2})(\s+(?P<dmy_m>' + months_all + '))((,?\s+)(?P<dmy_y>\d{4}))?)',
                    # 2013[, 13 october]
                    'ydm': '(?P<ydm>(?P<ydm_y>\d{4})((,?\s+)(?P<ydm_d>\d{1,2}))(\s+(?P<ydm_m>' + months_all + ')))'
                    }


def parse_date_exp(exp):
    ''' Parse the input expression.
        Return a tuple of expression key and string value.

        In:     parse_date_exp('2w')
        Out:    ('short', '2w')
    '''
    m = re.fullmatch('|'.join(expressions_dict.values()),
                     exp, re.RegexFlag.IGNORECASE)
    if m:
        groups = m.groupdict()
        return m.lastgroup, dict([(k, v) for (k, v) in groups.items() if v])


def span_to_date(factor, span):
    today = datetime.now()
    dt = None
    s = span[0]
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
    return datetime.strptime(date_string, fmt)
