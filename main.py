from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel ,Field ,computed_field
from typing import Annotated ,Literal, Optional


app = FastAPI()

class Patient (BaseModel):

    id: Annotated[str , Field(...,description = " Patient ID" ,examples=["P001"])]
    name : Annotated[str, Field(..., description= "Patient Name")]
    city: Annotated[str , Field(..., description=" City of the Patient")]
    age : Annotated [int, Field (..., description="Age of the Patient", gt=0, lt=120)]
    gender :Annotated[ 
        Literal['male','female','others'],
        Field(...,description=" Gender of the Patient")
        ]
    height: Annotated[float,Field(...,description='Height of the Patiet in mtrs',gt=0)]
    weight: Annotated [float,Field(...,description="Weight of the patient in kg",gt=0)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi= round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:

        if self.bmi <18.5:
            return 'Underweight'
        elif 18.5<=self.bmi<24.9:
            return 'Normal Weight'
        elif 25.0<=self.bmi<29.9:
            return "Overweight"
        else:
            return "Obese"
        
class PatientUpdate(BaseModel):
    name : Annotated[Optional [str], Field(default=None)]
    city: Annotated[Optional [str] , Field(default=None)]
    age : Annotated [Optional [int], Field (default=None, gt=0,lt=120)]
    gender :Annotated[ 
        Optional[Literal['male','female','others']],
        Field(default= None)
        ]
    height: Annotated[Optional[float],Field(default=None,gt=0)]
    weight: Annotated [Optional[float],Field(default=None,gt=0)]
            
        

def load_patients_data():
    with open ('patients.json','r') as f:
        data =json.load(f)
        return data
    
def save_patients_data(data):
    with open("patients.json",'w')as f:
        json.dump(data,f)

@app.get("/")
async def read_root():
    return {"message": "Patient Management API is running"}

@app.get("/about")
async def read_about():
    return {"About": "This API manages patient data including BMI calculations and health verdicts."}

@app.get("/view")
def view_patients():
    data=load_patients_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id:str =Path(...,description="ID of the patient",example="P001")):
    data=load_patients_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="Patient not found")
    
@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by patients height, weight or bmi", example="bmi"),
    order: str = Query('asc', description="Order of sorting should be asc or desc")
):
    valid_fields=['height','weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail = f'Invalid sort_by field.Chose from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail = 'Invalid order value.Choose from asc or desc')
    
    data=load_patients_data()

    sort_order= True if order=='desc' else False

    sorted_data= sorted(data.values(), key=lambda x: x[sort_by], reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    #load existing data first

    data=load_patients_data()

    #check for duplicate patient id
    if patient.id in data:
        raise HTTPException(status_code=400,detail="Patient already exists with this ID")
    #add new patient to data

    data[patient.id]= patient.model_dump(exclude={'id'})

    #save updated data to json file 

    save_patients_data(data)
    return JSONResponse(status_code=201, content={"message":"Pateint created Successfully"})

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str,patient_update: PatientUpdate):
    
    data =load_patients_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not Found")
    existing_patient_data = data[patient_id]

    update_patient_data=patient_update.model_dump(exclude_unset=True)
    #exclude_unset=True keval vahi fields ko update karega jo user ne provide kiye hain

    for key ,value in update_patient_data.items():
        existing_patient_data[key] = value

    existing_patient_data['id']= patient_id

    pydantic_object=Patient(**existing_patient_data)#pydantic model ka object banaya

    existing_patient_data= pydantic_object.model_dump(exclude='id')

    #saving the updated data

    data[patient_id]=existing_patient_data
    save_patients_data(data)

    return JSONResponse(status_code=200,content={"message":"Patient record updated successfully"})
#endpoint for the delete

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str):

    data=load_patients_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail="Patient not found")
    
    del data[patient_id]

    save_patients_data(data)

    return JSONResponse(status_code=200,content={"message":"Patient record delete successfully"})