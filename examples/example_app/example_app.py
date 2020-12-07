#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import pika
import psycopg2

#redis 
from redis.sentinel import Sentinel
sentinel = Sentinel([('redis-sentinel', '26379')], socket_timeout=0.1)
# Антон, писать всё надо в мастер
master = sentinel.master_for('mymaster', socket_timeout=0.1,password='redis')
master.set('foo', 'bar')

# Даниил, всё чтение надо делать из слейвов
slave = sentinel.slave_for('mymaster', socket_timeout=0.1, password='redis')
slave.get('foo')


#rabbit
credentials = pika.credentials.PlainCredentials('rabbit', 'rabbit', erase_on_connect=False)
# что-то мне блокирующее соединение не нравится, Антон изучи. Не хотелось бы, чтобы очередь к чертям блочилась
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbit', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
connection.close()


#postgres
# чтобы сварм не создавал истерично новые контейнеры после выхода
from time import sleep
sleep(30)