from thread.thread import Runnable

import pickle
import logging

class Serialize(Runnable):
    """
    A class to handle serialization of mouse events in a separate thread.

    Inherits from Runnable to manage threading behavior.

    Attributes:
        __list (list): A list to store mouse events for serialization.
        __file (str): The filename for the serialized data.
        __logger (Logger): Logger instance for logging messages.
    """

    def __init__(self, file: str = "ser.pkl"):
        """
        Initialize the Serialize class.

        Args:
            file (str): The filename for the serialized data. Default is "ser.pkl".
        """
        super().__init__()
        self.__list = []
        self.__file = file
        self.__logger = logging.getLogger("ser.Serialize")

    def schedule_serialization(self, list):
        """
        Schedule serialization by adding each element to the internal list.

        Args:
            elements: A list of events to be serialized.
        """
        if list:
            with self._condition:
                self.__list.extend(list)
                self._condition.notify_all()

            self.__logger.info("Serialization scheduled")

    def _unsafe_serialize(self, events):
        """
        Serialize the provided events to a file.

        Warning:
            This method is not thread-safe.
            You must acquire the _condition before calling this

        Args:
            events: The events to be serialized.
        """

        self.__logger.debug("Attempting serialization")

        with open(self.__file, 'wb') as file:
            pickle.dump(events, file)

    def deserialize(self):
        """
        Deserialize events from the file.

        Returns:
            The deserialized events.
        """
        self.__logger.debug("Attempting deserialization")

        with self._condition:
            with open(self.__file, 'rb') as file:
                return pickle.load(file)

    def _run(self):
        """
        The main loop for the serialization thread.
        This method runs continuously while the state is RUNNING.
        """
        self.__logger.info("Serialization thread started")

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                if not self.__list:
                    self._condition.wait_for(lambda: self._state == Runnable.State.STOPPED or self.__list)

                if self.__list:
                    self._unsafe_serialize(self.__list)
                    self.__list.clear()

        self.__logger.info("Serialization thread finished")
