from PostgreSQLManager import PostgreSQLQueryManager
import os
class CdmQueryManager():
    def __init__(self, cfg_file_name, section, schema):
        path  = os.getcwd() + "/" + cfg_file_name
        self.postgres = PostgreSQLQueryManager(path, section)
        self.schema = schema
        self.diagnosis = ['Hyperparathyroidism', 'Hyperthyroidism', 'Neoplasm of thyroid gland', 'Neoplasm of parathyroid gland']
    def select_person_date_by_diagnosis(self):
        result = self.postgres.selectList(
            """
            select person_id, max(condition_start_date)
            from %s.condition_occurrence
            where condition_concept_id in (select concept_id from %s.concept where 
            concept_name similar to '%%(%s)%%'
            group by person_id
            """ % (self.schema, self.schema, "|".join(self.diagnosis))
            )
        return result

    def select_admission(self, person_id, start_date):
        result = self.postgres.selectList(
                """
                select *
                from %s.condition_occurrence a
                inner join %s.concept b
                on a.condition_concept_id = b.concept_id
                where person_id = %d and condition_start_date <= '%s'
                order by person_id, condition_start_date
                """ % (self.schema, self.schema, person_id, start_date)
        )
        return result

    def select_patients(self, patient_ids):
        
        query = """
                select *
                from %s.person
                where person_id in (%s)
                """ % (self.schema, ", ".join(patient_ids))
        result = self.postgres.selectList(query)
        return result

    def select_admissions_max_day(self, limit, offset):
        query = """
            select b.person_id, b.condition_concept_id, 
            (select concept_name from %s.concept where concept_id = b.condition_concept_id),
            b.condition_start_date
            from (select person_id, max(condition_start_date) as condition_start_date
            from %s.condition_occurrence a
            inner join %s.concept b
            on a.condition_concept_id = b.concept_id
            where b.concept_name similar to '%%(%s)%%'
            group by a.person_id
            limit %d offset %d) a left outer join %s.condition_occurrence b
            on a.person_id = b.person_id and b.condition_start_date <= a.condition_start_date
            order by b.person_id, condition_start_date
            """ % (self.schema, self.schema, self.schema, "|".join(self.diagnosis), limit, offset, self.schema)
        result = self.postgres.selectList(query)
        return result

    def select_admissions_max_twoday(self, limit, offset):
        query = """
            select b.person_id, b.condition_concept_id, 
            (select concept_name from %s.concept where concept_id = b.condition_concept_id),
            b.condition_start_date
	        from (

            select a.person_id, MAX(b.condition_start_date) as second_max_date, 
            MAX(a.condition_start_date) as max_date from

            (
            select person_id, MAX(condition_start_date) as condition_start_date
            from %s.condition_occurrence a
            inner join %s.concept b
            on a.condition_concept_id = b.concept_id
            where concept_name similar to '%%(%s)%%'
                

	        group by person_id
            limit %d offset %d
            ) a left outer join %s.condition_occurrence b
            on a.person_id = b.person_id and b.condition_start_date < a.condition_start_date
	        group by a.person_id ) a inner join %s.condition_occurrence b
	        on a.person_id = b.person_id and (a.second_max_date = b.condition_start_date 
            or a.max_date = b.condition_start_date)
		    order by person_id, condition_start_date
            
            """ %(self.schema, self.schema, self.schema, "|".join(self.diagnosis), limit, offset, self.schema, self.schema)
        result = self.postgres.selectList(query)
        return result

    def select_person_count(self):
        query = """
            select count(*) as count from (select person_id
            from %s.condition_occurrence a
            inner join %s.concept b
            on a.condition_concept_id = b.concept_id
            where concept_name similar to '%%(%s)%%'
	        group by person_id) a
            """ % (self.schema, self.schema, "|".join(self.diagnosis))

        result = self.postgres.selectList(query)
        return result[0][0]