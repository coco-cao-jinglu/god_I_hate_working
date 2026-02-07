from utilities.calculators.historical_monthly_return_calculator import ReturnCalculator
import numpy as np

c_return = ReturnCalculator()

class ModeratorHistorical:
    def __init__(self, **kwargs):
        # include start_year and end_year for the historical return periods in **kwargs here
        self.historical_annual_median = {}
        for i in range(11):
            stock_proportion = round(i/10, 1)
            l_monthly_returns = c_return.list_monthly_portfolio_return(stock_proportion, **kwargs)
            l_annual_returns = []
            annual_cumulated = 1
            for i in range(len(l_monthly_returns)):
                if i % 12 == 0:
                    annual_cumulated = 1 + l_monthly_returns[i]
                else:
                    annual_cumulated = annual_cumulated * (1+l_monthly_returns[i])
                    if i % 12 == 11:
                        l_annual_returns.append(annual_cumulated-1)
            self.historical_annual_median[stock_proportion] = np.median(l_annual_returns)

    def _calculate_next_year_stock_proportion(self, l_monthly_returns, l_annual_stock_proportion, **kwargs):
        '''
        given historical monthly returns and historical stock proportions, calculate next year's stock proportion

        - if cumulative return does not deviate more than threshold away from cumulative return expected by having cumulative historical average returns (by percentage), continue with the same stock proportion next year
        - if this year's return goes beyond threshove percentage above historical average for the portfolio, reduce stock proportion
        - if this year's return goes beyond threshove percentage below historical average for the portfolio, increase stock proportion

        **kwargs can take:
        - sensitivity: how reactive the increment/reduction of stock proportion is 
        - deviation_threshold: the threshold used for testing of deviation
        '''
        sensitivity = 0.2
        deviation_threshold = 0.3

        if 'sensitivity' in kwargs.keys():
            assert type(kwargs['sensitivity']) == float and kwargs['sensitivity'] >= 0.1 and kwargs['sensitivity'] <= 1.0 
            sensitivity = kwargs['sensitivity']
        if 'deviation_threshold' in kwargs.keys():
            assert type(kwargs['deviation_threshold']) == float and kwargs['deviation_threshold'] > 0 and kwargs['deviation_threshold'] < 1
            deviation_threshold = kwargs['deviation_threshold']

        return_actualcumulative = np.prod([1 + x for x in l_monthly_returns]).item()
        l_annual_theoretical_return = [self.historical_annual_median[stock_proportion] for stock_proportion in l_annual_stock_proportion]
        return_theoreticalcumulative = np.prod([1 + x for x in l_annual_theoretical_return]).item()

        percentage_deviation = 1-return_actualcumulative/return_theoreticalcumulative
        if abs(percentage_deviation) <= deviation_threshold:
            return l_annual_stock_proportion[-1]
        elif percentage_deviation > deviation_threshold:
            # this year performed worse than expected from historical data
            # increase stock
            return min(1.0, round(l_annual_stock_proportion[-1]+sensitivity,1))
        else:
            return max(0.0, round(l_annual_stock_proportion[-1]-sensitivity,1))
        
    def start(self, **kwargs):
        start_proportion = 0.6
        if 'start_proportion' in kwargs.keys():
            start_proportion = kwargs['start_proportion']

        if 'f_dynamic_composition_annual_verbose' in kwargs.keys() and kwargs['f_dynamic_composition_annual_verbose'] is True:
            print('dynamic composer starts with stock ratio = ' + str(start_proportion))
        return start_proportion
    
    def generate(self, l_account_history, l_annual_stock_proportion, l_monthly_returns, **kwargs):
        # calculate annual return this year
        return self._calculate_next_year_stock_proportion(l_monthly_returns, l_annual_stock_proportion, **kwargs)




        