#  Trifacta Inc. Confidential
#
#  Copyright 2020 Trifacta Inc.
#  All Rights Reserved.
#
#  Any use of this material is subject to the Trifacta Inc., Source License located
#  in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
#  this material and any derivative works thereof are reserved by Trifacta Inc.

# this dictionary provides the mapping for ICU datetime format
# string tokens to strftime format string tokens
DATETIME_PARSE_TOKEN_DICTIONARY = {
    # '%': '%%',        # dealing with retaining '%' in ICU format string
    'MMMM': '%B',  # ex - January
    'MMM': '%b',  # ex - Jan
    'MM': '%!',  # ex - 01 (month number 1-12)   (proxy for %m)
    'mm': '%@',  # ex - 09 (minutes)             (proxy for %M)
    'm': '%@',  # ex - 9 (minutes) temp         (proxy for %M)  temp
    'M': '%m',  # ex - January     temp
    'dd': '%&',  # ex - 09 (day # of month)      (proxy for %d)
    'D': '%j',  # ex - 352 (day # in year)
    'd': '%d',  # ex - 9 (day # of month)
    'EEEE': '%A',  # ex - Wednesday
    'EEE': '%^',  # ex - Wed                      (proxy for %a)
    'yyyy': '%Y',  # ex - 2016
    'yy': '%y',  # ex - 16
    'SSS': '%f',  # ex - 003920 (millisecond)
    'SS': '%f',  # ex - 003920 (millisecond)
    'S': '%f',  # ex - 003920 (millisecond)
    'ss': '%S',  # ex - 03 (seconds)
    's': '%S',  # ex - 3 (seconds)                              temp
    'HH': '%_',  # ex - 0-23 (hour of day)       (proxy for %H)
    'H': '%I',  # ex - 0-11 (hour of day)
    'a': '%p',  # ex - AM/PM
    'XXX': '%z',  # ex - ISO 8601 +0530
    'xxx': '%z',  # ex - ISO 8601 +0530
    'XX': '%z',  # ex - ISO 8601 +0530
    'xx': '%z',  # ex - ISO 8601 +0530
    'X': '%z',  # ex - ISO 8601 +0530
    'x': '%z',  # ex - ISO 8601 +0530
    'ww': '%W',
    'w': '%W',
    '_': 'H',  #
    '^': 'a',  #
    '!': 'm',  #
    '@': 'M',  #
    '&': 'd',  #
}
DATETIME_FORMAT_TOKEN_DICTIONARY = {
    # '%': '%%',        # dealing with retaining '%' in ICU format string
    'MMMM': '%B',  # ex - January
    'MMM': '%b',  # ex - Jan
    'MM': '%!',  # ex - 01 (month number 1-12)   (proxy for %m)
    'mm': '%@',  # ex - 09 (minutes)             (proxy for %M)
    'm': '%-@',  # ex - 9 (minutes) temp         (proxy for %M)  temp
    'M': '%m',  # ex - January     temp
    'dd': '%&',  # ex - 09 (day # of month)      (proxy for %d)
    'D': '%j',  # ex - 352 (day # in year)
    'd': '%-d',  # ex - 9 (day # of month)
    'EEEE': '%A',  # ex - Wednesday
    'EEE': '%^',  # ex - Wed                      (proxy for %a)
    'yyyy': '%Y',  # ex - 2016
    'yy': '%y',  # ex - 16
    'SSS': '%f',  # ex - 003920 (millisecond)
    'SS': '%f',  # ex - 003920 (millisecond)
    'S': '%f',  # ex - 003920 (millisecond)
    'ss': '%S',  # ex - 03 (seconds)
    's': '%-S',  # ex - 3 (seconds)                              temp
    'HH': '%_',  # ex - 0-23 (hour of day)       (proxy for %H)
    'H': '%I',  # ex - 0-11 (hour of day)
    'a': '%p',  # ex - AM/PM
    'XXX': '%z',  # ex - ISO 8601 +0530
    'xxx': '%z',  # ex - ISO 8601 +0530
    'XX': '%z',  # ex - ISO 8601 +0530
    'xx': '%z',  # ex - ISO 8601 +0530
    'X': '%z',  # ex - ISO 8601 +0530
    'x': '%z',  # ex - ISO 8601 +0530
    'ww': '%W',
    'w': '%W',
    '_': 'H',  #
    '^': 'a',  #
    '!': 'm',  #
    '@': 'M',  #
    '&': 'd',  #
}
