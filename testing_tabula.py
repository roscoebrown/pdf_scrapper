from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index
from tabula.io import read_pdf
import pandas as pd
import joiner 
import re
import glob

dir = 'output'
file = [filename for filename in glob.glob(dir)]

def rolling_group(val):
    if pd.notnull(val): rolling_group.group +=1 #pd.notnull is signal to switch group
    return rolling_group.group
rolling_group.group = 0 #static variable

# need to work on changing this def
def joinFunc(g,column):
    col =g[column]
    joiner = "/" if column == "Action" else ","
    s = joiner.join([str(each) for each in col if pd.notnull(each)])
    s = re.sub("(?<=&)"+joiner," ",s) #joiner = " "
    s = re.sub("(?<=-)"+joiner,"",s) #joiner = ""
    s = re.sub(joiner*2,joiner,s)    #fixes double joiner condition
    return s

###################    Make this a def
fc = 72
columns = [1.11,1.93,4.14,5.78,8.08,8.56,9.1,9.95]
# [top,left,bottom,width]
area_date = [.51,.3,.9,5.66]
area = [1.09,.3,7.8,10.67]
header =['County', 'Sec-Twp_Rng','Company','Well', 'Location', 'Type','Permit Number','API Number','Objective', 'Date']
#header = pd.DataFrame(header)
for i in range(len(columns)):
    columns[i]*=fc
for i in range(len(area)):  
    area[i]*=fc
    area_date[i]*=fc
#joiner.join()

df_main = read_pdf(file,pages ='all',pandas_options={'header': None},area =area, columns=columns,guess = False)
df_date = read_pdf(file,pages ='1',pandas_options={'header': None},area =area_date,guess=False)
'''
cols = header[0].values.tolist()[0]
df_main[0] = header[0].iloc[0:]
print(df_main[0])
'''
pandasdf = pd.concat(df_main)
# Add a header
#pandasdf = pd.DataFrame(pandasdf, columns = header)
pandasdf_date = pd.concat(df_date)

groups=pandasdf.groupby(pandasdf[0].apply(rolling_group), as_index = False)
groupFunct = lambda g: pd.Series([joinFunc(g,col) for col in g.columns],index=g.columns)
pd.set_option("display.max_rows", None)
Data_Sheet = groups.apply(groupFunct)
Date=pandasdf_date[1]
for i in range(1,len(Data_Sheet)):
    Data_Sheet[9]=Date[0]

Data_Sheet.to_csv('Test.csv',header=header)
print(Data_Sheet)