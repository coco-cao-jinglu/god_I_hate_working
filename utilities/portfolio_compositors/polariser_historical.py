from utilities.portfolio_compositors.moderator_historical import ModeratorHistorical

class PolariserHistorical:
    def __init__(self, **kwargs):
        self.moderator = ModeratorHistorical(**kwargs)

    def start(self, **kwargs):
        return self.moderator.start(**kwargs)

    def generate(self, l_account_history, l_annual_stock_proportion, l_monthly_return, **kwargs):
        sensitivity = -0.2

        if 'sensitivity' in kwargs.keys():
            assert type(kwargs['sensitivity']) == float and kwargs['sensitivity'] <= -0.1 and kwargs['sensitivity'] >= -1.0 and sensitivity % 0.1 == 0
            sensitivity = kwargs['sensitivity']

        return self.moderator.generate(l_account_history, l_annual_stock_proportion, l_monthly_return, **kwargs)
        