#  Trifacta Inc. Confidential
#
#  Copyright 2020 Trifacta Inc.
#  All Rights Reserved.
#
#  Any use of this material is subject to the Trifacta Inc., Source License located
#  in the file 'SOURCE_LICENSE.txt' which is part of this package.  All rights to
#  this material and any derivative works thereof are reserved by Trifacta Inc.
from trifacta.transform_functions.function_definitions import Replace

import unittest


class TestReplace(unittest.TestCase):
    def test_something(self):
        replace1 = Replace(
            '(?:^((?:1[4-9]|2[0-5])\\d{2})(?: |,|\\/|-)(0?[1-9]|1[0-2])(?: |,|\\/|-)([0-2]?[0-9]|30|31)$)|(?:^.*$)',
            '$1 $2 $3', False, True)

        self.assertEqual(replace1.exec('2048-05-06'), False)


if __name__ == '__main__':
    unittest.main()
