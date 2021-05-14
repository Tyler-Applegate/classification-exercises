import pandas as pd
import numpy as np
import os
from env import host, user, password
# general framework / template
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my env file to create a connection url to access
    the Codeup database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def prep_iris(df):
    '''
    This function will acquire the iris_db from Codeup and 
    prepare the data to be split for train / validate / test
    '''
#     drop species_id and measurement columns
    df = df.drop(columns=(['species_id', 'measurement_id']))
# Rename the species_name column to just species.
    df = df.rename(columns={'species_name': 'species'})
#     Create dummy variables of the species name.
    dummy_df = pd.get_dummies(df[['species']], dummy_na=False, drop_first=True)
# let's put it all together...
    df = pd.concat([df, dummy_df], axis=1)
    return df