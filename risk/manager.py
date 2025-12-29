class RiskManager:

    def __init__(self, max_qty=500, daily_loss_limit=-0.05):
        self.max_qty = int(max_qty)
        self.daily_loss_limit = daily_loss_limit
        self.daily_pnl = 0

    def allow(self, signal, open_qty):

        # -------- ensure numeric qty --------
        try:
            qty = int(signal.qty)
        except Exception:
            qty = 0

        try:
            open_qty = int(open_qty)
        except Exception:
            open_qty = 0

        # -------- position size rule --------
        if open_qty + qty > self.max_qty:
            return None

        # -------- daily stop rule --------
        if self.daily_pnl < self.daily_loss_limit:
            return None

        return signal
