#-*- coding: utf-8 -*-
from Admission import Admission
import collections
import datetime
from dateutil.relativedelta import relativedelta
class CdmToTrainDataConverter():

    def __init__(self):
        self.index_data = {}
        self.diagnosis_indice = []

    def get_admit_date(self, diagnosis_map, date):
        ret = None
        for start_date in diagnosis_map.keys():
            end_date = start_date + relativedelta(months=1)
            if start_date <= date <= end_date:
                ret = start_date
                return ret
        
    def set_index_data(self, admissions):
        print 'make index data start'
        for admission in admissions:
            diagnosis_id = admission.get_diagnosis_id()
            diagnosis_index = []
            if diagnosis_id not in self.index_data:
                self.index_data[diagnosis_id] = len(self.index_data)
                diagnosis_index.append(diagnosis_id)
                diagnosis_index.append(self.index_data[diagnosis_id])
                diagnosis_index.append(admission.get_diagnosis_name())    
                self.diagnosis_indice.append(diagnosis_index)
        print 'make index data end'

    def get_visit_diagnosis_map(self, admissions):
        print 'Building Person-Visit-diagnosis mapping start'
        person_map = collections.OrderedDict()
        for admission in admissions:
            
            person_id = admission.get_person_id()
            
            if person_id not in person_map:
                person_map[person_id] = collections.OrderedDict()
            
            admit_date = admission.get_admit_date()
            '''
            start_date = self.get_admit_date(person_map[person_id], admit_date)

            if start_date is None:
                person_map[person_id][admit_date] = []
                start_date = admit_date
            '''
            if admit_date not in person_map[person_id]:
                person_map[person_id][admit_date] = []

        
            diagnosis = []
            diagnosis_id = admission.get_diagnosis_id()
            if diagnosis_id in self.index_data:
                person_map[person_id][admit_date].append(self.index_data[diagnosis_id])    #start_date -> admit_date로 변경
        print 'Building Person-Visit-diagnosis mapping end'
        return person_map
    '''
    def convert_to_model_data(self):
    	print 'convertToModelData Start'
        diagnosis_indice = []
        all_patient_diagnosis = []
        diagnosis_numbers = {}
        person_map = self.get_visit_diagnosis_map()

        for value in person_map.values():
            if len(value) > 1:
                one_patient_diagnosis = []

                for diagnosis in value.values():
                    codes = []
                    
                    for code in diagnosis:
                        diagnosis_index = []
                        diagnosis_id = code[0]
                        diagnosis_name = code[1]
                        if diagnosis_id not in diagnosis_numbers:
                            diagnosis_numbers[diagnosis_id] = len(diagnosis_numbers)
                            diagnosis_index.append(diagnosis_numbers[diagnosis_id])
                            diagnosis_index.append(diagnosis_id)
                            diagnosis_index.append(diagnosis_name)
                            diagnosis_indice.append(diagnosis_index)
        
                        
                    
                        codes.append(diagnosis_numbers[diagnosis_id])
                    
                    one_patient_diagnosis.append(codes)
                
                all_patient_diagnosis.append(one_patient_diagnosis)
        
        return all_patient_diagnosis, diagnosis_indice
    '''

    def get_model_data(self, admissions):
        
        person_date_diagnosis = self.get_visit_diagnosis_map(admissions)
        all_patient_diagnosis = []
        for date_diagnosis in person_date_diagnosis.values():
            if len(date_diagnosis) > 1:
                one_patient_diagnosis = []
                for diagnosis in date_diagnosis.values():
                    if len(diagnosis) >= 1: 
                        one_patient_diagnosis.append(diagnosis)
                
                if len(one_patient_diagnosis) > 1:
                    all_patient_diagnosis.append(one_patient_diagnosis)
            
        return all_patient_diagnosis

    def get_diagnosis_indice(self):
        return self.diagnosis_indice