from data.constants import Constants
from utilities.simulators.economics.monthly_investment_return_simulator import ReturnSimulator
from utilities.calculators.historical_monthly_return_calculator import ReturnCalculator

c = Constants()
c_return = ReturnCalculator()

class GoalAssigner:
    def __init__(self):
        pass

    def assign_goal(self, monthly_income, l_stock_proportions, life_expectancy = c.life_expectancy, retirement_age = c.retirement_age, goal_setting = "average", threshold_failure = c.threshold_failure, n_simulations = 1000, current_age =c.current_age, current_capital = c.current_capital, acceptable_failure_rate = 0.05, **kwargs):
        '''
        calculate the minimal account values (among values considered) at each year that would have failure rates below acceptable_failure_rate, in n_simulations simulations, while satisfying the conditions specified in goal_setting

        l_stock_proportions are lifetime portfolio composition with stock proportions, annually adjusted

        goal_setting can take the following values:
        - disaster-averse: assign the goal under the philosophy that the portfolio can sustain itself under the worst disaster, which in this case is defined as having a financial crisis at the year of retirement, where for 5 consecutive years following, investment return would be historical lowest. the rest of the time the portfolio is assumed to have historically normally distributed returns
        - average: assign the goal under the philosophy that the portfolio can sustain itself if each month we have historically normally distributed returns
        '''
        assert len(l_stock_proportions) >= retirement_age - current_age

        l_goal_annual_accounts = []

        # deduce reversely, from end of life expectancy
        l_goal_annual_accounts.append(threshold_failure) # to have at death
        