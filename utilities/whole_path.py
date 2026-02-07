from utilities.accumulation_account_increment import IncrementCalculator
from utilities.retirement_account_drawdown import RetirementAccountCalculator
from utilities.accumulation_account_increment_dynamic_portfolio import IncrementCalculator_DynamicPortfolio
from utilities.retirement_account_drawdown_dynamic_portfolio import RetirementAccountCalculator_DynamicPortfolio
from data.constants import Constants
from utilities.portfolio_compositors.glidepath import GlidePathCompositor

c = Constants()

c_increment = IncrementCalculator()
c_drawdown = RetirementAccountCalculator()
c_incrementDynamic = IncrementCalculator_DynamicPortfolio()
c_drawdownDynamic = RetirementAccountCalculator_DynamicPortfolio()
comp_glidepath = GlidePathCompositor()

class WholePath:
    def __init__(self):
        pass

    def whole_path_monthly_account(self, monthly_net_income, retirement_age = c.retirement_age, life_expectancy = c.life_expectancy, inflation_method = 'constant', return_method = 'constant', **kwargs):
        '''
        kwargs can take the following inputs:
        - f_portfolio_composition: whether should pay attention to portfolio composition related variables
        - portfolio_method: applicable when f_portfolio_composition = True. the method to determine portfolio composition. can be 'constant', 'glidepath', 'annual_goal_fitter'. 
        - 
        '''
        f_primary_case = False # if true, proceed with primary case coded before and without considerations of portfolio composition

        if 'f_portfolio_composition' not in kwargs.keys():
            f_primary_case = True
        elif kwargs['f_portfolio_composition'] == False:
            f_primary_case = True
        elif kwargs['f_portfolio_composition'] == True and kwargs['portfolio_method'] == 'constant':
            f_primary_case = True

        if f_primary_case:
            l_account_before_retirement = c_increment.monthly_account(monthly_net_income, retirement_age = retirement_age, inflation_method = inflation_method, return_method = return_method, **kwargs)
            capital_at_retirement = l_account_before_retirement[-1]

            l_account_after_retirement = c_drawdown.monthly_account(retirement_age = retirement_age, retirement_capital = capital_at_retirement, life_expectancy = life_expectancy, inflation_method = inflation_method, return_method = return_method, **kwargs)
            l_wholepath_account = l_account_before_retirement + l_account_after_retirement[1:]
        else:
            assert 'portfolio_method' in kwargs.keys()
            assert kwargs['portfolio_method'] in ['glidepath', 'moderator', 'polariser', 'moderator_historical', 'polariser_historical']
            assert 'proportion_stock' not in kwargs.keys() # proportion_stock should not be provided, as it will be determined by portfolio compositer

            if kwargs['portfolio_method'] == 'glidepath':
                l_account_before_retirement = c_increment.monthly_account(monthly_net_income, retirement_age = retirement_age, inflation_method = inflation_method, return_method = return_method, proportion_stock = 1, **kwargs)

                capital_at_retirement = l_account_before_retirement[-1]

                if 'glidepath_type' in kwargs.keys():
                    glidepath_type = kwargs['glidepath_type']
                    kwargs.pop('glidepath_type')
                else:
                    glidepath_type = 'linear'
                l_glidepath_monthly_returns = comp_glidepath.generate_simulated_monthly_returns(retirement_age = retirement_age, life_expectancy = life_expectancy, glidepath_type = glidepath_type, return_method = return_method, **kwargs)

                l_account_after_retirement = c_drawdown.monthly_account(retirement_age = retirement_age, retirement_capital = capital_at_retirement, life_expectancy = life_expectancy, inflation_method = inflation_method, return_method = return_method, l_simulated_monthly_returns = l_glidepath_monthly_returns, **kwargs)
                l_wholepath_account = l_account_before_retirement + l_account_after_retirement[1:]
            elif kwargs['portfolio_method'] in ['moderator', 'polariser']:
                if kwargs['portfolio_method'] == 'moderator':
                    from utilities.portfolio_compositors.moderator import Moderator 
                    strategy_portfolio = Moderator(**kwargs)
                elif kwargs['portfolio_method'] == 'polariser':
                    from utilities.portfolio_compositors.polariser import Polariser
                    strategy_portfolio = Polariser(**kwargs)

                l_account_before_retirement = c_incrementDynamic.monthly_account(monthly_net_income, strategy_portfolio, retirement_age = retirement_age, inflation_method = inflation_method, **kwargs)

                capital_at_retirement = l_account_before_retirement[-1]

                l_account_after_retirement = c_drawdownDynamic.monthly_account(strategy_portfolio, retirement_age = retirement_age, retirement_capital = capital_at_retirement, life_expectancy = life_expectancy, inflation_method = inflation_method, **kwargs)
                l_wholepath_account = l_account_before_retirement + l_account_after_retirement[1:]


        return l_wholepath_account