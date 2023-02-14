#!/usr/bin/python3

import random
import uuid
from time import sleep

from confluent_kafka import Producer


def delivery_callback(err, msg):
    if err:
        print("ERROR: Message failed delivery: {}".format(err))
    else:
        print(
            "Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(),
                key=msg.key().decode("utf-8"),
                value=msg.value().decode("utf-8"),
            )
        )


def push_fake_data() -> None:

    config = {
        "bootstrap.servers": "localhost:9092",
    }

    producer = Producer(**config)

    topic = "watch"
    users = [uuid.uuid4() for _ in range(1000)]
    films = [uuid.uuid4() for _ in range(1000)]
    timestamps = [str(i) for i in range(18000)]

    producer.flush()

    for _ in range(100):
        for _ in range(10000):
            key = f"{random.choice(users)}+{random.choice(films)}"
            value = random.choice(timestamps)
            producer.produce(
                topic,
                value.encode("utf-8"),
                key.encode("utf-8"),
                callback=delivery_callback,
            )

        producer.poll(10000)
        producer.flush()


if __name__ == "__main__":
    push_fake_data()
