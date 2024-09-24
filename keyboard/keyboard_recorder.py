from thread.thread import Runnable

from pynput import keyboard

import logging

class KeyboardRecorder(Runnable):
    """
    A class that records keyboard events

    Inherits from RUnnable to manage threading behavior
    """

    def __init__(self):
        """
        Initalize the keyboardRecorder
        """
        super().__init__()
        self.__listener: keyboard.Listener = None
        self.__logger = logging.getLogger("keyboard.KeyboardRecorder")

    def __start_listener(self):
        """
        Start the keyboard listener if it is not already running.
        """
        if not self.__listener:
            self.__listener = keyboard.Listener(on_press=self.on_press)

        self.__listener.start()
        self.__logger.info("Listener started")

    def __stop_listener(self):
        """
        Stop the keyboard listener if it is currently running.
        """
        if self.__listener:
            self.__listener.stop()

        self.__listener = None
        self.__logger.info("Listener stopped")

    def _run(self):
        """
        The main loop for the keyboard recorder. This runs continously while the state is RUNNING
        """
        self.__logger.info("Keyboard recorder started")
        self.__start_listener()

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                self._condition.wait(timeout=60)

        self.__stop_listener()
        self.__logger.info("Keyboard recorder stopped")

    def on_press(self, key: keyboard.Key):
        """
        Handle key press events
        """
        try:
            self.__logger.debug(f"Got press event for: {key.char}")
        except AttributeError:
            self.__logger.debug(f"Got press event for special key: {key}")