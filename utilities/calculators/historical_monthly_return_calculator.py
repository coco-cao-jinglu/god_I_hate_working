'''
calculate the monthly return rate based on historical data
'''

import pandas as pd
import numpy as np

class ReturnCalculator:
    def __init__(self, stock_data_path = r"data/historic/return/s&p 500_annual.csv", bond_data_path = r"data/historic/return/aaa_bond_annual.csv"):
        self.df_stock = pd.read_csv(stock_data_path)
        self.df_bond = pd.read_csv(bond_data_path)
        self.df = self.__combine_stocks_and_bonds()

    def __data_cleansing(self, df):
        df.columns = df.columns.str.lower()
        df.set_index('year', inplace=True)
        df.columns = ['annual_return'] 
        if type(df['annual_return'][2010]) == str and '%' in df['annual_return'][2010]:
            df['annual_return'] = df['annual_return'].str.rstrip('%').astype('float') / 100.0
        

    def __calculate_average_monthly_return(self, df):
        df['monthly_return'] = df['annual_return'].apply(lambda x: (1 + x) ** (1/12) - 1)


    def __combine_stocks_and_bonds(self):
        self.__data_cleansing(self.df_stock)
        self.__calculate_average_monthly_return(self.df_stock)
        self.df_stock.columns = ['stock_annual_return', 'stock_monthly_return']
        self.__data_cleansing(self.df_bond)
        self.__calculate_average_monthly_return(self.df_bond)
        self.df_bond.columns = ['bond_annual_return', 'bond_monthly_return']
        df = self.df_stock.join(self.df_bond, how='inner')
        return df 
    
    def list_monthly_portfolio_return(self, proportion_stock = 1, **kwargs):
        # assume portfolio allocates between only stock (s&p500) and bond (aaa)
        '''
        **kwargs can take:
        - start_year: start year of the historical data included for calculation
        - end_year: end year of the historical data included for calculation
        '''

        assert proportion_stock <= 1 and proportion_stock >= 0

        df = self.df.copy()
        if 'start_year' in kwargs.keys():
            assert kwargs['start_year'] >= self.df.index.min()
            df = df[df.index >= kwargs['start_year']]
        if 'end_year' in kwargs.keys():
            assert kwargs['end_year'] <= self.df.index.max()
            df = df[df.index <= kwargs['end_year']]

        l_returns = df['stock_monthly_return'].apply(lambda x: x * proportion_stock) + df['bond_monthly_return'].apply(lambda x: x * (1 - proportion_stock))
        l_returns = l_returns.to_list()
        return l_returns
    
    def normal_distribution_variables(self, proportion_stock = 1, **kwargs):
        l_all_returns = self.list_monthly_portfolio_return(proportion_stock = proportion_stock, **kwargs)
        mean = sum(l_all_returns)/len(l_all_returns)
        std = np.std(l_all_returns)
        return mean, std 

    
    
    
    