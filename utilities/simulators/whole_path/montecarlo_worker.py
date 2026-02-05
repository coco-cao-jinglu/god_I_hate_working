from utilities.whole_path import WholePath


def _run_single_simulation(args):
    (

        monthly_net_income,
        retirement_age,
        life_expectancy,
        return_method,
        threshold_failure,
        kwargs
    ) = args

    wp = WholePath()

    l_monthly = wp.whole_path_monthly_account(
        monthly_net_income=monthly_net_income,
        retirement_age=retirement_age,
        life_expectancy=life_expectancy,
        return_method=return_method,
        **kwargs
    )

    final_account = l_monthly[-1]
    failure = min(l_monthly) < threshold_failure

    return final_account, failure
