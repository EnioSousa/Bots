from mouse.mouse_event import MouseEvent
from thread.thread import Runnable
from ser.ser import Serialize

from pynput import mouse
from pynput.mouse import Button
from threading import Lock
from datetime import datetime

import logging

class MouseRecorder(Runnable):
    """
    A class to record mouse events and serialize them.

    Inherits from Runnable to manage threading behavior.
    """

    def __init__(self, ser: Serialize = None):
        """
        Initialize the MouseRecorder.

        Args:
            ser (Serialize): An optional Serialize instance for handling serialization.
        """
        super().__init__()
        self.__listener: mouse.Listener = None

        self.__eventLock: Lock = Lock()
        self.__events: list[MouseEvent] = []
        self.__record_start: datetime = datetime.now()

        self.__ser: Serialize = Serialize("mouse_events.pkl") if ser is None else ser

        self.__logger = logging.getLogger("mouse.MouseRecorder")

    def __start_listener(self):
        """
        Start the mouse listener if it is not already running.
        """
        if not self.__listener:
            self.__listener = mouse.Listener(on_move=self.on_move, on_click=self.on_click, on_scroll=self.on_scroll)

        self.__listener.start()
        self.__logger.info("Listener started")

    def __stop_listener(self):
        """
        Stop the mouse listener if it is currently running.
        """
        if self.__listener:
            self.__listener.stop()

        self.__listener = None
        self.__logger.info("Listener stopped")

    def _run(self):
        """
        The main loop for the mouse recorder. This runs continuously while the state is RUNNING.
        """
        self.__logger.info("Mouse Recorder started")
        self.__ser.start()
        self.__start_listener()

        self.__record_start = datetime.now()

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                self._condition.wait(timeout=60)

                with self.__eventLock:
                    self.__ser.schedule_serialization(self.__events)
                    self.__events.clear()

        self.__stop_listener()
        self.__ser.stop()

        with self.__eventLock:
            self.__events = []

        self.__logger.info("Mouse Recorder stopped")

    def get_events(self) -> list[MouseEvent]:
        """
        Get the list of recorded mouse events.

        Returns:
            list[MouseEvent]: The list of recorded mouse events.
        """
        with self.__eventLock:
            return self.__events

    def on_move(self, x, y):
        """
        Handle mouse movement events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
        """
        with self.__eventLock:
            event = MouseEvent(MouseEvent.EventType.MOVE, x, y, datetime.now() - self.__record_start)
            self.__events.append(event)

        self.__logger.debug(event)

    def on_click(self, x, y, button, pressed):
        """
        Handle mouse click events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            button (Button): The button that was pressed or released.
            pressed (bool): True if the button was pressed, False if released.
        """
        with self.__eventLock:
            if button == Button.left:
                event_type = MouseEvent.EventType.PRESSED_LEFT if pressed else MouseEvent.EventType.RELEASED_LEFT
            elif button == Button.right:
                event_type = MouseEvent.EventType.PRESSED_RIGHT if pressed else MouseEvent.EventType.RELEASED_RIGHT
            else:
                return

            event = MouseEvent(event_type, x, y, datetime.now() - self.__record_start)
            self.__events.append(event)

        self.__logger.debug(event)

    def on_scroll(self, x, y, dx, dy):
        """
        Handle mouse scroll events.

        Args:
            x (int): The x-coordinate of the mouse pointer.
            y (int): The y-coordinate of the mouse pointer.
            dx (int): The amount of horizontal scroll.
            dy (int): The amount of vertical scroll.
        """
        self.__logger.debug("Scroll event ignored")
