import pandas as pd
import re
from pandas import DataFrame



def reform(df_,col1,col2,f_col):
    char1 = '/'
    char2='?'

    j=0
    images=[]
    status=[]
    for i in df_[col1]:
        i=i[15:]
        if 'http' in i :
            
            i=i[i.find(char1)+1 : i.find(char2)]
        else:
            i=i[i.find(char1)+1 :]
        images.append(i)
        status.append(df_[col2][j])
        j+=1

    df={'image_names':images,f_col:status}
    df= pd.DataFrame(df) 
    return df
    
        


df1 = pd.read_csv ('testing_data_2.csv')
df2 = pd.read_csv ('PROD_TESt_2/DEMO7.csv')


df3=reform(df1,'URL','Status','QC_out') 
print(df3)

df4=reform(df2,'image_names','result','predictions')
print(df4)


"""
df5=pd.merge(df3,df4, on='image_names', how='inner')
print(df5)
df5.to_csv('final1.csv',index=False) 


total=0
for i in range(len(df5)):
    if df5['QC_out'][i]==df5['predictions'][i]:
        total+=1
print(total,total/len(df5))
"""