from mouse.mouse_recorder import MouseRecorder
from mouse.mouse_controller import MouseController
from keyboard.keyboard_recorder import KeyboardRecorder
from mem.mem import MemoryMonitor
from ser.ser import Serialize
from log.log import setup_logging

from pynput import keyboard
import logging

class MainThread(KeyboardRecorder):
    """
    Main thread based on keyboard monitoring system.
    """
    def __init__(self, memMonitor: MemoryMonitor, mouseRec: MouseRecorder, mouseCtrl: MouseController):
        super().__init__()
        self.__logger = logging.getLogger("root")
        self.memMonitor = memMonitor
        self.mouseRec = mouseRec
        self.mouseCtrl = mouseCtrl

    def __repr__(self):
        return (
            "MainThread: A keyboard monitoring system to control various components.\n"
            "Available commands:\n"
            "  - 's': Start the Memory Monitor\n"
            "  - 'm': Start Mouse Recording\n"
            "  - 'n': Stop Mouse Recording\n"
            "  - 'c': Start Mouse Controller\n"
            "  - 'x': Stop Mouse Controller\n"
            "  - 'Esc' or 'q': Quit the program\n"
        )

    def on_press(self, key: keyboard.Key):
        if key == keyboard.KeyCode(char='s'):
            self.__logger.info("Start selected")
            self.memMonitor.start()
        elif key == keyboard.Key.esc or key == keyboard.KeyCode(char='q'):
            self.__logger.info("Quit selected")
            self.mouseCtrl.stop()
            self.mouseRec.stop()
            self.memMonitor.stop()
            self.stop()
        elif key == keyboard.KeyCode(char='m'):
            self.__logger.info("Mouse Recording Start Selected")
            self.mouseCtrl.stop()
            self.mouseRec.start()
        elif key == keyboard.KeyCode(char='n'):
            self.__logger.info("Mouse Recording Stop Selected")
            self.mouseRec.stop()
        elif key == keyboard.KeyCode(char='c'):
            self.__logger.info("Mouse Controller Start Selected")
            self.mouseRec.stop()
            self.mouseCtrl.start()
        elif key == keyboard.KeyCode(char='x'):
            self.__logger.info("Mouse Controller Stop Selected")
            self.mouseCtrl.stop()
        else:
            self.__logger.info("No functionality associated with key")


def main():
    ser = Serialize("mouse_events.pkl")
    mainThread: MainThread = MainThread(memMonitor=MemoryMonitor(), mouseRec=MouseRecorder(ser), mouseCtrl=MouseController(ser))

    mainThread.start()
    print(mainThread)

    mainThread.wait_for_end()

if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()
    logging.shutdown()