from kraken_api.mock import KrakenMockAPI
from kraken_api.websocket import KrakenWebsocketAPI
from loguru import logger
from quixstreams import Application


def main(
    kafka_broker_address: str,
    kafka_topic: str,
    kraken_api: KrakenWebsocketAPI | KrakenMockAPI,
):
    # Initialize the Quix Streams application
    # This class handles all the low-level details to connect to Kafka
    app = Application(
        broker_address=kafka_broker_address,
    )

    # This lines defines the Kafka topic that we will produce messages to
    topic = app.topic(name=kafka_topic, value_serializer='json')

    with app.get_producer() as producer:
        while True:
            trades = kraken_api.get_trades()

            for trade in trades:
                # Serialize the trade as bytes
                message = topic.serialize(key=trade.pair, value=trade.to_dict())

                # Produce the message to the Kafka topic
                producer.produce(topic=topic.name, key=message.key, value=message.value)

                logger.info(f'Pushed trade to Kafka: {trade}')


if __name__ == '__main__':
    from config import config

    # Initialize the Kraken API
    kraken_api = KrakenWebsocketAPI(pairs=config.pairs)

    main(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        kraken_api=kraken_api,
    )
