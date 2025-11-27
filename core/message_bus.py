# core/message_bus.py
"""Simple in-memory pub/sub message bus for agent-to-agent communication (A2A style)."""

from typing import Callable, Dict, List, Any
from threading import Lock
import uuid
import time

class Message:
    def __init__(self, sender: str, topic: str, payload: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.sender = sender
        self.topic = topic
        self.payload = payload
        self.timestamp = int(time.time())

    def to_dict(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "topic": self.topic,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }

class MessageBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[Message], None]]] = {}
        self._lock = Lock()

    def subscribe(self, topic: str, callback: Callable[[Message], None]) -> None:
        """Subscribe a callback to a topic (topic exact match)."""
        with self._lock:
            if topic not in self._subs:
                self._subs[topic] = []
            self._subs[topic].append(callback)

    def publish(self, topic: str, sender: str, payload: Dict[str, Any]) -> Message:
        """Publish a message to a topic; synchronous delivery to subscribers."""
        msg = Message(sender=sender, topic=topic, payload=payload)
        handlers = []
        with self._lock:
            handlers = list(self._subs.get(topic, []))
        for cb in handlers:
            try:
                cb(msg)
            except Exception:
                # Do not let subscriber exceptions break publishing
                pass
        return msg

    def list_subscriptions(self) -> Dict[str, int]:
        with self._lock:
            return {k: len(v) for k, v in self._subs.items()}
