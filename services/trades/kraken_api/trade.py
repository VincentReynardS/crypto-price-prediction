from datetime import datetime

from pydantic import BaseModel


class Trade(BaseModel):
    """
    A trade from the Kraken API
    """

    pair: str
    volume: float
    price: float
    timestamp: str
    timestamp_ms: int

    @classmethod
    def from_kraken_api_response(
        cls, pair: str, price: float, volume: float, timestamp: datetime
    ) -> 'Trade':
        return cls(
            pair=pair,
            price=price,
            volume=volume,
            timestamp=timestamp,
            timestamp_ms=cls._datestr2milliseconds(timestamp),
        )

    @staticmethod
    def _datestr2milliseconds(datestr: str) -> int:
        return int(
            datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp() * 1000
        )

    def to_str(self) -> str:
        # Pydantic method to convert the model into a dict
        return self.model_dump_json()

    def to_dict(self) -> str:
        return self.model_dump()
