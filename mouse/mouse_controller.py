from mouse.mouse_event import MouseEvent
from utils.controller.inputController import InputController
from ser.ser import Serialize

from pynput.mouse import Button, Controller
import logging

class MouseController(InputController):
    def __init__(self, ser: Serialize, timeout: int):
        super().__init__(ser=ser, timeout=timeout, logger_name="mouse.MouseController")
        self.__controller: Controller = Controller()
        self.__logger = logging.getLogger("mouse.MouseController")


    def _parse_event(self, event: MouseEvent):
        """
        Parse Mouse events with the intention to control the mouse

        Args:
            event: The mouse event
        """
        self.__logger.debug(event)

        if event.event_type == MouseEvent.EventType.MOVE:
            self.__controller.position = (event.x, event.y)
            self.__logger.debug("Moving mouse to {0}".format((event.x, event.y)))
        else:
            self.__controller.position = (event.x, event.y)
            self.__logger.debug("Moving mouse to {0}".format((event.x, event.y)))

            if event.event_type == MouseEvent.EventType.PRESSED_LEFT:
                self.__controller.press(Button.left)
                self.__logger.debug("Pressed left button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.RELEASED_LEFT:
                self.__controller.release(Button.left)
                self.__logger.debug("Released left button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.PRESSED_RIGHT:
                self.__controller.press(Button.right)
                self.__logger.debug("Pressed right button at {0}".format((event.x, event.y)))

            elif event.event_type == MouseEvent.EventType.RELEASED_RIGHT:
                self.__controller.release(Button.right)
                self.__logger.debug("Released right button at {0}".format((event.x, event.y)))


