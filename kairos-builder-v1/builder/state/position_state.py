class PositionState:

    def __init__(self):

        # 🔥 현재 보유 포지션 저장
        self.positions = {}

    # -----------------------------
    # CHECK EXISTING POSITION
    # -----------------------------
    def has_position(self, ticker):

        return ticker in self.positions

    # -----------------------------
    # ADD POSITION
    # -----------------------------
    def add_position(self, ticker, qty, price):

        self.positions[ticker] = {
            "qty": qty,
            "entry_price": price
        }

    # -----------------------------
    # UPDATE POSITION
    # -----------------------------
    def update_position(self, ticker, qty, price):

        if ticker in self.positions:

            self.positions[ticker]["qty"] += qty
            self.positions[ticker]["entry_price"] = price

    # -----------------------------
    # GET POSITION
    # -----------------------------
    def get_position(self, ticker):

        return self.positions.get(ticker)

    # -----------------------------
    # ALL POSITIONS
    # -----------------------------
    def get_all(self):

        return self.positions