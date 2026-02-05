from utilities.accumulation_account_increment import IncrementCalculator
from utilities.retirement_account_drawdown import RetirementAccountCalculator
from data.constants import Constants

c = Constants()

c_increment = IncrementCalculator()
c_drawdown = RetirementAccountCalculator()

class WholePath:
    def __init__(self):
        pass

    def whole_path_monthly_account(self, monthly_net_income, retirement_age = c.retirement_age, life_expectancy = c.life_expectancy, inflation_method = 'constant', return_method = 'constant', **kwargs):
        l_account_before_retirement = c_increment.monthly_account(monthly_net_income, retirement_age = retirement_age, inflation_method = inflation_method, return_method = return_method, **kwargs)
        capital_at_retirement = l_account_before_retirement[-1]

        l_account_after_retirement = c_drawdown.monthly_account(retirement_age = retirement_age, retirement_capital = capital_at_retirement, life_expectancy = life_expectancy, inflation_method = inflation_method, return_method = return_method, **kwargs)
        l_wholepath_account = l_account_before_retirement + l_account_after_retirement[1:]

        return l_wholepath_account