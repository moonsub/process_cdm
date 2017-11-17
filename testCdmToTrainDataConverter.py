# -*- coding: utf-8 -*-
from CdmToTrainDataConverter import CdmToTrainDataConverter
import datetime
import unittest

class CdmToTrainDataConverterTest(unittest.TestCase):
    
    def setUp(self):
        self.converter = CdmToTrainDataConverter(None)

    def test_get_admit_date(self):
        diagnosis_map = {}
        diagnosis_map[datetime.date(2008, 10, 19)] = ""
        diagnosis_map[datetime.date(2009, 1, 1)] = ""
        
        first_date = datetime.date(2008, 11, 11)
        first_result = self.converter.get_admit_date(diagnosis_map, first_date)
        self.assertEqual(first_result, datetime.date(2008, 10, 19))

        second_date = datetime.date(2008, 12, 5)
        second_result = self.converter.get_admit_date(diagnosis_map, second_date)
        self.assertEqual(second_result, None)
        
        third_date = datetime.date(2009, 1, 1)
        third_result = self.converter.get_admit_date(diagnosis_map, third_date)
        self.assertEqual(third_result, datetime.date(2009, 1, 1))

        fourth_date = datetime.date(2009, 1, 19)
        fourth_result = self.converter.get_admit_date(diagnosis_map, fourth_date)
        self.assertEqual(fourth_result, datetime.date(2009, 1, 1))
        
        fifth_date = datetime.date(2009, 3, 3)
        fifth_result = self.converter.get_admit_date(diagnosis_map, fifth_date)
        self.assertEqual(fifth_result, None)

if __name__ == "__main__":
    unittest.main(verbosity=2)