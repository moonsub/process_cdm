# -*- coding: utf-8 -*-
import unittest
import os
import ConfigParser
from Admission import Admission
from PostgreSQLManager import PostgreSQLQueryManager
from CdmToTrainDataConverter import CdmToTrainDataConverter
class MysqlManagerTest(unittest.TestCase):
    
    def setUp(self):
        path  = os.getcwd() + "/config.cfg"


        self.postgres = PostgreSQLQueryManager(path, 'PostgreSQLConnect')

    def test_selectList(self):
        schema = 'synpuf5'


        result = self.postgres.selectList(
            """
            select person_id, max(condition_start_date)
            from %s.condition_occurrence a
            inner join %s.concept b
            on a.condition_concept_id = b.concept_id
            where b.concept_name like '%%hyperparathyroidism%%'
            group by a.person_id
            """ % (schema, schema)
            )

        admissions = []
        for person in result:
            result = self.postgres.selectList(
                """
                select *
                from %s.condition_occurrence a
                inner join %s.concept b
                on a.condition_concept_id = b.concept_id
                where person_id = %d and condition_start_date <= '%s'
                order by person_id, condition_start_date
                """ % (schema, schema, person[0], person[1])
            )
            for patient in result:
                admissions.append(Admission(int(patient[1]), int(patient[2]), patient[12], patient[4]))
        
        converter = CdmToTrainDataConverter(admissions)
        model_data, diagnosis_indice = converter.convert_to_model_data()
        print(model_data)
        print(diagnosis_indice)

if __name__ == "__main__":
    unittest.main(verbosity=2)