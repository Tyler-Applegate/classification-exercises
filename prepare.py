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


################## Titanic Time#########################

def titantic_split(df):
    '''
    This function will take in the titanic data acquired by get_titanic_data,
    performs a split, and stratifies column.
    Returnd train, validate, and test DataFrames.
    '''
    train_validate, test = train_test_split(df, test_size=0.2,
                            random_state=1221,
                            stratify=df.survived)
    train, validate = train_test_split(train_validate, test_size=0.3,
                                    random_state=1221,
                                    stratify=train_validate.survived)
    return train, validate, test


def impute_mean_age(train, validate, test):
    '''
    This function imputes the mean of the age column for
    observations with missing values.
    Returns transformed train, validate, and test df.
    '''
    # create the imputer object with mean strategy
    imputer = SimpleImputer(strategy = 'mean')
    
    # fit on and transform age column in train
    train['age'] = imputer.fit_transform(train[['age']])
    
    # transform age column in validate
    validate['age'] = imputer.transform(validate[['age']])
    
    # transform age column in test
    test['age'] = imputer.transform(test[['age']])
    
    return train, validate, test

def prep_titanic(df):
    '''
    This function take in the titanic data acquired by get_titanic_data,
    Returns prepped train, validate, and test dfs with embarked dummy vars,
    deck dropped, and the mean of age imputed for Null values.
    '''
    
    # drop rows where embarked/embark town are null values
    df = df[~df.embarked.isnull()]
    
    # encode embarked using dummy columns
    titanic_dummies = pd.get_dummies(df.embarked, drop_first=True)
    
    # join dummy columns back to df
    df = pd.concat([df, titanic_dummies], axis=1)
    
    # drop the deck column
    df = df.drop(columns='deck')
    
    # split data into train, validate, test dfs
    train, validate, test = titanic_split(df)
    
    # impute mean of age into null values in age column
    train, validate, test = impute_mean_age(train, validate, test)
    
    return train, validate, test