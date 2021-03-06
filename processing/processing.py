#!/usr/bin/env python
import pika
import time
import psycopg2
import os
import json

# Connect to RabbitMQ
credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'], os.environ['RABBITMQ_DEFAULT_PASS'])
parameters = pika.ConnectionParameters(host='rabbit',
                                       port=5672, credentials=credentials)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print('Processing: RabbitMQ not up yet.')
        time.sleep(2)

print('Processing: Connection to RabbitMQ established')

# Connect to log-analysis channel
channel = connection.channel()
channel.queue_declare(queue='log-analysis')

print('Processing: Channel to RabbitMQ established')

# Connect to PostgreSQL database
conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
cur = conn.cursor()

print('Processing: Connection to DB established')

# main function that reads from RabbitMQ queue and stores it in database
def callback(ch, method, properties, body):
    msg = json.loads(body)
    values = [msg['day'], msg['status'], msg['source']]
    sql = """INSERT INTO weblogs (day, status, source)
             VALUES (to_date(%s, 'YYYY-MM-DD'), %s, %s);"""
    cur.execute(sql, values)
    #print("Row inserted", cur.rowcount)
    conn.commit()


print('Processing: Start Consumer')
#Start consumer
channel.basic_consume(callback,
                      queue='log-analysis',
                      no_ack=True)


print('Processing: Start Consuming')
channel.start_consuming()
