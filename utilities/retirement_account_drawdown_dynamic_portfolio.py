from data.constants import Constants
from data.expenses import ExpensesAfterRetirement
from utilities.simulators.economics.annual_inflation_simulator import InflationSimulator
from utilities.simulators.economics.monthly_investment_return_simulator import ReturnSimulator

c = Constants()
e = ExpensesAfterRetirement()
s_inflation = InflationSimulator()
s_return = ReturnSimulator()

class RetirementAccountCalculator_DynamicPortfolio:
    def __init__(self):
        pass 


    def monthly_account(self, dynamic_portfolio_strategy, retirement_age = c.retirement_age, retirement_capital = c.retirement_capital, life_expectancy = c.life_expectancy, inflation_method = 'constant', **kwargs):
        '''
        dynamic_portfolio_strategy expects an object with (1) a "generate" function which, given past account value and portfolio composition information thus far, would give stock proportion for coming year (2) a "start" function which gives a beginning stock proportion value

        assumes return simulation is normally distributed from historical values 


        kwargs can take the following inputs:
        - c_inflation_constant: applicable when return_method = 'constant'. the assumed constant inflation for annual inflation simulator. optional even if 'inflation_method' == 'constant', as constant simulator has a default value
        - proportion_stock: applicable when return_method = 'normal' or 'bootstrap'. the assumed proportion of stock in the portfolio for monthly investment return simulator. optional, as normal and bootstrap simulators have a default value of 1 (100% stock portfolio)
        - l_simulated_monthly_returns: applicable when return_method = 'normal' or 'bootstrap'. the list of simulated monthly returns to use for monthly investment return simulator. optional. for the purpose of portfolio-compositor related calculations. the simulated return generation will be handled inside whole_path calculator. so the drawdown calculator expect to be fed the already simulated returns
        - inflation_country: applicable when inflation_method = 'normal' or 'bootstrap'. the country for historical annual inflation data. optional, as normal and bootstrap simulators have a default value of 'mixed', which averages over all available countries (US, UK, singapore, spain)
        '''
        account = retirement_capital
        l_account_history = [account]
        l_annual_inflation = []
        l_monthly_return = []
        l_annual_stock_proportion = [dynamic_portfolio_strategy.start(**kwargs)]

        # generate inflation
        assert inflation_method in ['constant', 'normal', 'bootstrap']

        if inflation_method == 'constant':
            if 'c_inflation_constant' in kwargs.keys():
                i_constant = kwargs['c_inflation_constant']
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.constant(i_constant))
            else:
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.constant())
        if inflation_method == 'normal':
            if 'inflation_country' in kwargs.keys():
                inflation_country = kwargs['inflation_country']
                kwargs.pop('inflation_country')
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.normal(country = inflation_country, kwargs = kwargs))
            else:
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.normal(kwargs = kwargs))
        if inflation_method == 'bootstrap':
            if 'inflation_country' in kwargs.keys():
                inflation_country = kwargs['inflation_country']
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.bootstrap(country = inflation_country, **kwargs))
            else:
                for _ in range(life_expectancy - c.current_age):
                    l_annual_inflation.append(s_inflation.bootstrap(**kwargs))
            
        
        accumulated_inflation = 1
        for i in range(retirement_age - c.current_age):
            accumulated_inflation = accumulated_inflation * (1+l_annual_inflation[i])

        for i in range((life_expectancy - retirement_age) * 12):

            # retirement setup
            if i == 0:
                account = account - e.retirement_setup_onetime * accumulated_inflation - e.monthly_expenditure() * accumulated_inflation
            else:
                account = account - e.monthly_expenditure() * accumulated_inflation
            
            monthly_return = s_return.normal(proportion_stock=l_annual_stock_proportion[-1], kwargs = kwargs) 
            account = account * (1+monthly_return)
            l_account_history.append(account)
            l_monthly_return.append(monthly_return)

            if i % 12 == 0:
                i_inflation_year = int(i/12)+(retirement_age - c.current_age) - 1
                accumulated_inflation = accumulated_inflation * (1+l_annual_inflation[i_inflation_year])

                # portfolio composition is annually adjusted
                if i != 0:
                    next_stock_proportion = dynamic_portfolio_strategy.generate(l_account_history, l_annual_stock_proportion, **kwargs)
                    l_annual_stock_proportion.append(next_stock_proportion)

                    if 'f_dynamic_composition_annual_verbose' in kwargs.keys() and kwargs['f_dynamic_composition_annual_verbose'] is True:
                        if l_annual_stock_proportion[-1] != l_annual_stock_proportion[-2]:
                            print('dynamic composer changes portfolio stock ratio to ' + str(next_stock_proportion))

        return l_account_history

            