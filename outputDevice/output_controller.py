import logging
from datetime import datetime
from threading import Lock
from typing import List, Dict

from inputDevice.input_event import InputEvent, InputSource
from outputDevice.output_handler import OutputHandler
from utils.thread.thread import Runnable
from ser.ser import Serialize


class OutputController(Runnable):
    """
    Replays a stream of InputEvents by dispatching each one to whichever
    registered OutputHandler declares support for that event's source.

    Owns the single shared timing loop (speed control, scaled waits, etc),
    so individual handlers (KeyboardController, MouseController, ...) stay
    free of any timing/threading concerns and only implement how to replay
    their own payload type.
    """

    def __init__(self, handlers: List[OutputHandler], ser: Serialize, timeout: int):
        super().__init__()
        self.__ser = ser
        self._timeout = timeout
        self._speed = 1
        self._speed_lock = Lock()
        self.__logger = logging.getLogger("outputDevice.OutputController")

        self.__handlers_by_source: Dict[InputSource, OutputHandler] = {}
        for handler in handlers:
            for source in handler.get_supported_sources():
                if source in self.__handlers_by_source:
                    self.__logger.warning(
                        f"Multiple handlers registered for source {source.name}, the last one registered will take precedence"
                    )
                self.__handlers_by_source[source] = handler

    def update_speed(self, delta: float) -> bool:
        """
        Update the playback speed by a delta.
        """
        with self._speed_lock:
            if self._speed + delta > 0:
                self._speed = self._speed + delta
                self.__logger.info(f"New speed set at x{self._speed}")
                return True
            else:
                self.__logger.error("Failed to update speed because the value would be negative")
                return False

    def _parse_event(self, event: InputEvent):
        """
        Dispatch a single InputEvent to the handler registered for its
        payload's source. Logs and skips the event if no handler supports it.

        Args:
            event: The InputEvent to replay.
        """
        source = event.payload.getSourceType()
        handler = self.__handlers_by_source.get(source)

        if handler is None:
            self.__logger.error(f"No handler registered for source {source.name}, skipping event")
            return

        handler.handle_event(event.payload)

    def _run(self):
        self.__logger.info("Output controller started")

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                try:
                    events = self.__ser.deserialize()
                except Exception as e:
                    self.__logger.error(f"Exception caught: {e}")
                    return

                with self._speed_lock:
                    speed = self._speed

                start_time: int = datetime.now().timestamp() * 1_000

                for event in events:
                    scaled_time = event.timestamp / speed
                    wait_time = max(0, scaled_time + start_time - int(datetime.now().timestamp() * 1_000)) / 1_000

                    self.__logger.debug(f"For next event {event}, Waiting {wait_time} seconds (speed=x{speed})")

                    self._condition.wait(timeout=wait_time)

                    if self._state == Runnable.State.RUNNING:
                        self._parse_event(event)
                    else:
                        break

                if self._state == Runnable.State.RUNNING:
                    timeout_between_runs: int = 0
                    self.__logger.info(f"Sleeping for {timeout_between_runs} seconds")
                    self._condition.wait_for(lambda: self._state == Runnable.State.STOPPED, timeout=timeout_between_runs)

        self.__logger.info("Output controller stopped")