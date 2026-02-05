from utilities.retirement_account_drawdown import RetirementAccountCalculator


def _run_single_simulation(args):
    (
        retirement_age,
        retirement_capital,
        life_expectancy,
        return_method,
        threshold_failure,
        kwargs
    ) = args

    r = RetirementAccountCalculator()

    l_monthly = r.monthly_account(
        retirement_age=retirement_age,
        retirement_capital=retirement_capital,
        life_expectancy=life_expectancy,
        return_method=return_method,
        **kwargs
    )

    final_account = l_monthly[-1]
    failure = min(l_monthly) < threshold_failure

    return final_account, failure
