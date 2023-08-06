import pandas as pd 
from download import download 

class Load_data:
    def __init__(self,url, target_name):
        download(url, target_name, replace=True)
    @staticmethod
    def save_as_df(path_target):
        df = pd.read_csv(path_target, na_values="", low_memory=False)
        return df 