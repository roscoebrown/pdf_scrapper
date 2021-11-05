from pandas.core.frame import DataFrame
from pandas.core.indexes.base import Index
from tabula.io import read_pdf
import pandas as pd
import joiner 
import re
import glob

# add __init__"name"

dir = '.\output\*.pdf'
file = [filename for filename in glob.glob(dir)]
print(file)
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

fc = 72
columns = [1.11,1.93,4.14,5.78,8.08,8.56,9.1,9.95]
# [top,left,bottom,width]
area_date = [.51,.3,.9,5.66]
area = [1.09,.3,7.8,10.67]
header =['County', 'Sec-Twp_Rng','Company','Well', 'Location', 'Type','Permit Number','API Number','Objective', 'Date']#
pandasdf = pd.DataFrame()
pandasdf_date = pd.DataFrame()

number = []
date_comb = []
df_multi=[]
Data_Sheet = pd.array([1,2,3,4,5,6,7,8,9])
#header = pd.DataFrame(header)
for i in range(len(columns)):
    columns[i]*=fc
for i in range(len(area)):  
    area[i]*=fc
    area_date[i]*=fc
#joiner.join()

for pdffilepath in file:
    df_main = read_pdf(pdffilepath,pages ='all',pandas_options={'header': None},area =area, columns=columns,guess = False)
    df_date = read_pdf(pdffilepath,pages ='1',pandas_options={'header': None},area =area_date,guess=False)
    
    df_multi += df_main
    pandasdf = pd.concat(df_multi)
      
    date_comb += df_date

    pandasdf_date = pd.concat(date_comb)
    groups=pandasdf.groupby(pandasdf[0].apply(rolling_group), as_index = False)
    groupFunct = lambda g: pd.Series([joinFunc(g,col) for col in g.columns],index=g.columns)

    Data_Sheet = groups.apply(groupFunct)
    number +=[len(Data_Sheet)]
    
    # Clean up the variables
    DataBase = Data_Sheet

print(number)

pd.set_option("display.max_rows", None,"display.max_columns", None)
#,"display.max_columns", None

number_p2=[0,0,0,0]

print('')

# number works fine
for j in range(0,len(number)):
    if j ==0:
        number_p2[j]=number[j]
    elif 0 < j < (len(number)):
        number_p2[j] = number[j]-number[j-1]
    else:
        number_p2[j] = 'error: out of bounds'

print(number_p2)
#number[1] = number[1]-number[0]
a=[]

for j in range(0,len(number)):
    for i in range(0,number_p2[j]):
        a.append(date_comb[j][1][0][:])
        continue

a=list(a)


# Take away the 0 in the index

DataBase['9']=a
print(DataBase)

DataBase.to_csv('Test.csv',header=header)




