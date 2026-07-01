class RiskManager:

    def __init__(self):

        self.daily_pnl = 0
        self.max_daily_loss = -0.05   # -5%
        self.max_drawdown = -0.10     # -10%

        self.is_trading_enabled = True

    # -----------------------------
    # UPDATE PnL
    # -----------------------------
    def update_pnl(self, pnl):

        self.daily_pnl += pnl

        if self.daily_pnl <= self.max_daily_loss:
            self.is_trading_enabled = False

    # -----------------------------
    # CHECK TRADE ALLOWED
    # -----------------------------
    def can_trade(self):

        return self.is_trading_enabled

    # -----------------------------
    # FORCE STOP
    # -----------------------------
    def stop(self):

        self.is_trading_enabled = False