from quixstreams import Application
from kraken_api.websocket import KrakenWebsocketAPI
from kraken_api.mock import KrakenMockAPI
from loguru import logger

def main(
        kafka_broker_address: str,
        kafka_topic: str,
        kraken_api: KrakenWebsocketAPI | KrakenMockAPI,
):
    app = Application(
        broker_address=kafka_broker_address,
    )

    topic = app.topic(name=kafka_topic, value_serializer="json")

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # Serialize the trade as bytes
                message = topic.serialize(key=trade.pair, value=trade.to_str())

                # Produce the message to the Kafka topic
                producer.produce(topic=topic.name, key=message.key, value=message.value)

                logger.info(f"Pushed trade to Kafka: {trade}")

if __name__ == "__main__":

    from config import config

    kraken_api = KrakenWebsocketAPI(pairs=config.pairs,
                                    )

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )