# tests/test_message_bus.py
from core.message_bus import MessageBus

def test_subscribe_publish():
    bus = MessageBus()
    results = []
    def cb(msg):
        results.append(msg.payload.get("x"))
    bus.subscribe("test.topic", cb)
    bus.publish("test.topic", sender="unit", payload={"x": 42})
    assert results == [42]
