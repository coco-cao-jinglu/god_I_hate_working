# define/assume expenses (in today's money without inflation, i.e. value now, in euro)
import os

class ExpensesAfterRetirement:
    def __init__(self):
        self.monthly_insurance = int(os.environ.get("MONTHLY_INSURANCE", 100))
        self.monthly_food = int(os.environ.get("MONTHLY_FOOD", 500))
        self.monthly_utilities_fuel = int(os.environ.get("MONTHLY_UTILITIES_FUEL", 200))
        self.monthly_vacation = int(os.environ.get("MONTHLY_VACATION", 400))
        self.monthly_farm_upkeep = int(os.environ.get("MONTHLY_FARM_UPKEEP", 500))
        self.annual_emergency_miscellaneous = int(os.environ.get("ANNUAL_EMERGENCY_MISCELLANEOUS", 2000))
        self.retirement_setup_onetime = int(os.environ.get("RETIREMENT_SETUP_ONETIME", 10000))

    def monthly_expenditure(self):
        sum_monthly = self.monthly_food + self.monthly_insurance + self.monthly_utilities_fuel + self.monthly_vacation + self.monthly_farm_upkeep
        return sum_monthly

    def annual_expenditure(self):
        sum_monthly = self.monthly_expenditure()
        sum_annual = sum_monthly * 12 + self.annual_emergency_miscellaneous
        return sum_annual
    
class ExpenditureBeforeRetirement:
    def __init__(self):
        self.monthly_rent_utilities = int(os.environ.get("BR_MONTHLY_RENT_UTILITIES", 1200))
        self.monthly_food = int(os.environ.get("BR_MONTHLY_FOOD", 400))
        self.monthly_activities = int(os.environ.get("BR_MONTHLY_ACTIVITIES", 200))
        self.monthly_vacation = int(os.environ.get("BR_MONTHLY_VACATION", 600))
        self.monthly_insurance = int(os.environ.get("BR_MONTHLY_INSURANCE", 400))
        self.monthly_other_health = int(os.environ.get("BR_MONTHLY_OTHER_HEALTH", 200))
        self.annual_emergency_miscellaneous = int(os.environ.get("BR_ANNUAL_EMERGENCY_MISCELLANEOUS", 3000))

    def monthly_expenditure(self):
        sum_monthly = self.monthly_rent_utilities + self.monthly_food + self.monthly_activities + self.monthly_vacation + self.monthly_insurance + self.monthly_other_health 
        return sum_monthly

    def annual_expenditure(self):
        sum_monthly = self.monthly_expenditure()
        sum_annual = sum_monthly * 12 + self.annual_emergency_miscellaneous
        return sum_annual