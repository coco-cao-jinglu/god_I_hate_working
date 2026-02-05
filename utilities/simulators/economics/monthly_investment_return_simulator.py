from utilities.calculators.historical_monthly_return_calculator import ReturnCalculator

import numpy as np

r = ReturnCalculator()

class ReturnSimulator:
    def __init__(self):
        self.normal_generation = {}

    def constant(self, return_rate = 0.005):
        # baseline assumption gives annual investment return rate of 0.06
        return return_rate
    
    def normal(self, proportion_stock=1, **kwargs):
        if proportion_stock not in self.normal_generation.keys():
            mean, std = r.normal_distribution_variables(proportion_stock=proportion_stock, kwargs=kwargs)
            self.normal_generation[proportion_stock] = np.random.normal(mean, std, 100000)
        return np.random.choice(self.normal_generation[proportion_stock])
    
    def bootstrap(self, proportion_stock=1, **kwargs):
        l_all_returns = r.list_monthly_portfolio_return(proportion_stock=proportion_stock, kwargs=kwargs)
        return np.random.choice(l_all_returns)
    
