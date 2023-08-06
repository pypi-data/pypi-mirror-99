import pandas as pd 

def bike_format(bike):
    bike['Date'] = pd.to_datetime(bike['Date'])
    bike.columns=['Date','Heure','Grandtotal','Todaystotal', 'Unnamed','Remark'] ##rename the columns
    ##remove useless columns 
    bike.pop("Unnamed")
    bike.pop("Remark")
    bike.pop("Grandtotal")

    bike.drop(0,0,inplace=True)
    bike.drop(1,0,inplace=True)
    bike['Heure'].fillna(0, inplace = True)
    return bike
