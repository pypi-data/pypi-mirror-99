Swarm-Bus
=========

Client side implementation of an ESB with Amazon SQS.

Simple Usage
------------

::

    # Default transport config
    transport = {
        'prefix': 'dev-%(hostname)s-',
        'priorities': ['low', 'medium', 'high'],
        'polling_interval': 20,                   # Default queue polling interval
        'retention_period': 864000,               # Default queue retention period
        'visibility_timeout': 30,                 # Default queue visibility timeout
        'sleep_time': 0,                          # Default queue sleep time
        'office_hours': True,
        'region': 'eu-west-1'
    }

    bus = SwarmBus('LOGIN', 'PASSWORD', **transport)
    bus.connect()

    queue_config = {
        'visibility_timeout': 5
    }

    # Now we register a new queue
    bus.register_queue('new_queue', **queue_config)

    # Disconnect the bus to finish
    bus.disconnect()


Using as a producer
-------------------

::

    with SwarmBus('LOGIN', 'PASSWORD', **transport) as producer:
        producer.register_queue('new_queue')

        producer.publish(
            'new_queue',
            {'id': 42}
        )

        producer.publish(
            'new_queue',
            {'id': 84},
            priority=1,  # Priority index, correspond to 'medium'
            delay=5      # Delay of the message
        )


Using as a consumer
-------------------

::

    def handle_message(body, message):
        print(body)
        message.delete()

    def error_handler(body, message):
        raise ValueError('Error while processing message')

    with SwarmBus('LOGIN', 'PASSWORD', **transport) as consumer:
        consumer.register_queue('new_queue')

        consumer.consume(
            'new_queue',
            handle_message,
            error_handler
        )
