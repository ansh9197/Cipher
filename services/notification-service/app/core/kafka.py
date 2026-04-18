from confluent_kafka import Consumer, KafkaError
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
