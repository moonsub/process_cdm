class Index():
    def __init__(self, index, diagnosis_id, diagnosis_name):
            
        self.index = index
        self.diagnosis_id = diagnosis_id
        self.diagnosis_name = diagnosis_name

    def get_index(self):
        return self.index

    def get_diagnosis_id(self):
        return self.diagnosis_id

    def get_diagnosis_name(self):
        return self.diagnosis_name

    def __str__(self):
        return """
            index : %d, diagnosis_id : %d, diagnosis_name : %s
            """ % (self.index, self.diagnosis_id, self.diagnosis_name)