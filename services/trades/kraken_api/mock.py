from datetime import datetime
from time import sleep
from typing import List

from .trade import Trade


class KrakenMockAPI:
    def __init__(self, pair: str):
        self.pair = pair

    def get_trades(self) -> List[Trade]:
        """
        Returns a list of mock trades
        """
        mock_trades = [
            Trade(
                pair=self.pair,
                volume=100,
                price=100,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
            Trade(
                pair=self.pair,
                volume=200,
                price=200,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
            Trade(
                pair=self.pair,
                volume=300,
                price=300,
                timestamp=datetime.now(),
                timestamp_ms=int(datetime.now().timestamp() * 1000),
            ),
        ]
        sleep(1)

        return mock_trades
