import json
from typing import List

from loguru import logger
from websocket import create_connection

from .base import TradesAPI
from .trade import Trade


class KrakenWebsocketAPI(TradesAPI):
    URL = 'wss://ws.kraken.com/v2'

    def __init__(self, pairs: List[str]):
        self.pairs = pairs

        self._ws_client = create_connection(self.URL)

        self._subscribe()

    def get_trades(self) -> List[Trade]:
        """
        Fetches the trades from the Kraken Websocket APIs and returns them as a list of Trade objects

        Returns:
            List[Trade]: A list of Trade objects.
        """
        data = self._ws_client.recv()

        # If the message contains "heartbeat" string, then skip it.
        if 'heartbeat' in data:
            logger.info('Heartbeat received')
            return []

        # Attempt to decode the message as JSON
        try:
            data = json.loads(data)
        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON: {e}')
            return []

        # Obtain the data from the "data" key in the dictionary
        try:
            trades_data = data['data']
        except KeyError:
            logger.error("No 'data' key found in the message {e}")
            return []

        # Return the trades from the data
        return [
            Trade.from_kraken_api_response(
                pair=trade['symbol'],
                price=trade['price'],
                volume=trade['qty'],
                timestamp=trade['timestamp'],
            )
            for trade in trades_data
        ]

    def _subscribe(self):
        """
        Subscribes to the trade channel for the given pair
        """
        self._ws_client.send(
            json.dumps(
                {
                    'method': 'subscribe',
                    'params': {
                        'channel': 'trade',
                        'symbol': self.pairs,
                        'snapshot': True,
                    },
                }
            )
        )

        # Dump the first message of each pairs because they are only subscription confirmations
        for _ in self.pairs:
            self._ws_client.recv()
