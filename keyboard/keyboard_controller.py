from keyboard.keyboard_event import KeyboardEvent
from utils.controller.inputController import InputController
from ser.ser import Serialize

from pynput import keyboard
import logging

class KeyboardController(InputController):
    def __init__(self, ser: Serialize, timeout: int):
        super().__init__(ser, timeout, "keyboard.KeyboardController")
        self.__controller = keyboard.Controller()
        self.__logger = logging.getLogger("keyboard.KeyboardController")

    def _parse_event(self, event: KeyboardEvent):
        self.__logger.debug(event)

        try:
            key: keyboard.Key = event.get_key_value()
        except ValueError as e:
            self._logger.error(f"Failed to deserialize event: {e}")
            return

        if event.event_type == KeyboardEvent.EventType.PRESSED:
            self.__controller.press(key)
        elif event.event_type == KeyboardEvent.EventType.RELEASED:
            self.__controller.release(key)