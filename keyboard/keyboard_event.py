from datetime import timedelta
from pynput import keyboard
from enum import Enum
from utils.atomic.atomic import AtomicCounter

import logging

class KeyboardEvent:
    """
    Represents a keyboard event with an associated type, timestamp and Keys

    This class captures the type of keyboard event (e.g Key 'h' pressed or released)
    along with the time the event occured

    Attributes:
        event_type  (KeyboardEvent): The type of the keyboard event (PRESSED, RELEASED)
        event_value (int): The value of the key pressed
        timestamp   (datetime): The timestamp when the event was created
    """

    class EventType(Enum):
        """
        Enum describing a keyboard event type

        Attributes:
            PRESSED: Indicates a certain key was pressed
            RELEASE: Indicates a certain key was released
        """
        PRESSED = 0
        RELEASED = 1

    _id_counter: AtomicCounter = AtomicCounter()

    def __init__(self, event_type: EventType, key: keyboard.Key, elapsed_time: timedelta):
        self.event_type: KeyboardEvent.EventType = event_type
        self.timestamp: int = int(elapsed_time.total_seconds() * 1_000)
        self.key: str = self.__serialize_key(key)
        self.id: int = KeyboardEvent._id_counter.increment()

    def __serialize_key(self, key: keyboard.Key):
        if isinstance(key, keyboard.KeyCode):
            return f"char:{key.char}"
        else:
            return f"name:{key.name}"

    def get_key_value(self) -> keyboard.Key:
        kind, value = self.key.split(':', 1)
        if kind == "char":
            return keyboard.KeyCode.from_char(value)
        else:
            try:
                return getattr(keyboard.Key, value)
            except AttributeError:
                raise ValueError(f"Unkown key name '{value}'")

    def __repr__(self) -> str:
        return (f"KeyboardEvent(ID={self.id}, Timestamp={self.timestamp}, event_type={self.event_type.name}, KeyValue={self.key})")
        