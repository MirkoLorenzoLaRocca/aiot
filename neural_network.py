#from keras.src.models import Sequential
#from keras.src.layers import Dense 
#from keras.src.optimizers import Adam
#from keras.src.callbacks import EarlyStopping
#import matplotlib.pyplot as plt
#import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.
import pandas as pd

#path
path = fr'tactigon\csvcomplete'

# da csv a df
df1 = pd.read_csv(path + fr'\registrazionidx_complete.csv')
df2 = pd.read_csv(path + fr'\registrazionigiù_complete.csv')
df3 = pd.read_csv(path + fr'\registrazionisopra_complete.csv')
df4 = pd.read_csv(path + fr'\registrazionisx_complete.csv')

# Concatenazione dei DataFrame
train_set = pd.concat([df1, df2, df3, df4])

# Controllo concat
print(train_set.head())

x, y = train_set.drop(columns=['verso']), train_set['verso']
x = x.drop(columns=['timestamp'])

# x = fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.15, random_state=88, shuffle=True, stratify=y)

random_forest = RandomForestClassifier(
    n_estimators=100,
    criterion = 'entropy',
    oob_score=True)

random_forest.fit(x_train, y_train)

