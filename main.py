from CdmQueryManager import CdmQueryManager
from CdmToTrainDataConverter import CdmToTrainDataConverter
from Admission import Admission
import cPickle as pickle

def divideTrainValidTestFiles(patientDiagnosesArray):
    print 'divideTrainValidTestFiles Start'
	
    validData = []
    testData = []

    personCount = len(patientDiagnosesArray)
	
	
    trainEndIndex = int(personCount * 0.8)
    validEndIndex = personCount

    i = 0
    
    while i < trainEndIndex:
        validData.append(patientDiagnosesArray[i])
        i = i + 1

    while i < validEndIndex:
        testData.append(patientDiagnosesArray[i])
        i = i + 1

    return validData, testData

if __name__ == "__main__":
    
    outFile = '/Users/xiilab/Desktop/dev/git/process_cdm/'
    

    '''
    for i in range(1, 2):
        section = 'PostgreSQLConnect' + str(i)
        
        query_manager = CdmQueryManager('config.cfg', section, 'synpuf5')
        result_db = query_manager.select_person_date_by_diagnosis()
        print len(result_db)
        person_count_db = len(result_db)
        train_person_count_db = int(person_count_db * 0.8)
        for person_date in result_db[:train_person_count_db]:
            admissions = query_manager.select_admission(person_date[0], person_date[1])
           
            for admission in admissions:
                train_admit_result.append(Admission(int(admission[1]), int(admission[2]), admission[12], admission[4]))
                

        for person_date in result_db[train_person_count_db:]:
            admissions = query_manager.select_admission(person_date[0], person_date[1])
            
            for admission in admissions:
                test_admit_result.append(Admission(int(admission[1]), int(admission[2]), admission[12], admission[4]))
        print (train_admit_result)
        print (test_admit_result)
    '''
    train_admit_result = [] 
    valid_admit_result = []
    test_admit_result = []

    for i in range(1, 5):
        section = 'PostgreSQLConnect' + str(i)
        query_manager = CdmQueryManager('config.cfg', section, 'synpuf5')
        person_count = query_manager.select_person_count()
        print(person_count)

        person_train_count = int(person_count * 0.6)
        person_valid_count = int(person_count * 0.2)
        print 'train_person_count : ' + str(person_train_count)
        print 'valid_test_person_count : ' + str(person_valid_count)

        result = query_manager.select_admissions_max_twoday(person_train_count, 0)
        print 'train_admit_count : ' + str(len(result))
        for admission in result:
            train_admit_result.append(Admission(int(admission[0]), int(admission[1]), admission[2], admission[3]))  

        print len(train_admit_result)

        result = query_manager.select_admissions_max_twoday(person_valid_count, person_train_count)
        print 'valid_admit_count : ' + str(len(result))
        for admission in result:
            valid_admit_result.append(Admission(int(admission[0]), int(admission[1]), admission[2], admission[3]))  

        print len(train_admit_result)

        result = query_manager.select_admissions_max_twoday(person_train_count, person_train_count + person_valid_count)
        print 'test_admit_count : ' + str(len(result))
        for admission in result:
            test_admit_result.append(Admission(int(admission[0]), int(admission[1]), admission[2], admission[3]))  
        
        print len(test_admit_result)
    

    converter = CdmToTrainDataConverter()
    converter.set_index_data(train_admit_result)

    train_result = converter.get_model_data(train_admit_result)
    valid_result = converter.get_model_data(valid_admit_result)
    test_result = converter.get_model_data(test_admit_result)

    diagnosis_indice = converter.get_diagnosis_indice()

    
    pickle.dump(train_result, open(outFile+'data.train', 'wb'), -1)
    pickle.dump(valid_result, open(outFile+'data.valid', 'wb'), -1)
    pickle.dump(test_result, open(outFile+'data.test', 'wb'), -1)
#    pickle.dump(test_result, open(outFile+'test', 'wb'), -1)
    pickle.dump(diagnosis_indice, open(outFile+'data.index', 'wb'), -1)

'''
    converter = CdmToTrainDataConverter(admit_result)
    visit_file, diagnosis_index = converter.get_model_data(admit_result)

    train_data, valid_data, test_data = divideTrainValidTestFiles(visit_file)

    pickle.dump(train_data, open(outFile+'.train', 'wb'), -1)
    pickle.dump(valid_data, open(outFile+'.valid', 'wb'), -1)
    pickle.dump(test_data, open(outFile+'.test', 'wb'), -1)
    pickle.dump(diagnosis_index, open(outFile+'.index', 'wb'), -1)
'''

