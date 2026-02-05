from utilities.calculators.historical_annual_inflation_calculator import InflationCalculator
import numpy as np 

i = InflationCalculator()

class InflationSimulator:
    def __init__(self):
        self.normal_generation = {}

    def constant(self, inflation_rate = 0.03):
        return inflation_rate
    
    def normal(self, country = 'mixed',**kwargs):
        if country not in self.normal_generation.keys():
            mean, std = i.normal_distribution_variables(country = country, kwargs = kwargs)
            self.normal_generation[country] = np.random.normal(mean, std, 100000)
        return np.random.choice(self.normal_generation[country])
    
    def bootstrap(self, country = 'mixed', **kwargs):
        l_all_inflations = i.list_monthly_inflation(country = country, kwargs = kwargs)
        return np.random.choice(l_all_inflations)
    
        
    