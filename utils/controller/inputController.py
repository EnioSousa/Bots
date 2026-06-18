from utils.thread.thread import Runnable
from ser.ser import Serialize
from datetime import datetime
from abc import abstractmethod

import threading
import logging


class InputController(Runnable):
    """
    Base class for replaying timestamped input events (mouse, keyboard, etc).
    Subclasses only need to implement _parse_event for their specific input type.
    """

    def __init__(self, ser: Serialize, timeout: int, logger_name: str):
        super().__init__()
        self.__ser = ser
        self._timeout = timeout
        self._speed = 1
        self._speed_lock = threading.Lock()
        self._logger = logging.getLogger(logger_name)

    def update_speed(self, delta: float) -> bool:
        """
        Update the playback speed by a delta.
        """
        with self._speed_lock:
            if self._speed + delta > 0:
                self._speed = self._speed + delta
                self._logger.info(f"New speed set at x{self._speed}")
                return True
            else:
                self._logger.error("Failed to update speed because the value would be negative")
                return False

    @abstractmethod
    def _parse_event(self, event):
        """
        Replay a single event. Must be implemented by subclasses.
        """
        raise NotImplementedError

    def _run(self):
        self._logger.info(f"{self.__class__.__name__} started")

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                try:
                    events = self.__ser.deserialize()
                except Exception as e:
                    self._logger.error(f"Exception caught: {e}")
                    return

                start_time: int = datetime.now().timestamp() * 1_000

                for event in events:
                    with self._speed_lock:
                        scaled_time = event.timestamp / self._speed
                        speed = self._speed
                    wait_time = max(0, scaled_time + start_time - int(datetime.now().timestamp() * 1_000)) / 1_000
                    self._logger.debug(f"For next event {event}, Waiting {wait_time} seconds (speed=x{speed})")

                    self._condition.wait(timeout=wait_time)

                    if self._state == Runnable.State.RUNNING:
                        self._parse_event(event)
                    else:
                        break

                if self._state == Runnable.State.RUNNING:
                    timeout_between_runs: int = 0
                    self._logger.info(f"Sleeping for {timeout_between_runs} seconds")
                    self._condition.wait_for(lambda: self._state == Runnable.State.STOPPED, timeout=timeout_between_runs)

        self._logger.info(f"{self.__class__.__name__} stopped")