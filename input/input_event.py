from enum import Enum
from abc import ABC, abstractmethod

from utils.atomic.atomic import AtomicCounter

class InputPayload(ABC):
    """
    Abstracts interface for any device-specific event payload (e.g MouseEvent, KeyboardEvent).
    """

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplemented
    
class InputEvent:
    """
    Wraps a device-specific InputPayload with a source tag, allowing any number of input types to
    be recorded and replayed on a single shared timeline

    Attributes:
        source (InputEvent.Source): Which device produced this event.
        payload (InputPayload): The underlying device-specific event.
        timestamp (int): Milliseconds elapsed since the start of recording,
                         shared across all InputEvents regardless of source.
        id (int): Unique, monotonically increasing identifier for this event.
    """

    class Source(Enum):
        MOUSE       = 0
        KEYBOARD    = 1

    _id_counter: AtomicCounter = AtomicCounter()

    def __init__(self, source: Source, payload: InputPayload, timestamp: int):
        self.source: InputEvent.Source = source
        self.payload: InputPayload = payload
        self.timestamp: int = timestamp
        self.id: int = InputEvent._id_counter.increment()

    def __repr__(self) -> str:
        return (f"InputEvent(ID={self.id}, Timestamp={self.timestamp}, "source={self.source.name}, payload={self.payload})")
    

