from thread.thread import Runnable

import psutil
from enum import Enum
from threading import Lock

import logging

class MemoryMonitor(Runnable):
    """
    A class to monitor the memory usage of the current process.

    Inherits from Runnable to manage threading behavior.
    """

    def __init__(self):
        """
        Initialize the memory monitor
        """
        super().__init__()
        self.process = psutil.Process()

        self.access_lock = Lock()
        self.current = self.process.memory_info().rss
        self.min = self.current
        self.max = self.current

        self.__logger = logging.getLogger("mem.MemoryMonitor")

    def _run(self):
        """
        Monitor memory usage
        """

        self.__logger.info("Monitoring started")

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                self._condition.wait(timeout=5)

                with self.access_lock:
                    self.current = self.process.memory_info().rss
                    self.min = min(self.min, self.current)
                    self.max = max(self.max, self.current)

                    self.__logger.info(f"Current: {self.current / (1024 * 1024):.2f} MB, "
                        f"Min: {self.min / (1024 * 1024):.2f} MB, "
                        f"Max: {self.max / (1024 * 1024):.2f} MB")

        self.__logger.info("Monitoring stoped")

    def get_current(self):
        """
        Get the current memory usage.

        Returns:
            int: The current memory usage in bytes.
        """
        with self.access_lock:
            return self.current