import pandas as pd
from odin.strategy import AbstractStrategy
from odin.strategy.templates import BuyAndHoldStrategy


class BuyAndHoldSpyderStrategy(BuyAndHoldStrategy):
    def buy_indicator(self, feats):
        return feats.name in ("SPY", )


class RebalanceETFStrategy(AbstractStrategy):
    def __init__(self, portfolio, direction):
        """Initialize parameters of the buy and hold strategy object."""
        super(RebalanceETFStrategy, self).__init__(portfolio)
        self.direction = direction

    def direction_indicator(self, feats):
        """Implementation of abstract base class method."""
        return self.direction

    def buy_indicator(self, feats):
        """Implementation of abstract base class method."""
        return True

    def sell_indicator(self, feats):
        """Implementation of abstract base class method."""
        return False

    def exit_indicator(self, feats):
        """Implementation of abstract base class method."""
        symbol = feats.name
        pos = self.portfolio.portfolio_handler.filled_positions[symbol]
        date = self.portfolio.data_handler.current_date
        return pos.compute_holding_period(date).days > 63

    def generate_features(self):
        """Implementation of abstract base class method."""
        symbols = self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index
        return pd.DataFrame(index=symbols)

    def generate_priority(self, feats):
        """Implementation of abstract base class method."""
        return self.portfolio.data_handler.bars.ix[
            "adj_price_open", -1, :
        ].dropna().index