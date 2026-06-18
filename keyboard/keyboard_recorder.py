from utils.thread.thread import Runnable
from keyboard.keyboard_event import KeyboardEvent
from ser.ser import Serialize

from pynput import keyboard
from threading import Lock
from datetime import datetime

import logging

class KeyboardRecorder(Runnable):
    """
    A class that records keyboard events

    Inherits from RUnnable to manage threading behavior
    """

    def __init__(self, ser: Serialize = None):
        """
        Initalize the keyboardRecorder
        """
        super().__init__()
        self.__listener: keyboard.Listener = None

        self.__eventLock: Lock = Lock()
        self.__events: list[KeyboardEvent] = []
        self.__record_start: datetime = datetime.now()

        self.__ser: Serialize = ser

        self.__logger = logging.getLogger("keyboard.KeyboardRecorder")

    def __start_listener(self):
        """
        Start the keyboard listener if it is not already running.
        """
        if not self.__listener:
            self.__listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

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
        if self.__ser is not None:
            self.__ser.start()
        self.__start_listener()

        self.__record_start = datetime.now()

        with self._condition:
            while self._state == Runnable.State.RUNNING:
                self._condition.wait(timeout=60)

            with self.__eventLock:
                if self.__ser is not None:
                    self.__ser.schedule_serialization(self.__events)
                self.__events.clear()

    
        self.__stop_listener()
        if self.__ser is not None:
            self.__ser.stop()

        with self.__eventLock:
            self.__events = []

        self.__logger.info("Keyboard recorder stopped")

    def on_press(self, key: keyboard.Key):
        """
        Handle key press events
        """
        self._on_event(key, KeyboardEvent.EventType.PRESSED)

    def on_release(self, key: keyboard.Key):
        """
        Handle key release events
        """
        self._on_event(key, KeyboardEvent.EventType.RELEASED)
    
    def _on_event(self, key: keyboard.Key, eventType: KeyboardEvent.EventType):
        """
        Handle a generic event
        """
        event = KeyboardEvent(eventType, key, datetime.now() - self.__record_start)
        with self.__eventLock:
            self.__events.append(event)

        self.__logger.debug(event)

