from concurrent.futures import ProcessPoolExecutor
import os

from utilities.simulators.drawdown.montecarlo_worker import _run_single_simulation
from data.constants import Constants

c = Constants()

class ParallelWorkerSimulator:
    def __init__(self):
        pass

    def __analyse_account_end(self, l_accounts):
        n = len(l_accounts)
        sorted_accounts = sorted(l_accounts)

        return {
            'mean': sum(sorted_accounts) / n,
            'median': sorted_accounts[n // 2],
            'percentile_10': sorted_accounts[int(0.1 * n)],
            'percentile_90': sorted_accounts[int(0.9 * n)],
        }

    def simulate(
        self,
        n_simulation=5000,
        retirement_age=c.retirement_age,
        retirement_capital=c.retirement_capital,
        life_expectancy=c.life_expectancy,
        return_method='constant',
        threshold_failure=c.threshold_failure,
        **kwargs
    ):
        args = [
            (
                retirement_age,
                retirement_capital,
                life_expectancy,
                return_method,
                threshold_failure,
                kwargs
            )
            for _ in range(n_simulation)
        ]

        l_final_account = []
        n_failure = 0

        # Use all cores by default
        with ProcessPoolExecutor(max_workers=os.cpu_count()-1) as executor:
            for final_account, failure in executor.map(_run_single_simulation, args):
                l_final_account.append(final_account)
                n_failure += failure

        return {
            'final_account_analysis': self.__analyse_account_end(l_final_account),
            'failure_rate': n_failure / n_simulation
        }
