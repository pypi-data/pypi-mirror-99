#  Trifacta Inc. Confidential
#
#  Copyright 2020 Trifacta Inc.
#  All Rights Reserved.
#
#  Any use of this material is subject to the Trifacta Inc., Source License located
#  in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
#  this material and any derivative works thereof are reserved by Trifacta Inc.

from trifacta.constants import DATETIME_FORMAT_TOKEN_DICTIONARY, DATETIME_PARSE_TOKEN_DICTIONARY
from datetime import datetime


class DateTimeFormattingUtil(object):
    """
    Utility class for translation datetime formatting string.
    This utility acts in place of ICU library,
    processing ICU format string
    ex- 'yyyy-MM-dd HH:mm:ss' ---> '%Y-%m-%d %H:%M:%S'
    """
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if DateTimeFormattingUtil.__instance is None:
            DateTimeFormattingUtil()
        return DateTimeFormattingUtil.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DateTimeFormattingUtil.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DateTimeFormattingUtil.__instance = self
            self.translation_cache = dict()

    def translate(self, icu_fstring, mode='parse'):
        """
        @param icu_fstring: basestring containing datetime format following ICU based specification
        This is not a exhaustive mapping of ICU tokens, this also does not translate any string
        ICU lib can, as trifacta UI inhibits user to enter a specific set of token and delimiters
        thus format string CDF can be translated easily
        """
        if mode == 'parse':
            DATETIME_TOKEN_DICTIONARY = DATETIME_PARSE_TOKEN_DICTIONARY
        else:
            DATETIME_TOKEN_DICTIONARY = DATETIME_FORMAT_TOKEN_DICTIONARY
        if self.translation_cache.get(icu_fstring) is not None:
            return self.translation_cache.get(icu_fstring)
        str_fstring = icu_fstring
        for key in DATETIME_TOKEN_DICTIONARY:
            str_fstring = str_fstring.replace(key, DATETIME_TOKEN_DICTIONARY[key])
        # self.inspect_translation(str_fstring)
        self.translation_cache[icu_fstring] = str_fstring
        return str_fstring

    def strptime(self, str, f_str):
        """
        @param str: basestring to parse to datetime,based on given ICU format string
        @return datetime object
        """
        try:
            # return timezone('UTC').localize(datetime.strptime(str, self.translate(f_str)))
            return datetime.strptime(str, self.translate(f_str))
        except (ValueError, TypeError):
            raise Exception

    def strftime(self, dt_obj, f_str):
        """
        @param dt_obj: datetime object
        @param f_str: basestring ICU format string
        """
        try:
            return dt_obj.strftime(self.translate(f_str))
        except (ValueError, TypeError):
            raise Exception

    # def inspect_translation(self, post_translation):
    #     non_token = re.sub(r'%[A-Za-z]', '', post_translation)
    #     alphabet_count =
    #     pass
    #     # removing ISO format tokens


'''
| ICU token | ICU string output    | strftime token | strftime string output        |
| --------- | -------------------- | -------------- | ----------------------------- |
|           |                      | %%             | %                             |
| MMMM      | January              | %B             | January                       |
| MMM       | Jan                  | %b             | Jan                           |
| MM        | 01                   | %m             | 01                            |
| M         | 1                    | %-m            |                               |

| dd        | 09                   | %d             | 09                            |
| D         | 352                  | %j             | 352                           |
| d         | 9                    | %-d            | 9                             |

| EEEE      | Wednesday (Week)     | %A             | Wednesday (Week)              |
| EEE       | Wed (Week)           | %a             | Wed (Week)                    |

| YYYY      | 2016 (year)          | %Y/%G          | 2016 (year)                   |
| YY        | 16 (year)            | %y             | 16 (year)                     |

| SSS       | 003920 (millisecond) | %f             | 003920 (millisecond)          |
| SS        | 003920 (millisecond) | %f             | 003920 (millisecond)          |
| S         | 003920 (millisecond) | %f             | 003920 (millisecond)          |

| ss        | 03 (second)          | %S             | 03 (second)                   |
| s         | 3 (second)           | %-S            | 3 (second)                    |

| mm        | 09 (minutes)         | %M             | 09                            |
| m         | 9 (minutes)          | %-M            | 9                             |

| HH        | 0-23 (hours)         | %H             | 0-23 (hours)                  |
| H         | 0-11 (hours)         | %I             | 0-11 (hours)                  |

| a         | am/pm                | %p             | AM/PM                         |

| XXX       | ISO 8601 (+ 5.30)    | %z             | +0530                         |
| XX        | ISO 8601 (+ 5.30)    | %z             | +0530                         |
| X         | ISO 8601 (+ 5.30)    | %z             | +0530                         |

| ww        | 09 (week #)          | %W             | 09 (week # with Monday first)  |
| w         | 09 (week #)          |                |                               |
|           |                      | %V             | 09 (week # with Sunday first)  |


|           |                      | %s             | 1614858605 (unix timestamp)   |
|           |                      | %Z             | IST                           |

|           |                      | %x             | 03/04/21 (local date)         |
|           |                      | %X             | 17:20:05 (local time)         |
|           |                      | %v             | 4-Mar-2021                    |
|           |                      | %u/%w          | 0-6 (weekday)                 |
|           |                      | %V             | 09 (01-52 week no)            |
|           |                      | %c             | Thu Mar  4 17:20:05 2021      |
| --------- | -------------------- | -------------- | ----------------------------- |
'''
