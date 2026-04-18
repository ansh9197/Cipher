from confluent_kafka import Consumer, Producer, KafkaError
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)


def get_consumer(group_id: str) -> Consumer:
    return Consumer({
        "bootstrap.servers":  settings.kafka_bootstrap_servers,
        "group.id":           group_id,
        "auto.offset.reset":  "earliest",
        "enable.auto.commit": False,
    })


def get_producer() -> Producer:
    return Producer({
        "bootstrap.servers": settings.kafka_bootstrap_servers,
        "client.id":         "analysis-service",
        "acks":              "all",
    })


def publish_event(topic: str, key: str, payload: dict) -> bool:
    try:
        producer = get_producer()
        producer.produce(
            topic=topic,
            key=key.encode("utf-8"),
            value=json.dumps(payload).encode("utf-8"),
        )
        producer.flush(timeout=10)
        return True
    except Exception as e:
        logger.error(f"Kafka publish error: {e}")
        return False
