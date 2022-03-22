import os
import pandas as pd
from general import *


info_file = os.path.join(os.getcwd(), 'liziqi_top_10\liziqi_top_10_info.csv')
df = pd.read_csv(info_file)
print(df.columns)
print(df.iloc[1,1])