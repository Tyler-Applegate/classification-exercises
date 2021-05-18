import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from env import host, user, password
import seaborn as sns
import matplotlib.pyplot as plt

def iris_melt(df):
    '''
    This function will take in the cleaned/prepped/split iris_train and return a melted
    dataframe of all numerical/continuous variables
    '''
#     melts the data into 3 cols (species, measurement, value)
# species=['versicolor', 'setosa', 'virginica']
# measurement=['sepal_length', sepal_width', 'petal_length', 'petal_width']
# value = specific numerical length/width of each measurement
    df = df[['species', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width']].melt(id_vars = ['species'],
                         var_name = 'measurement',
                         value_name = 'value')
    return df


def iris_swarm(df):
    '''
    takes in my melted iris_train df and returns a swarm plot of all numerical/
    continuous variables on the x-axis, with the value on the y-axis, and
    includes a color hue to distinguish between the 3 species
    '''
    plt.figure(figsize=(8,6))
    p = sns.swarmplot(
    x='measurement',
    y='value',
    hue='species',
    data=df,
    )
    p.set(xlabel='')
    return plt.show()