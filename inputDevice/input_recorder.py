import logging
from datetime import datetime
from typing import List
from threading import Lock

from inputDevice.input_event import InputEvent, InputPayload
from inputDevice.input_source import InputSource
from ser.ser import Serialize
from utils.thread.thread import Runnable

class InputRecorder(Runnable):

    def __init__(self, sources: List[InputSource], ser: Serialize):
        """
        Initialize the InputRecorder with the set of sources it will
        coordinate and the serializer events will be written to.

        Args:
            sources: The InputSource implementations to record from
                     (e.g. a MouseRecorder and a KeyboardRecorder).
            ser: The Serialize instance used to persist InputEvents.
        """
        super().__init__()
        self.__sources = sources
        self.__ser = ser

        self.__eventLock: Lock = Lock()
        self.__start_time: int = 0
        self.__events: list[InputPayload] = []

        self.__logger = logging.getLogger("inputDevice.InputRecorder")

        for source in self.__sources:
            source.register_callback(self.__on_event)

    def __start_listeners(self):
        """
        Start the device listeners
        """
        for source in self.__sources:
            source.start()

        self.__logger.info("Input Recorder started")
    
    def __stop_listeners(self):
        """
        Stop the devices listeners
        """
        for source in self.__sources:
            source.stop()
        
        self.__logger.info("Input Recorder stopped")

    def __on_event(self, eventPayload: InputPayload):
        """
        Handle event from a subRecorder
        """
        with self.__eventLock:
            elapsed = datetime.now() - self.__start_time
            elapsed_ms = int(elapsed.total_seconds() * 1_000)
            self.__events.append(InputEvent(eventPayload, elapsed_ms))
    
    def _run(self):
        """
        The main loop for the input recorder. This runs continuously while the state is RUNNING.
        """
        self.__logger.info("Input Recorder loop started")
        if self.__ser is not None:
            self.__ser.start()

        self.__start_time = datetime.now()
        self.__start_listeners()

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                self._condition.wait(timeout=15)

                with self.__eventLock:
                    batch = self.__events
                    self.__events = []

                if self.__ser is not None:
                    self.__ser.schedule_serialization(batch)

        self.__stop_listeners()
        if self.__ser is not None:
            self.__ser.stop()

        with self.__eventLock:
            self.__events = []

        self.__logger.info("Input Recorder loop stopped")