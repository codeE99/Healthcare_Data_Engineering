#!/usr/bin/env python
# coding: utf-8

import kagglehub as kh
import pandas as pd
from sqlalchemy import create_engine
import os 

def run():

    path = kh.dataset_download("prasad22/healthcare-dataset")

    dtype={
        "Name":"string",
        "Age":"Int64",
        "Gender":"string",
        "Blood Type":"string",
        "Medical Condition":"string",
        "Doctor":"string",
        "Hospital":"string",
        "Billing Amount":"float64",
        "Room Number":"Int64", 
        "Admission Type":"string",
        "Medication":"string",
        "Test Results":"string"
    }

    parse_dates=[
        "Date of Admission",
        "Discharge Date"
    ]

    hd=pd.read_csv(f"{path}/healthcare_dataset.csv", dtype=dtype, parse_dates=parse_dates)

    hd['Name']=hd['Name'].str.title()
    hd['Billing Amount']=hd['Billing Amount'].round(2)

    print(hd.isnull().sum())

    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")
    db_host= os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    

    engine = create_engine(f'postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

    patient_df=hd[['Age','Gender','Blood Type']]
    patient_df[['First Name', 'Last Name']]=hd['Name'].str.split(' ', n=1, expand=True)
    patient_df['Patient ID']=hd.groupby(['Name']).ngroup()
    patient_df=patient_df[['Patient ID', 'First Name','Last Name','Age','Gender','Blood Type']]

    hospital_df=hd[['Hospital']]

    doctor_df=pd.DataFrame(columns=['Doctor ID', 'First Name', 'Last Name'])
    doctor_df[['First Name','Last Name']]=hd['Doctor'].str.split(' ',n=1,expand=True)
    doctor_df['Doctor ID']=hd.groupby(['Doctor']).ngroup()

    case_df=pd.DataFrame(columns=['Case ID', 'Patient ID', 'Doctor ID', 'Date of Admission', 'Discharge Date', 'Medical Condition', 'Billing Amount', 'Medication', 'Admission Type', 'Test Results', 'Insurance Provider', 'Room Number'])
    case_df['Patient ID']=patient_df['Patient ID']
    case_df['Doctor ID']=doctor_df['Doctor ID']
    case_df[[ 'Medical Condition','Date of Admission'  , 'Insurance Provider','Billing Amount',  'Room Number','Admission Type', 'Discharge Date','Medication', 'Test Results']]=hd[['Medical Condition','Date of Admission'  , 'Insurance Provider','Billing Amount',  'Room Number','Admission Type', 'Discharge Date','Medication', 'Test Results']]
    case_df['Case ID']=patient_df['First Name'].str[0]+patient_df['Last Name'].str[0]+"--"+[str(1000+i) for i in range(len(case_df))]


    print(pd.io.sql.get_schema(patient_df, name='Patient'))
    print(pd.io.sql.get_schema(hospital_df, name='Hospital'))
    print(pd.io.sql.get_schema(doctor_df, name='Doctor'))
    print(pd.io.sql.get_schema(case_df, name='Case'))

    first=True
    if first==True:
        patient_df.head(0).to_sql(name='Patient', con=engine, if_exists='replace')
        doctor_df.head(0).to_sql(name='Doctor', con=engine, if_exists='replace')
        hospital_df.head(0).to_sql(name='Hospital', con=engine, if_exists='replace')
        case_df.head(0).to_sql(name='Case', con=engine, if_exists='replace')
        first=False

    patient_df.to_sql(name='Patient', con=engine, if_exists='append', index=False, chunksize=5000)
    doctor_df.to_sql(name='Doctor', con=engine, if_exists='append', index=False, chunksize=5000 )
    hospital_df.to_sql(name='Hospital', con=engine, if_exists='append', index=False, chunksize=5000 )
    case_df.to_sql(name='Case', con=engine, if_exists='append', index=False, chunksize=5000 )

if __name__=="__main__":
    run()