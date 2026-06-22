from pynput import keyboard
from threading import Event
from os import _exit
import argparse
import logging

from inputDevice.input_recorder import InputRecorder
from outputDevice.output_controller import OutputController
from keyboard.keyboard_recorder import KeyboardRecorder
from keyboard.keyboard_controller import KeyboardController
from mouse.mouse_recorder import MouseRecorder
from mouse.mouse_controller import MouseController
from mem.mem import MemoryMonitor
from ser.ser import Serialize
from log.log import setup_logging

class MainThread(KeyboardRecorder):
    """
    Main thread based on keyboard monitoring system.
    """
    def __init__(self,
                 memMonitor: MemoryMonitor,
                 inputRecorder: InputRecorder,
                 outputController: OutputController,
                 parser: argparse.ArgumentParser):
        super().__init__()
        self.__logger = logging.getLogger("root")
        self.memMonitor = memMonitor
        self.inputRecorder = inputRecorder
        self.outputController = outputController
        self.ignoreKeys: bool = False
        self.__parser = parser
        self.__stop_event = Event()

    def __repr__(self):
        return (
            "\n"
            f"{self.__parser.format_help()}"
            "\n"
            "MainThread: A keyboard monitoring system to control various components.\n"
            "Available commands:\n"
            "  - f12: Emergency Stop\n"
            "  - 's': Start the Memory Monitor\n"
            "  - 'm': Start Recording (mouse + keyboard)\n"
            "  - 'n': Stop Recording\n"
            "  - 'c': Start Controller (replay mouse + keyboard)\n"
            "  - 'x': Stop Controller\n"
            "  - 'q': Quit the program\n"
            "  - 'w': Increase controller speed by x0.25\n"
            "  - 'e': Decrease controller speed by x0.25\n"
            "  - ESC: To disable or enable key control\n"
            "\n"
        )

    def on_press(self, key: keyboard.Key):
        return

    def _on_event(self, key, eventType):
        return

    def on_release(self, key: keyboard.Key):
        if key == keyboard.Key.esc:
            self.ignoreKeys = not self.ignoreKeys
            self.__logger.info(f"Keyboard control {'disabled' if self.ignoreKeys else 'enabled'}")
            return
        elif key == keyboard.Key.f12:
            self.__logger.critical("Emergency failsafe triggered!")
            _exit(1)

        if self.ignoreKeys:
            return

        if key == keyboard.KeyCode(char='h'):
            self.__logger.info(self)
        elif key == keyboard.KeyCode(char='s'):
            self.__logger.info("Start selected")
            self.memMonitor.start()
        elif key == keyboard.KeyCode(char='q'):
            self.__logger.info("Quit selected")
            self.outputController.stop()
            self.inputRecorder.stop()
            self.memMonitor.stop()
            self.__stop_event.set()
        elif key == keyboard.KeyCode(char='m'):
            self.__logger.info("Recording Start Selected")
            self.outputController.stop()
            self.inputRecorder.start()
        elif key == keyboard.KeyCode(char='n'):
            self.__logger.info("Recording Stop Selected")
            self.inputRecorder.stop()
        elif key == keyboard.KeyCode(char='c'):
            self.__logger.info("Controller Start Selected")
            self.inputRecorder.stop()
            self.outputController.start()
        elif key == keyboard.KeyCode(char='x'):
            self.__logger.info("Controller Stop Selected")
            self.outputController.stop()
        elif key == keyboard.KeyCode(char='w'):
            self.__logger.info("Increasing speed")
            self.outputController.update_speed(0.25)
        elif key == keyboard.KeyCode(char='e'):
            self.__logger.info("Decreasing speed")
            self.outputController.update_speed(-0.25)

    def wait_for_end(self):
        """
        Block the calling thread until 'q' is pressed (or the failsafe
        triggers, which exits the process directly).
        """
        self.__stop_event.wait()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mouse and keyboard bot controller",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--events_path",
        type=str,
        default="input_events.pkl",
        help="Path to the unified input events pickle file (e.g. input_events.pkl)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=1,
        help="Timeout between script runs."
    )
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()

    ser = Serialize(args.events_path)

    input_recorder = InputRecorder(
        sources=[MouseRecorder(), KeyboardRecorder()],
        ser=ser
    )

    output_controller = OutputController(
        handlers=[MouseController(), KeyboardController()],
        ser=ser,
        timeout=args.timeout
    )

    mainThread: MainThread = MainThread(
        memMonitor=MemoryMonitor(),
        inputRecorder=input_recorder,
        outputController=output_controller,
        parser=parser
    )
    mainThread.start()
    print(mainThread)

    mainThread.wait_for_end()


if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()
    logging.shutdown()