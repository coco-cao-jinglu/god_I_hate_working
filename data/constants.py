import os


class Constants:
    def __init__(self):
        self.life_expectancy = int(os.environ.get("LIFE_EXPECTANCY"))
        self.current_age = int(os.environ.get("CURRENT_AGE"))
        self.retirement_age = int(os.environ.get("RETIREMENT_AGE"))

        self.retirement_capital = int(os.environ.get("RETIREMENT_CAPITAL")) # capital you have at the moment of retirement, value then (at the year of retirement)
        self.current_capital = int(os.environ.get("CURRENT_CAPITAL"))
        self.average_annual_salary_increment = float(os.environ.get("AVERAGE_ANNUAL_SALARY_INCREMENT")) #since we should retire before my professional earning potential starts to dwindle

        self.threshold_failure = float(os.environ.get("THRESHOLD_FAILURE")) # the threshold under which the simulation would be considered a failure if the account value falls under any time during the period of consideration