import pandas as pd

df= pd.read_csv("diputados.csv")
df2= pd.read_csv("diputados_votos_33633.csv")
result= pd.merge(df,df2,on='id_diputado')
result.to_csv('merge.csv')
