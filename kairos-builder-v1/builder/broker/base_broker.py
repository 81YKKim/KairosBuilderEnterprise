class BaseBroker:

    def buy(self, ticker, amount):
        raise NotImplementedError

    def sell(self, ticker, amount):
        raise NotImplementedError