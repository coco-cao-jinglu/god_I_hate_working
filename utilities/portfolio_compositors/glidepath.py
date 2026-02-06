from data.constants import Constants
from utilities.simulators.economics.monthly_investment_return_simulator import ReturnSimulator


c = Constants()
s_return = ReturnSimulator()

class GlidePathCompositor:
    # compose the after retirement glidepath
    def __init__(self):
        pass    

    def get_stock_proportion(self, retirement_age = c.retirement_age, life_expectancy = c.life_expectancy, glidepath_type = 'linear'):
        '''
        glidepath_type assumed to be linear for now
        '''
        assert glidepath_type in ['linear']

        l_stock_proportions = [1.0] # list of stock proportions for each year from current age to life expectancy, so length is life_expectancy - current_age

        if glidepath_type == 'linear':
            for k in range(retirement_age, life_expectancy):
                stock_proportion = round(1-1/(life_expectancy - retirement_age)*(k-retirement_age),1)
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
    