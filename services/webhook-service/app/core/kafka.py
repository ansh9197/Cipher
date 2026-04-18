from confluent_kafka import Producer
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

_producer = None

def get_producer() -> Producer:
    global _producer
    if _producer is None:
        _producer = Producer({
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "client.id":         "webhook-service",
            "acks":              "all",
            "retries":           3,
        })
    return _producer

def delivery_report(err, msg):
    if err:
        logger.error(f"Kafka delivery failed: {err}")
    else:
        logger.info(f"Kafka message delivered to {msg.topic()} [{msg.partition()}]")

def publish_event(topic: str, key: str, payload: dict) -> bool:
    try:
        producer = get_producer()
        producer.produce(
            topic=topic,
            key=key.encode("utf-8"),
            value=json.dumps(payload).encode("utf-8"),
            callback=delivery_report,
        )
        producer.flush(timeout=10)
        return True
    except Exception as e:
        logger.error(f"Failed to publish to {topic}: {e}")
        return False
