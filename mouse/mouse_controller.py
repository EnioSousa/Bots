from mouse.mouse_event import MouseEvent
from thread.thread import Runnable
from ser.ser import Serialize
from datetime import datetime

from pynput.mouse import Button, Controller
import threading
import logging

class MouseController(Runnable):
    def __init__(self, ser: Serialize, timeout: int):
        super().__init__()
        self.__ser = ser
        self._timeout = timeout
        self._speed = 1
        self._speed_lock = threading.Lock()
        self.__controller = Controller()
        self.__logger = logging.getLogger("mouse.MouseController")

    def update_speed(self, delta: float) -> bool:
        """
        Update the mouse speed by a dealta
        """
        with self._speed_lock:
            if self._speed + delta > 0:
                self._speed = self._speed + delta
                self.__logger.info(f"New speed set at x{self._speed}")
                return True
            else:
                self.__logger.error(f"Failed to update speed because the value would be negative")
                return False

    def _parse_event(self, event: MouseEvent):
        """
        Parse mouse event

        Args:
            event: The mouse event
        """
        self.__parse_event_direct(event)

    def __parse_event_direct(self, event: MouseEvent):
        """
        Parse Mouse events with the intention to directly control the mouse

        Args:
            event: The mouse event
        """
        self.__logger.debug("Current position {0}".format(self.__controller.position))

        if event.event_type == MouseEvent.EventType.MOVE:
            self.__controller.position = (event.x, event.y)
            self.__logger.debug("Moving mouse to {0}".format((event.x, event.y)))
        else:
            self.__controller.position = (event.x, event.y)
            self.__logger.debug("Moving mouse to {0}".format((event.x, event.y)))

            if event.event_type == MouseEvent.EventType.PRESSED_LEFT:
                self.__controller.press(Button.left)
                self.__logger.debug("Pressed left button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.RELEASED_LEFT:
                self.__controller.release(Button.left)
                self.__logger.debug("Released left button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.PRESSED_RIGHT:
                self.__controller.press(Button.right)
                self.__logger.debug("Pressed right button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.RELEASED_RIGHT:
                self.__controller.release(Button.right)
                self.__logger.debug("Released right button at {0}".format((event.x, event.y)))


    def _run(self):
        self.__logger.info("Mouse controller started")

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                try:
                    events = self.__ser.deserialize()
                except Exception as e:
                    self.__logger.error(f"Exception caught: {e}")
                    return

                start_time: int = datetime.now().timestamp() * 1_000

                for event in events:
                    with self._speed_lock:
                        scaled_time = event.timestamp / self._speed
                    wait_time = max(0, scaled_time + start_time - int(datetime.now().timestamp() * 1_000)) / 1_000 / self._speed
                    self.__logger.debug(f"For next event {event}, Waiting {wait_time} seconds (speed=x{self._speed}")

                    self._condition.wait(timeout=wait_time)

                    if self._state == Runnable.State.RUNNING:
                        self._parse_event(event)
                    else:
                        break

                if self._state == Runnable.State.RUNNING:
                    timeout_between_runs: int = 0
                    self.__logger.info(f"Sleeping for {timeout_between_runs} seconds")
                    self._condition.wait_for(lambda: self._state == Runnable.State.STOPPED, timeout=timeout_between_runs)

        self.__logger.info("Mouse controller stopped")

