import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from env import host, user, password

# general framework / template
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my env file to create a connection url to access
    the Codeup database.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

################ iris tools ##############################

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

def iris_split(df):
    '''
    This function will take in the iris data acquired by get_iris_data,
    performs a split, and stratifies column.
    Returnd train, validate, and test DataFrames.
    '''
    train_validate, test = train_test_split(df, test_size=0.2,
                            random_state=1221,
                            stratify=df.species)
    train, validate = train_test_split(train_validate, test_size=0.3,
                                    random_state=1221,
                                    stratify=train_validate.species)
    return train, validate, test

################## Titanic Time#########################

def split_data(df):
    '''
    take in a DataFrame and return train, validate, and test DataFrames; stratify on survived.
    return train, validate, test DataFrames.
    '''
    train_validate, test = train_test_split(df, test_size=.2, random_state=123, stratify=df.survived)
    train, validate = train_test_split(train_validate, 
                                       test_size=.3, 
                                       random_state=123, 
                                       stratify=train_validate.survived)
    return train, validate, test

def impute_mode(train, validate, test, column , method):
    '''
    impute a choosen strategy (method) for age column into observations with missing values.
    column:  is the column to impute or fill the missing values in and 
    method:  is the type of strategy(media, media, most_frequent)
    '''
    imputer = SimpleImputer(strategy= method, missing_values= np.nan)
    train[[column]] = imputer.fit_transform(train[[column]])
    validate[[column]] = imputer.transform(validate[[column]])
    test[[column]] = imputer.transform(test[[column]])
    return train, validate, test


def prep_titanic_data(df, column, method ,dummies):
    '''
    takes in a dataframe of the titanic dataset that was  acquired before and returns a cleaned dataframe
    arguments:
    - df: a pandas DataFrame with the expected feature names and columns
    - column : the name of the column to fill or impute the missing values in
    - method: type of strategy (median, mean, most_frequent) for SimpleImputer
    - dummies: list of columns to create a dummy variable 
    return: 
    train, validate, test (three dataframes with the cleaning operations performed on them)
    '''
    #clean data
    df = df.drop_duplicates()
    df = df.drop(columns=['deck', 'embark_town', 'class'])
    
    #create a dummy df
    dummy_df = pd.get_dummies(df[dummies], drop_first=[True, True])
    ## Concatenate the dummy_df dataframe above with the original df
    df = pd.concat([df, dummy_df], axis=1)
    
    # drop the deck column
    df = df.drop(columns= dummies)
    #split data
    
    # split data into train, validate, test dfs
    train, validate, test = split_data(df)

    # impute the chosen strategy (median)  for  the selected column (age) into null values in age column
    train, validate, test = impute_mode(train, validate, test, column , method)
   
    return train, validate, test


########### To Code along with Madeleine #################

def train_validate_test_split(df, seed=123):
    train_and_validate, test = train_test_split(
        df, test_size=0.2, random_state=seed, stratify=df.survived
    )
    train, validate = train_test_split(
        train_and_validate,
        test_size=0.3,
        random_state=seed,
        stratify=train_and_validate.survived,
    )
    return train, validate, test