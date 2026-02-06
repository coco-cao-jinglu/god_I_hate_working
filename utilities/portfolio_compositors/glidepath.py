from data.constants import Constants
from utilities.simulators.economics.monthly_investment_return_simulator import ReturnSimulator


c = Constants()
s_return = ReturnSimulator()

class GlidePathCompositor:
    # compose the after retirement glidepath
    def __init__(self):
        pass    

    def _y_concave(self, x, alpha, p):
        """
        Concave decreasing function, where y=1 when x=0 and y=0 when x=alpha. The parameter p controls the curvature of the function.
        to calculate y value given x value
        Valid for 0 <= x <= alpha 
        when 0 < p < 1, it's concave down; when p > 1, it's concave up
        """
        if not (0 <= x <= alpha):
            raise ValueError("x must be in [0, alpha]")
        return 1 - (x / alpha) ** p


    def get_stock_proportion(self, retirement_age = c.retirement_age, life_expectancy = c.life_expectancy, glidepath_type = 'linear', **kwargs):
        '''
        glidepath_type can take the following values:
        - linear: stock proportion decreases linearly from 100% at retirement age to 0% at life expectancy
        - concave: stock proportion decreases following a concave function from 100% at retirement age to 0% at life expectancy. the curvature of the function is determined by the p parameter in kwargs. when 0 < p < 1, it's concave down; when p > 1, it's concave up
        - concave_down: stock proportion decreases following a concave down function from 100% at retirement age to 0% at life expectancy. 
        - concave_up: stock proportion decreases following a concave up function from 100% at retirement age to 0% at life expectancy.

        kwargs can take the following inputs:
        - concave_p: applicable when glidepath_type = 'concave' or 'concave_up' or 'concave_down'. the p parameter for the concave function. 
        '''
        assert glidepath_type in ['linear', 'concave', 'concave_down', 'concave_up']

        l_stock_proportions = [1.0] # list of stock proportions for each year from current age to life expectancy, so length is life_expectancy - current_age

        if glidepath_type == 'linear':
            for k in range(retirement_age, life_expectancy):
                stock_proportion = round(1-1/(life_expectancy - retirement_age)*(k-retirement_age),1)
                l_stock_proportions.append(stock_proportion)
        else:
            p = 1
            if 'concave_p' in kwargs.keys():
                if glidepath_type == 'concave_down':
                    assert kwargs['concave_p'] > 0 and kwargs['concave_p'] < 1
                elif glidepath_type == 'concave_up':
                    assert kwargs['concave_p'] > 1
                p = kwargs['concave_p']
            else:
                if glidepath_type == 'concave_down':
                    p = 0.5
                elif glidepath_type == 'concave_up':
                    p = 2
                else:
                    assert False, "concave_p parameter must be provided for concave glidepath type"
            for k in range(retirement_age, life_expectancy):
                stock_proportion = round(self._y_concave(k - retirement_age, life_expectancy - retirement_age, p),1)
                l_stock_proportions.append(stock_proportion)
            
    
        l_stock_proportions.append(0.0) # at the end of life expectancy, stock proportion is 0
        
        return l_stock_proportions
    
    def _generate_simulated_monthly_returns_from_stock_proportions_list(self, l_stock_proportions, return_method = 'normal', **kwargs):
        '''
        return a list of simulated monthly returns from a list of stock proportions for each year. 
        '''
        assert return_method in ['normal', 'bootstrap']

        l_monthly_returns = []
        
        for i in range(len(l_stock_proportions)):
            proportion_stock = l_stock_proportions[i]
            for _ in range(12):
                if return_method == 'normal':
                    l_monthly_returns.append(s_return.normal(proportion_stock=proportion_stock, kwargs = kwargs))
                if return_method == 'bootstrap':
                    l_monthly_returns.append(s_return.bootstrap(proportion_stock=proportion_stock, **kwargs))
        
        return l_monthly_returns
                
            
    def generate_simulated_monthly_returns(self, retirement_age = c.retirement_age, life_expectancy = c.life_expectancy, glidepath_type = 'linear', return_method = 'normal', **kwargs):
        l_stock_proportions = self.get_stock_proportion(retirement_age, life_expectancy, glidepath_type)
        l_monthly_returns = self._generate_simulated_monthly_returns_from_stock_proportions_list(l_stock_proportions, return_method, **kwargs)

        return l_monthly_returns
    