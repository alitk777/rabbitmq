#!/usr/bin/env python
import json

import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'),
)
channel = connection.channel()

channel.queue_declare(queue='hello')

data = {
    "action": "Create",
    "attribute": "batch",
    "details": "Phase",
    "oldValue": "0",
    "newValue": "",
}
message = json.dumps(data)

channel.basic_publish(exchange='', routing_key='hello', body=message)

print(" [x] Sent data to RabbitMQ")

connection.close()

