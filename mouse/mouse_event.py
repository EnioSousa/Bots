from datetime import timedelta
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

    _id_counter = 0

    def __init__(self, event_type: EventType, x: int, y: int, elapsed_time: timedelta):
        self.event_type: MouseEvent.EventType = event_type
        self.timestamp: int = int(elapsed_time.total_seconds() * 1_000)
        self.x: int = x
        self.y: int = y
        self.id: int = MouseEvent._id_counter
        MouseEvent._id_counter += 1


    def __repr__(self) -> str:
        return (f"MouseEvent(ID={self.id}, Timestamp={self.timestamp}, event_type={self.event_type.name}, x={self.x}, y={self.y})")
