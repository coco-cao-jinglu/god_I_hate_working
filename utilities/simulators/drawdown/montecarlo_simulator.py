from utilities.retirement_account_drawdown import RetirementAccountCalculator
from data.constants import Constants

c = Constants()

class MonteCarloSimulator:
    def __init__(self):
        self.r = RetirementAccountCalculator()

    def __analyse_account_end(self, l_accounts):
        n = len(l_accounts)
        sorted_accounts = sorted(l_accounts)

        return {
            'mean': sum(sorted_accounts) / n,
            'median': sorted_accounts[n // 2],
            'percentile_10': sorted_accounts[int(0.1 * n)],
            'percentile_90': sorted_accounts[int(0.9 * n)],
        }
        

    def simulate(self, n_simulation = 5000, retirement_age = c.retirement_age, retirement_capital = c.retirement_capital, life_expectancy = c.life_expectancy, return_method = 'constant', threshold_failure = 10000, **kwargs):
    # threshold failure: the number below which it would be counted as a failure if the account dips below it at any point during retirement 

        l_final_account = []
        n_failure = 0

        verbose = kwargs.get('f_montecarlo_verbose', False)


        for i in range(n_simulation):
            l_monthly = self.r.monthly_account(retirement_age = retirement_age, retirement_capital = retirement_capital, life_expectancy = life_expectancy, return_method = return_method, **kwargs)
            l_final_account.append(l_monthly[-1])
            if min(l_monthly) < threshold_failure:
                n_failure += 1
            if verbose:
                if i % 10 == 0:
                    print(f'Simulation {i+1}: final account: {l_monthly[-1]}, failure: {min(l_monthly) < threshold_failure}')

        return {'final_account_analysis': self.__analyse_account_end(l_final_account), 'failure_rate': n_failure/n_simulation}
