from datetime import datetime
from enum import Enum

class MouseEvent:
    """
    Represents a mouse event with an associated type and timestamp.

    This class captures the type of mouse event (e.g., movement, button press/release) 
    along with the exact time the event occurred.

    Attributes:
        event_type (MouseEvent.EventType): The type of the mouse event (MOVE, PRESSED, RELEASED).
        timestamp (datetime): The timestamp when the event was created.
    """

    class EventType(Enum):
        """
        Enum describing an mouse event type

        Attributes:
            MOVE (int): Indicates mouse movement.
            PRESSED_LEFT (int): Indicates the left mouse button was pressed.
            PRESSED_RIGHT (int): Indicates the right mouse button was pressed.
            RELEASED_LEFT (int): Indicates the left mouse button was released.
            RELEASED_RIGHT (int): Indicates the right mouse button was released.
        """
        MOVE = 0
        PRESSED_LEFT = 1
        PRESSED_RIGHT = 2
        RELEASED_LEFT = 3
        RELEASED_RIGHT = 4

    def __init__(self, event_type: EventType, timestamp: datetime = None):
        self.event_type = event_type
        self.timestamp = timestamp if timestamp else datetime.now()

    def __repr__(self) -> str:
        return (f"MouseEvent(Timestamp={self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}, event_type={self.event_type.name})")
