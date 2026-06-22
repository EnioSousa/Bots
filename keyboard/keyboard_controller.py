from pynput import keyboard
from typing import Set
import logging

from keyboard.keyboard_event import KeyboardEvent
from inputDevice.input_event import InputPayload, InputSource
from outputDevice.output_handler import OutputHandler

class KeyboardController(OutputHandler):
    def __init__(self):
        self.__controller = keyboard.Controller()
        self.__logger = logging.getLogger("keyboard.KeyboardController")

    def get_supported_sources(self) -> Set[InputSource]:
        return {InputSource.KEYBOARD}

    def handle_event(self, event: InputPayload):
        if event.getSourceType() != InputSource.KEYBOARD:
            self.__logger.error(f"Keyboard controller cannot handle event: {event}")
            return

        self._parse_event(event)

    def _parse_event(self, event: KeyboardEvent):
        self.__logger.debug(event)

        try:
            key: keyboard.Key = event.get_key_value()
        except ValueError as e:
            self.__logger.error(f"Failed to deserialize event: {e}")
            return

        if event.event_type == KeyboardEvent.EventType.PRESSED:
            self.__controller.press(key)
            self.__logger.debug(f"Pressed key {key}")
        elif event.event_type == KeyboardEvent.EventType.RELEASED:
            self.__controller.release(key)
            self.__logger.debug(f"Released key {key}")