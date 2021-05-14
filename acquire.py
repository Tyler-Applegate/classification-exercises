# Make a new python module, acquire.py to hold the following data aquisition functions:
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

# now let's get some data...

def get_db_data():
    '''
    This function reads data from the Codeup db into a pandas DataFrame.
    '''
    sql_query = 'inset sql query here; TEST in SQL Ace 1st!'
    return pd.read_sql(sql_query, get_connection('db_name'))

# Make a function named get_titanic_data that returns the titanic data from the codeup data science 
# database as a pandas data frame. Obtain your data from the Codeup Data Science Database.

def new_titanic_data():
    '''This functions reads in the titanic db from Codeup db
    and returns a pandas DataFrame with all columns/values.
    '''
    sql_query = 'SELECT * FROM passengers'
    return pd.read_sql(sql_query, get_connection('titanic_db'))

# Make a function named get_iris_data that returns the data from the iris_db on the codeup data science 
# database as a pandas data frame. The returned data frame should include the actual name of the species 
# in addition to the species_ids. Obtain your data from the Codeup Data Science Database.

def new_iris_data():
    '''
    This function joins the 'measurements' and 'species' tables from the Codeup db
    and return a pandas DataFrame will call columns/values from both tables.
    '''
    sql_query = 'SELECT * FROM measurements JOIN species USING (species_id)'
    return pd.read_sql(sql_query, get_connection('iris_db'))



# Once you've got your get_titanic_data and get_iris_data functions written, now it's time to add caching to them. 
# To do this, edit the beginning of the function to check for a local filename like titanic.csv or iris.csv. 
# If they exist, use the .csv file. If the file doesn't exist, then produce the SQL and pandas necessary to 
# create a dataframe, then write the dataframe to a .csv file with the appropriate name.

def get_iris_data():
    '''
    This function reads in iris data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('iris_df.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('iris_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_iris_data()
        
        # Cache data
        df.to_csv('iris_df.csv')
        
    return df

# getting titanic db from a csv

def get_titanic_data():
    '''
    This function reads in titanic data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('titanic_df.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('titanic_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = new_titanic_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('titanic_df.csv')
        
    return df