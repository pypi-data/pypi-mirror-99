#  Trifacta Inc. Confidential
#
#  Copyright 2020 Trifacta Inc.
#  All Rights Reserved.
#
#  Any use of this material is subject to the Trifacta Inc., Source License located
#  in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
#  this material and any derivative works thereof are reserved by Trifacta Inc.
from trifacta.util.datetime_formatting_util import DateTimeFormattingUtil
import unittest
from trifacta.transform_functions.function_definitions import ParseDate, DateTimeFormat, ToTime, UnixTime, \
    ConvertTimeZone, UnixTimeFormat, DayOfWeek, DateDiff, DateAdd
import datetime


class DateTimeUtilTestCase(unittest.TestCase):

    def test_translate_format_with_delimiter(self):
        obj = DateTimeFormattingUtil.get_instance()
        self.assertEqual(obj.translate('yyyy-MM-dd HH:mm:ss'), '%Y-%m-%d %H:%M:%S')
        self.assertEqual(obj.translate('MMMM d, yyyy'), '%B %d, %Y')
        self.assertEqual(obj.translate('MM/dd/yy'), '%m/%d/%y')
        self.assertEqual(obj.translate('M/dd/yy'), '%m/%d/%y')
        self.assertEqual(obj.translate('dd/MM/yy'), '%d/%m/%y')
        self.assertEqual(obj.translate('yyyy/MM/dd'), '%Y/%m/%d')
        self.assertEqual(obj.translate('dd.MMM.yyyy'), '%d.%b.%Y')
        self.assertEqual(obj.translate('MMM dd yyyy HH.mm.ss xxx'), '%b %d %Y %H.%M.%S %z')

    def test_translate_format_without_delimiter(self):
        obj = DateTimeFormattingUtil.get_instance()
        self.assertEqual(obj.translate('yyyyMMddHHmmss'), '%Y%m%d%H%M%S')
        self.assertEqual(obj.translate('MMMMdyyyy'), '%B%d%Y')
        self.assertEqual(obj.translate('MMddyy'), '%m%d%y')
        self.assertEqual(obj.translate('Mddyy'), '%m%d%y')
        self.assertEqual(obj.translate('ddMMyy'), '%d%m%y')
        self.assertEqual(obj.translate('yyyyMMdd'), '%Y%m%d')
        self.assertEqual(obj.translate('ddMMMyyyy'), '%d%b%Y')
        self.assertEqual(obj.translate('MMMddyyyyHHmmssxxx'), '%b%d%Y%H%M%S%z')

    def test_non_zero_padding_token(self):
        pass

    def test_translation_string(self):
        obj = DateTimeFormattingUtil.get_instance()
        date_str = '11/12/2015 06:23:12'
        f_str = 'dd/MM/yyyy HH:mm:ss'
        self.assertEqual(obj.strftime(obj.strptime(date_str, f_str), f_str), date_str)
        date_str = '1.12.2015 06:23 am'
        f_str = 'dd.MM.yyyy HH:mm a'
        self.assertEqual(obj.strftime(obj.strptime(date_str, f_str), f_str), date_str)

    def test_datetime_parsing(self):
        pass

    def test_datetime_formatting(self):
        pass

    def test_parse_date(self):
        parsedate1 = ParseDate('MMMM d, yyyy', 'MM/dd/yy', 'M/dd/yy', 'dd/MM/yy', 'yyyy/MM/dd', 'dd.MMM.yyyy',
                               'MMM dd yyyy HH.mm.ss xxx')
        datetimeformat1 = DateTimeFormat("yyyy-MM-ddTHH:mm:ss.SSS")

        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("April 24, 2019")), "2019-04-24T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("May 5, 2019")), "2019-05-05T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("29.Feb.2016")), "2016-02-29T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("1/02/90")), "1990-01-02T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("30/01/90")), "1990-01-30T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("2011/01/15")), "2011-01-15T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("03/04/05")), "2005-03-04T00:00:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("Jan 14 1996 10.30.00 +00:00")), "1996-01-14T10:30:00.000000")
        self.assertEqual(datetimeformat1.exec(
            parsedate1.exec("September 24, 2019")), "2019-09-24T00:00:00.000000")

    def test_unix_time(self):
        unixtime1 = UnixTime()
        totime2 = ToTime('M / d / yyyy')
        self.assertEqual(unixtime1.exec(totime2.exec("09 / 17 / 2015")), 1442448000)
        self.assertEqual(unixtime1.exec(totime2.exec("02 / 04 / 2010")), 1265241600)
        self.assertEqual(unixtime1.exec(totime2.exec("11 / 07 / 2013")), 1383782400)

    def test_convert_time_zone(self):
        convertTimeZone1 = ConvertTimeZone('UTC', 'Asia/Calcutta')
        datetimeformat1 = DateTimeFormat("yyyy-MM-dd HH:mm:ss")
        totime1 = ToTime('dd-MM-yyyy HH:mm:ss.SSS')
        self.assertEqual(datetimeformat1.exec(
            convertTimeZone1.exec(totime1.exec("21-01-2011 12:24:43.456"))), "2011-01-21 17:54:43")

    def test_day_of_week(self):
        dayOfWeek = DayOfWeek()
        totime2 = ToTime('M / d / yyyy')
        self.assertEqual(dayOfWeek.exec(totime2.exec("01 / 21 / 2011")), 5)
        self.assertEqual(dayOfWeek.exec(totime2.exec("09 / 17 / 2015")), 4)
        self.assertEqual(dayOfWeek.exec(totime2.exec("11 / 07 / 2013")), 4)
        self.assertEqual(dayOfWeek.exec(totime2.exec("08 / 23 / 1999")), 1)

    def test_work_day_in_tl(self):
        pass

    def test_net_work_day_in_tl(self):
        pass

    def test_date_add(self):
        totime2 = ToTime('M / d / yyyy')
        dateAddYear = DateAdd('year')
        dateAddMonth = DateAdd('month')
        dateAddWeek = DateAdd('week')
        dateAddDay = DateAdd('day')
        dateAddHour = DateAdd('hour')
        dateAddMinute = DateAdd('minute')
        dateAddSecond = DateAdd('second')
        dateAddMilli = DateAdd('millisecond')
        self.assertEqual(dateAddYear.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2012, 1, 21, 0, 0))
        self.assertEqual(dateAddMonth.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 2, 21, 0, 0))
        self.assertEqual(dateAddWeek.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 28, 0, 0))
        self.assertEqual(dateAddDay.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 22, 0, 0))
        self.assertEqual(dateAddHour.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 21, 1, 0))
        self.assertEqual(dateAddMinute.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 21, 0, 1))
        self.assertEqual(dateAddSecond.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 21, 0, 0, 1))
        self.assertEqual(dateAddMilli.exec(totime2.exec("01 / 21 / 2011"), 1), datetime.datetime(2011, 1, 21, 0, 0))

    def test_date_diff(self):
        dateDiffYear = DateDiff('year')
        dateDiffMonth = DateDiff('month')
        dateDiffWeek = DateDiff('week')
        dateDiffDay = DateDiff('day')
        dateDiffHour = DateDiff('hour')
        dateDiffMinute = DateDiff('minute')
        dateDiffSecond = DateDiff('second')
        dateDiffMilli = DateDiff('millisecond')
        self.assertEqual(
            dateDiffYear.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2012, 1, 21, 0, 0)), 1)
        self.assertEqual(
            dateDiffMonth.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2011, 2, 21, 0, 0)), 1)
        self.assertEqual(
            dateDiffWeek.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2011, 1, 28, 0, 0)), 1)
        self.assertEqual(
            dateDiffDay.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2011, 1, 22, 0, 0)), 1)
        self.assertEqual(
            dateDiffHour.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2011, 1, 21, 1, 0)), 1)
        self.assertEqual(
            dateDiffMinute.exec(datetime.datetime(2011, 1, 21, 0, 0), datetime.datetime(2011, 1, 21, 0, 1)), 1)
        self.assertEqual(
            dateDiffSecond.exec(datetime.datetime(2021, 3, 17, 11, 21, 33, 579216),
                                datetime.datetime(2021, 3, 17, 11, 21, 43, 46349)), 9)
        self.assertEqual(
            dateDiffMilli.exec(datetime.datetime(2021, 3, 17, 11, 21, 33, 579216),
                               datetime.datetime(2021, 3, 17, 11, 21, 43, 46349)), 467)

    if __name__ == '__main__':
        unittest.main()
