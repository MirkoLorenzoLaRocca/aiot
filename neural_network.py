#from keras.src.models import Sequential
#from keras.src.layers import Dense 
#from keras.src.optimizers import Adam
#from keras.src.callbacks import EarlyStopping
#import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd

path = fr'tactigon\csvcomplete'
df1, df2, df3, df4 = pd.DataFrame(path+fr'\registrazionidx_complete.csv', path+fr'\registrazionigiù_complete.csv'), 
pd.DataFrame(path+fr'\registrazionisopra_complete.csv'), pd.DataFrame(path+fr'\registrazionisx_complete.csv')
train_set = pd.concat([df1, df2, df3, df4])
print(train_set.head())