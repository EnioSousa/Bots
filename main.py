from mouse.mouse_recorder import MouseRecorder
from mouse.mouse_controller import MouseController
from keyboard.keyboard_recorder import KeyboardRecorder
from mem.mem import MemoryMonitor
from ser.ser import Serialize
from log.log import setup_logging
import argparse
import threading

from pynput import keyboard
import logging

class MainThread(KeyboardRecorder):
    """
    Main thread based on keyboard monitoring system.
    """
    def __init__(self, memMonitor: MemoryMonitor, mouseRec: MouseRecorder, mouseCtrl: MouseController, parser: argparse.ArgumentParser):
        super().__init__()
        self.__logger = logging.getLogger("root")
        self.memMonitor = memMonitor
        self.mouseRec = mouseRec
        self.mouseCtrl = mouseCtrl
        self.ignoreKeys: bool = False
        self.__parser = parser

    def __repr__(self):
        return (
            "\n"
            f"{self.__parser.format_help()}"
            "\n"
            "MainThread: A keyboard monitoring system to control various components.\n"
            "Available commands:\n"
            "  - 's': Start the Memory Monitor\n"
            "  - 'm': Start Mouse Recording\n"
            "  - 'n': Stop Mouse Recording\n"
            "  - 'c': Start Mouse Controller\n"
            "  - 'x': Stop Mouse Controller\n"
            "  - 'q': Quit the program\n"
            "  - 'w': Increase controller speed by x0.25\n"
            "  - 'e': Decrease controller speed by x0.25\n"
            "  - ESC: To disable or enable key control\n"
            "\n"
        )

    def on_press(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.ignoreKeys = not self.ignoreKeys
            self.__logger.info(f"Keyboard control {'disabled' if self.ignoreKeys else 'enabled'}")
            return
        
        if self.ignoreKeys:
            return
        
        if key == keyboard.KeyCode(char='h'):
            self.__logger.info(self)
        elif key == keyboard.KeyCode(char='s'):
            self.__logger.info("Start selected")
            self.memMonitor.start()
        elif key == keyboard.KeyCode(char='q'):
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
        elif key == keyboard.KeyCode(char='w'):
            self.__logger.info("Increasing mouse speed")
            self.mouseCtrl.update_speed(0.25)
        elif key == keyboard.KeyCode(char='e'):
            self.__logger.info("Decreasing mouse speed")
            self.mouseCtrl.update_speed(-0.25)
        else:
            self.__logger.info("No functionality associated with key")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mouse bot controller",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--events_path",
        type=str,
        default="mouse_events.pkl",
        help="Path to the mouse events pickle file (e.g. mouse_events.pkl)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=5,
        help="Timeout between scripts runs."
    )
    return parser, parser.parse_args()

def main():
    parser, args = parse_args()

    ser = Serialize(args.events_path)
    mainThread: MainThread = MainThread(memMonitor=MemoryMonitor(), 
                                        mouseRec=MouseRecorder(ser), 
                                        mouseCtrl=MouseController(ser=ser, timeout=args.timeout), 
                                        parser=parser)
    mainThread.start()
    print(mainThread)

    mainThread.wait_for_end()

if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()
    logging.shutdown()