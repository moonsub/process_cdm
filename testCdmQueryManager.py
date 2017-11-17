# -*- coding: utf-8 -*-
import unittest
from CdmQueryManager import CdmQueryManager

class MysqlManagerTest(unittest.TestCase):
    
    def setUp(self):
        self.manager = CdmQueryManager('config.cfg', 'PostgreSQLConnect', 'synpuf5')

   # def test_selectList(self):
       # result = self.manager.select_person_date_by_diagnosis('hyperparathyroidism')
       # for person_date in result:
       #     admission = self.manager.select_admission(person_date[0], person_date[1])
       #     print(admission)

    def test_select_patient(self):
        result = self.manager.select_person_date_by_diagnosis('hyperparathyroidism')
        print result

    def test_select_test(self):
        result = self.manager.select_test()
        for admission in result:
            print admission
if __name__ == "__main__":
    unittest.main(verbosity=3)