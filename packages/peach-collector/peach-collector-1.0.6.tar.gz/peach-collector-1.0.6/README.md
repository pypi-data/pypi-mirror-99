# peach-collector

Peach Collector client implementation in Python 3.8


# PeachCollector

Simplest way to send events. Usage:

    collector = PeachCollector("a-site-key", "an-app-id")
    collector.add_event({"foo": 666})
    collector.add_event({"bar": 777})
    await collector.send_events()


# PeachCollectorQueue

Pushes events on to a Redis queue which is drained at regular intervals.  Usage:

    # Client
    q = PeachCollectorQueue("redis://localhost")
    q.push_event({"foo": 66})
    q.push_event({"bar": 777})

    # Scheduled Worker
    collector = PeachCollector("a-site-key", "an-app-id")
    q = PeachCollectorQueue("redis://localhost", collector)
    q.drain()
