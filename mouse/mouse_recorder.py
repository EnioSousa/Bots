from typing import Callable
from pynput import mouse
import logging

from inputDevice.input_event import InputPayload
from inputDevice.input_source import InputSource
from mouse.mouse_event import MouseEvent

class MouseRecorder(InputSource):
    """
    Concrete InputSource implementation that captures mouse events via
    pynput and forwards them to a registered callback as MouseEvent payloads.

    
    This class is not concurently safe, and start/stop methods should be handled carefully
    """

    def __init__(self):
        """
        Initialize the MouseRecorder.
        """
        self.__callback: Callable[[InputPayload], None] = None
        self.__listener: mouse.Listener = None
        self.__logger = logging.getLogger("mouse.MouseRecorder")

    def register_callback(self, callback: Callable[[InputPayload], None]) -> None:
        """
        Register Event callback
        """
        self.__callback = callback
        self.__logger.info("Callback registered")

    def start(self):
        """
        Start the mouse listener if it is not already running.
        """
        if not self.__listener:
            self.__listener = mouse.Listener(on_move=self._on_move, on_click=self._on_click, on_scroll=self._on_scroll)

        self.__listener.start()
        self.__logger.info("Listener started")

    def stop(self):
        """
        Stop the mouse listener if it is currently running.
        """
        if self.__listener:
            self.__listener.stop()

        self.__listener = None
        self.__logger.info("Listener stopped")

    def __on_event(self, event: MouseEvent):
        """
        Handle Generic Events
        """
        if self.__callback is not None:
            self.__callback(event)
        
        self.__logger.debug(event)

    def _on_move(self, x, y):
        """
        Handle mouse movement events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
        """
        self.__on_event(MouseEvent(MouseEvent.EventType.MOVE, x, y))

    def _on_click(self, x, y, button, pressed):
        """
        Handle mouse click events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            button (Button): The button that was pressed or released.
            pressed (bool): True if the button was pressed, False if released.
        """
        if button == mouse.Button.left:
            event_type = MouseEvent.EventType.PRESSED_LEFT if pressed else MouseEvent.EventType.RELEASED_LEFT
        elif button == mouse.Button.right:
            event_type = MouseEvent.EventType.PRESSED_RIGHT if pressed else MouseEvent.EventType.RELEASED_RIGHT
        else:
            return

        self.__on_event(MouseEvent(event_type, x, y))

    def _on_scroll(self, x, y, dx, dy):
        """
        Handle mouse scroll events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            dx (int): The amount of horizontal scroll.
            dy (int): The amount of vertical scroll.
        """
        self.__logger.debug("Scroll event ignored")
