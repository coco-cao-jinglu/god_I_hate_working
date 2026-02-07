from utilities.portfolio_compositors.moderator import Moderator

class Polariser:
    def __init__(self, **kwargs):
        self.moderator = Moderator(**kwargs)

    def start(self, **kwargs):
        return self.moderator.start(**kwargs)

    def generate(self, l_account_history, l_annual_stock_proportion, **kwargs):
        sensitivity = -0.2

        if 'sensitivity' in kwargs.keys():
            assert type(kwargs['sensitivity']) == float and kwargs['sensitivity'] <= -0.1 and kwargs['sensitivity'] >= -1.0 and sensitivity % 0.1 == 0
            sensitivity = kwargs['sensitivity']

        return self.moderator.generate(l_account_history, l_annual_stock_proportion, **kwargs)
        