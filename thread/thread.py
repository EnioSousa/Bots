from abc import ABC, abstractmethod
from enum import Enum
import threading
import logging

class Runnable(ABC):
    class State(Enum):
        """
        Enum describing the different states of the MouseRecorder.

        Attributes:
            STOPPED (int): The recorder is not running.
            RUNNING (int): The recorder is actively capturing mouse events.
        """
        STOPPED = 0
        RUNNING = 1

    def __init__(self):
        self.__thread: threading.Thread = None

        self.__lock: threading.Lock = threading.Lock()
        self._condition: threading.Condition = threading.Condition(self.__lock)

        self._state: Runnable.State = Runnable.State.STOPPED

        self.__logger = logging.getLogger("thread.Runnable")

    def start(self):
        """
        Start the thread and run the runnable method.
        """
        with self._condition:
            if self._state == Runnable.State.STOPPED:
                self._state = Runnable.State.RUNNING
                self.__thread = threading.Thread(target=self._run)
                self.__thread.start()
                self._condition.notify_all()
                self.__logger.debug("Thread started")
            else:
                self.__logger.error("Thread already running")

    def stop(self):
        """
        Stop the thread
        """
        with self._condition:
            if self._state == Runnable.State.RUNNING:
                self._state = Runnable.State.STOPPED
                self._condition.notify_all()
                self.__logger.debug("Thread stopped")
            else:
                self.__logger.error("Thread already stopped")

        if self.__thread is not None and self.__thread.is_alive():
            self.__thread.join()

        self.__thread = None

    def wait_time(self, time: int):
        threading.Event().wait(time)

    @abstractmethod
    def _run(self):
        """
        Method should be implemented by the subclasses
        """
        self.__logger.critical("Not this one")
        pass