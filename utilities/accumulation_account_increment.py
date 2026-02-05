from data.constants import Constants
from data.expenses import ExpenditureBeforeRetirement
from utilities.simulators.economics.annual_inflation_simulator import InflationSimulator
from utilities.simulators.economics.monthly_investment_return_simulator import ReturnSimulator

import numpy as np

c = Constants()
e = ExpenditureBeforeRetirement()
s_inflation = InflationSimulator()
s_return = ReturnSimulator()

class IncrementCalculator:
    def __init__(self):
        pass 

    def monthly_account(self, monthly_income, retirement_age = c.retirement_age, inflation_method = 'constant', return_method = 'constant', **kwargs):
        '''
        kwargs can take the following inputs:
        - c_inflation_constant: applicable when return_method = 'constant'. the assumed constant inflation for annual inflation simulator. optional even if 'inflation_method' == 'constant', as constant simulator has a default value
        - c_return_constant : applicable when return_method = 'constant'. the assumed constant inflation for monthly investment return simulator. optional even if 'return_method' == 'constant', as constant simulator has a default value
        - proportion_stock: applicable when return_method = 'normal' or 'bootstrap'. the assumed proportion of stock in the portfolio for monthly investment return simulator. optional, as normal and bootstrap simulators have a default value of 1 (100% stock portfolio)
        - inflation_country: applicable when inflation_method = 'normal' or 'bootstrap'. the country for historical annual inflation data. optional, as normal and bootstrap simulators have a default value of 'mixed', which averages over all available countries (US, UK, singapore, spain)
        '''
        account = c.current_capital
        l_account_history = [account]
        l_annual_inflation = []
        l_monthly_return = []

        # generate inflation
        assert inflation_method in ['constant', 'normal', 'bootstrap']

        if inflation_method == 'constant':
            if 'c_inflation_constant' in kwargs.keys():
                i_constant = kwargs['c_inflation_constant']
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.constant(i_constant))
            else:
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.constant())
        if inflation_method == 'normal':
            if 'inflation_country' in kwargs.keys():
                inflation_country = kwargs['inflation_country']
                kwargs.pop('inflation_country')
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.normal(country = inflation_country, kwargs = kwargs))
            else:
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.normal(kwargs = kwargs))
        if inflation_method == 'bootstrap':
            if 'inflation_country' in kwargs.keys():
                inflation_country = kwargs['inflation_country']
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.bootstrap(country = inflation_country, **kwargs))
            else:
                for _ in range(retirement_age - c.current_age):
                    l_annual_inflation.append(s_inflation.bootstrap(**kwargs))
            
        # generate return
        assert return_method in ['constant', 'normal', 'bootstrap']
        if return_method == 'constant':
            if 'c_return_constant' in kwargs.keys():
                i_constant = kwargs['c_return_constant']
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.constant(i_constant))
            else:
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.constant())

        if return_method == 'normal':
            if 'proportion_stock' in kwargs.keys():
                proportion_stock = kwargs['proportion_stock']
                kwargs.pop('proportion_stock')
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.normal(proportion_stock=proportion_stock, kwargs = kwargs))
            else:
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.normal(kwargs = kwargs))

        if return_method == 'bootstrap':
            if 'proportion_stock' in kwargs.keys():
                proportion_stock = kwargs['proportion_stock']
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.bootstrap(proportion_stock=proportion_stock, **kwargs))
            else:
                for _ in range((retirement_age - c.current_age)*12):
                    l_monthly_return.append(s_return.bootstrap(**kwargs))

        if 'f_monthly_verbose' in kwargs.keys() and kwargs['f_monthly_verbose'] == True:
            print('l_annual_inflation:', l_annual_inflation)
            print('l_monthly_return:', l_monthly_return)
        
        accumulated_inflation = 1

        for i in range((retirement_age - c.current_age) * 12):


            account = account + monthly_income * np.power(1+c.average_annual_salary_increment,int(i/12)) - e.monthly_expenditure() * accumulated_inflation
            
            account = account * (1+l_monthly_return[i])
            l_account_history.append(account)

            if i % 12 == 0 and i != 0:
                i_inflation_year = int(i/12) - 1
                accumulated_inflation = accumulated_inflation * (1+l_annual_inflation[i_inflation_year])

        return l_account_history

            