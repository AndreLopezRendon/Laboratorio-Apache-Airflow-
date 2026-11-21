import pandas as pd
def validate(df):
 return {"rows":len(df),"nulls":int(df.isna().sum().sum())}
