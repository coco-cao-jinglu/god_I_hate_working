from data.constants import Constants
from utilities.simulators.whole_path.paralle_worker_simulator import ParallelWorkerSimulator
import pandas as pd

c = Constants()
pws = ParallelWorkerSimulator()

class RetirementAgeCalculator:
    '''
    given info about income and expenditures, considering all available strategies, calculate at which age I can possibly retire
    '''
    def __init__(self):
        pass 

    def _run_for_method(self,monthly_net_income, strategy,retirement_age,
        n_simulation=5000,
        return_method='constant',
        threshold_failure=c.threshold_failure,
        **kwargs):
        assert strategy[0] in ['constant', 'glidepath', 'annual goal-fitter']
        if strategy[0] == 'constant':
            assert type(strategy[1]) == int or type(strategy[1]) == float
            stock_proportion = strategy[1]
            return pws.simulate(monthly_net_income=monthly_net_income, retirement_age=retirement_age,n_simulation=n_simulation, return_method=return_method, proportion_stock=stock_proportion, threshold_failure=threshold_failure, **kwargs)
        elif strategy[0] == 'glidepath':
            assert strategy[1] in ['linear', 'concave', 'concave_up', 'concave_down']
            glidepath_type = strategy[1]
            return pws.simulate(monthly_net_income=monthly_net_income, retirement_age=retirement_age,n_simulation=n_simulation, return_method=return_method, threshold_failure=threshold_failure, f_portfolio_composition = True, portfolio_method = 'glidepath', glidepath_type = glidepath_type, **kwargs)
        

    def calculate(self, monthly_net_income, l_available_strategies, max_tolerated_failure_rate,
        n_simulation=5000,
        current_age = c.current_age,
        life_expectancy=c.life_expectancy,
        return_method='constant',
        threshold_failure=c.threshold_failure,
        **kwargs):
        '''
        max_tolerated_failure_rate: can retire as soon as there is at least one strategy that gives a failure rate below max_tolerated_failure_rate
        '''


        # first, calculate if under the current combination, I would be able to retire at all
        def test_extreme_case():
            dic_extreme_case_results = {}
            retirement_age = life_expectancy - 1
            for strategy in l_available_strategies:
                res = self._run_for_method(monthly_net_income, strategy,
            n_simulation=n_simulation,
            retirement_age=retirement_age,
            return_method=return_method,
            threshold_failure=threshold_failure,
            **kwargs)
                if res['failure_rate'] < max_tolerated_failure_rate:
                    print("Congrats, you can retire within your lifetime. Calculating earliest retirement age now...")
                    return True
                else:
                    dic_extreme_case_results[strategy] = res['failure_rate']
            print("You cannot retire. Earn more or tolerate higher failure rates.")
            print("Even if you work until death, your lowest failure rate is still " + str(min(dic_extreme_case_results.values())))
            return False

        if test_extreme_case() is True:
            age = current_age + 1

            while age < life_expectancy - 1:
                dic_all_strategy_res = {}
                for strategy in l_available_strategies:
                    res = self._run_for_method(monthly_net_income, strategy,
                n_simulation=n_simulation,
                retirement_age=age,
                return_method=return_method,
                threshold_failure=threshold_failure,
                **kwargs)
                    dic_all_strategy_res[strategy] = res
                min_failure_fate = min([dic_all_strategy_res[method]['failure_rate'] for method in l_available_strategies])
                if min_failure_fate > max_tolerated_failure_rate:
                    print("Age " + str(age) + " fails. At this age, your lowest failure rate is " + str(min_failure_fate))
                    age += 1
                else:
                    print("Success! At age " + str(age) + ", you will be able to retire! Your lowest failure rate is " + str(min_failure_fate))
                    print("Printing results for all eligible portfolio strategies:")
                    df_portfolio_composition_comparison = pd.DataFrame({
    'method': l_available_strategies,
    'failure_rate': [dic_all_strategy_res[method]['failure_rate'] for method in l_available_strategies],
    'portfolio_median': [dic_all_strategy_res[method]['final_account_analysis']['median'] for method in l_available_strategies],
    'portfolio_10th_percentile':  [dic_all_strategy_res[method]['final_account_analysis']['percentile_10'] for method in l_available_strategies],
    'portfolio_90th_percentile': [dic_all_strategy_res[method]['final_account_analysis']['percentile_90'] for method in l_available_strategies]
})
                    df_eligible_portfolios = df_portfolio_composition_comparison[df_portfolio_composition_comparison['failure_rate'] <= max_tolerated_failure_rate].sort_values(by = 'failure_rate', ascending = True)
                    print(df_eligible_portfolios)
                    return df_eligible_portfolios
        

        
        