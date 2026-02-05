import pandas as pd
import glob
import os
from pathlib import Path
import pandas as pd
import numpy as np

class InflationCalculator:
    def __init__(self, inflation_data_folder = 'data/historic/inflation'):
        all_files = glob.glob(os.path.join(inflation_data_folder, "*.csv"))
        self.dic_df_inflation = {}
        for file in all_files:
            df = pd.read_csv(file)
            df.columns = df.columns.str.lower()
            df.set_index('year', inplace=True)
            df.columns = ['annual_inflation']
            country = Path(file).stem
            self.dic_df_inflation[country] = df


    def list_monthly_inflation(self, country = "mixed", **kwargs):
        assert country in self.dic_df_inflation.keys() or country == "mixed"

        if 'start_year' in kwargs.keys():
            assert kwargs['start_year'] >= self.dic_df_inflation["singapore"].index.min()
            for country in self.dic_df_inflation.keys():
                self.dic_df_inflation[country] = self.dic_df_inflation[country][self.dic_df_inflation[country].index >= kwargs['start_year']]
        if 'end_year' in kwargs.keys():
            assert kwargs['end_year'] <= self.dic_df_inflation["singapore"].index.max()
            for country in self.dic_df_inflation.keys():
                self.dic_df_inflation[country] = self.dic_df_inflation[country][self.dic_df_inflation[country].index <= kwargs['end_year']]

        if country == "mixed":
            df_mixed = pd.DataFrame(index=self.dic_df_inflation["US"].index)
            for c in self.dic_df_inflation.keys():
                if df_mixed.empty:
                    df_mixed = self.dic_df_inflation[c]
                else:
                    df_mixed = df_mixed.join(self.dic_df_inflation[c], how='outer', lsuffix = f'_{c}')
            df_mixed['mixed_annual_inflation'] = df_mixed.mean(axis=1).apply(lambda x: x/100)
            return df_mixed['mixed_annual_inflation'].to_list()
        
        else:
            return self.dic_df_inflation[country]['annual_inflation'].apply(lambda x: x/100).to_list()
        
    def normal_distribution_variables(self, country = 'mixed', **kwargs):
        l_all_inflations = self.list_monthly_inflation(self, country = country, kwargs = kwargs)
        mean = sum(l_all_inflations)/len(l_all_inflations)
        std = np.std(l_all_inflations)
        return mean, std 
                




        