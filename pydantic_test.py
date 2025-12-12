from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int

def insert_patient(patient : Patient):
    # Function to insert a patient record into the database
    print(patient.name)
    print(patient.age)
    print("Inserting patient into database")

patient_info= {"name":"ABHI","age":"30"}
patient1=Patient(**patient_info)

insert_patient(patient1)