from pynput import keyboard
from typing import Callable
import logging

from inputDevice.input_event import InputPayload
from inputDevice.input_source import InputSource
from keyboard.keyboard_event import KeyboardEvent

class KeyboardRecorder(InputSource):
    """
    Concreate InputSource implementation that captures keyboard events via pynput and forwards
    them to a registered callback as KeyboardEvent payloads

    This class is not concurently safe, and start/stop methods should be handled carefully
    """

    def __init__(self):
        """
        Initalize the keyboardRecorder
        """
        super().__init__()
        self.__callback: Callable[[InputPayload], None] = None
        self.__listener: keyboard.Listener = None
        self.__logger = logging.getLogger("keyboard.KeyboardRecorder")

    def register_callback(self, callback: Callable[[InputPayload], None]) -> None:
        """
        Register Event callback
        """
        self.__callback = callback
        self.__logger.info("Callback registered")

    def start(self):
        """
        Start the keyboard listener if it is not already running.
        """
        if not self.__listener:
            self.__listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

        self.__listener.start()
        self.__logger.info("Listener started")

    def stop(self):
        """
        Stop the keyboard listener if it is currently running.
        """
        if self.__listener:
            self.__listener.stop()

        self.__listener = None
        self.__logger.info("Listener stopped")

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
        event = KeyboardEvent(eventType, key)
        if self.__callback is not None:
            self.__callback(event)

        self.__logger.debug(event)

