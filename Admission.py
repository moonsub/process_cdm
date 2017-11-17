class Admission():
    
    def __init__(self, person_id, diagnosis_id, diagnosid_name, admit_date):
        
        self.person_id = person_id
        self.diagnosis_id = diagnosis_id
        self.diagnosis_name = diagnosid_name
        self.admit_date = admit_date

    def get_person_id(self):
        return self.person_id

    def get_diagnosis_id(self):
        return self.diagnosis_id

    def get_diagnosis_name(self):
        return self.diagnosis_name

    def get_admit_date(self):
        return self.admit_date

    def __str__(self):
        return """
            person_id : %d, diagnosis_id : %d, diagnosis_name : %s, admit_date : %s
            """ % (self.person_id, self.diagnosis_id, self.diagnosis_name, self.admit_date)