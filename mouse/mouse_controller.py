from mouse.mouse_event import MouseEvent
from thread.thread import Runnable
from ser.ser import Serialize
from datetime import datetime

from pynput.mouse import Button, Controller
import logging
import time

class MouseController(Runnable):
    def __init__(self, ser: Serialize):
        super().__init__()
        self.__ser = ser
        self.__controller = Controller()
        self.__logger = logging.getLogger("mouse.MouseController")
        self.__start_time: datetime
        self.__mouse_button: Dict[Button, bool] = {
            Button.left: False,
            Button.right: False,
            Button.middle: False
        }

    def _parse_event(self, event: MouseEvent):
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
                events = self.__ser.deserialize()

                start_time: int = datetime.now().timestamp() * 1_000

                for event in events:
                    wait_time = max(0, event.timestamp + start_time - int(datetime.now().timestamp() * 1_000)) / 1_000
                    self.__logger.debug(f"For next event {event}, Waiting {wait_time} seconds")

                    self._condition.wait(timeout=wait_time)

                    if self._state == Runnable.State.RUNNING:
                        self._parse_event(event)
                    else:
                        break

                if self._state == Runnable.State.RUNNING:
                    timeout_between_runs: int = 5
                    self.__logger.info(f"Sleeping for {timeout_between_runs} seconds")
                    self._condition.wait_for(lambda: self._state == Runnable.State.STOPPED, timeout=timeout_between_runs)

        self.__logger.info("Mouse controller stopped")

