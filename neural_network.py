#from keras.src.models import Sequential
#from keras.src.layers import Dense 
#from keras.src.optimizers import Adam
#from keras.src.callbacks import EarlyStopping
#import matplotlib.pyplot as plt
#import numpy as np
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
