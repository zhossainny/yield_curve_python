# Licensed under the Apache License, Version 2.0
# Copyright 2024 Zahid Hossain <zhossainny@gmail.com>
#
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
from datetime import date
from yield_curve.engine.util.data_field_immutable import DataFieldImmutable
from yield_curve.engine.util.data_field_builder import DataFieldBuilder
from yield_curve.engine.util.data_type import DataType


class TestDataFieldImmutable(unittest.TestCase):
    def test_integer(self):
        # Create DataFieldImmutable objects
        int_field = (
            DataFieldBuilder()
            .with_name("TestInt")
            .with_data_type(DataType.INTEGER)
            .with_value(12)
            .build()
        )
        string_field = (
            DataFieldBuilder()
            .with_name("TestString")
            .with_data_type(DataType.STRING)
            .with_value("TestString")
            .build()
        )

        # Test getInteger
        result = int_field.get_value()
        self.assertEqual(result, 12, "getInteger()")

        # Test findInteger
        result_opt = int_field.find_value()
        self.assertIsNotNone(result_opt, "Expected integer present")
        self.assertEqual(result_opt, 12, "findInteger()")

        # Test exception for invalid type
        # with self.assertRaises(ValueError, msg="Value is null."):
        #     string_field.get_value()

    def test_long(self):
        long_field = (
            DataFieldBuilder()
            .with_name("TestLong")
            .with_data_type(DataType.LONG)
            .with_value(12)
            .build()
        )
        string_field = (
            DataFieldBuilder()
            .with_name("TestString")
            .with_data_type(DataType.STRING)
            .with_value("test")
            .build()
        )

        # Test getLong
        result = long_field.get_value()
        self.assertEqual(result, 12, "getLong()")

        # Test findLong
        result_opt = long_field.find_value()
        self.assertIsNotNone(result_opt, "Expected long present")
        self.assertEqual(result_opt, 12, "findLong()")

        # Test exception for invalid type
        # with self.assertRaises(ValueError, msg="Expected exception"):
        #     string_field.get_value()

    def test_string(self):
        string_field = (
            DataFieldBuilder()
            .with_name("TestString")
            .with_data_type(DataType.STRING)
            .with_value("test")
            .build()
        )

        # Test getString
        result = string_field.get_value()
        self.assertEqual(result, "test", "getString()")

        # Test findString
        result_opt = string_field.find_value()
        self.assertIsNotNone(result_opt, "Expected string present")
        self.assertEqual(result_opt, "test", "findString()")

    def test_double(self):
        double_field = (
            DataFieldBuilder()
            .with_name("TestDouble")
            .with_data_type(DataType.DOUBLE)
            .with_value(12.0)
            .build()
        )
        string_field = (
            DataFieldBuilder()
            .with_name("TestString")
            .with_data_type(DataType.STRING)
            .with_value("test")
            .build()
        )

        # Test getDouble
        result = double_field.get_value()
        self.assertEqual(result, 12.0, "getDouble()")

        # Test findDouble
        result_opt = double_field.find_value()
        self.assertIsNotNone(result_opt, "Expected double present")
        self.assertEqual(result_opt, 12.0, "findDouble()")

        # Test exception for invalid type
        # with self.assertRaises(ValueError, msg="Expected exception"):
        #     string_field.get_value()

    def test_local_date(self):
        test_date = date(2022, 3, 24)
        date_field = (
            DataFieldBuilder()
            .with_name("TestDate")
            .with_data_type(DataType.LOCAL_DATE)
            .with_value(test_date)
            .build()
        )
        string_field = (
            DataFieldBuilder()
            .with_name("TestString")
            .with_data_type(DataType.STRING)
            .with_value("test")
            .build()
        )

        # Test getLocalDate
        result = date_field.get_value()
        self.assertEqual(result, test_date, "getLocalDate()")

        # Test findLocalDate
        result_opt = date_field.find_value()
        self.assertIsNotNone(result_opt, "Expected date present")
        self.assertEqual(result_opt, test_date, "findLocalDate()")

        # Test exception for invalid type
        # with self.assertRaises(ValueError, msg="Expected exception"):
        #     string_field.get_value()


if __name__ == "__main__":
    unittest.main()
