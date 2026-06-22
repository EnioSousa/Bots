import tkinter as tk
from tkinter import ttk
from os import _exit
from pynput import keyboard
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

class BotGUI(KeyboardRecorder):
    """
    Minimal control panel for the input recorder / output controller.
    Buttons mirror the keyboard shortcuts from MainThread.on_release.
    """

    def __init__(self, root: tk.Tk, inputRecorder, outputController, memMonitor):
        super().__init__()
        self.__logger = logging.getLogger("gui.BotGUI")
        self.__root = root
        self.__inputRecorder = inputRecorder
        self.__outputController = outputController
        self.__memMonitor = memMonitor

        root.title("Something")
        root.geometry("280x260")
        root.attributes("-topmost", True)  # stay on top of the game window

        frame = ttk.Frame(root, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Start Recording", command=self.__start_recording).pack(fill=tk.X, pady=4)
        ttk.Button(frame, text="Stop Recording", command=self.__stop_recording).pack(fill=tk.X, pady=4)

        ttk.Separator(frame).pack(fill=tk.X, pady=8)

        ttk.Button(frame, text="Start Controller", command=self.__start_controller).pack(fill=tk.X, pady=4)
        ttk.Button(frame, text="Stop Controller", command=self.__stop_controller).pack(fill=tk.X, pady=4)

        ttk.Button(frame, text="Stop Everything", command=self.__stop_all).pack(fill=tk.X, pady=4)
        ttk.Button(frame, text="Quit", command=self.__quit).pack(fill=tk.X, pady=4)

        ttk.Separator(frame).pack(fill=tk.X, pady=8)

        self.__status_label = ttk.Label(frame, text="Status: Idle")
        self.__status_label.pack(pady=4)

        failsafe = tk.Button(
            frame, text="EMERGENCY STOP", command=self.__emergency_stop,
            bg="red", fg="white", font=("Arial", 10, "bold")
        )
        failsafe.pack(fill=tk.X, pady=(12, 0))

        root.protocol("WM_DELETE_WINDOW", self.__quit)
        root.geometry("280x340")  # bumped to fit the new buttons

        self.start()

    def on_press(self, key: keyboard.Key):
        return

    def _on_event(self, key, eventType):
        return

    def on_release(self, key: keyboard.Key):
        if key == keyboard.Key.f12:
            self.__logger.info("Keyboard Controll: Emergency failsafe triggered!")
            self.__emergency_stop()
        elif key == keyboard.Key.f11:
            self.__logger.info("Keyboard Controll: Clean exiting")
            self.__quit()
        elif key == keyboard.Key.f10:
            self.__logger.info("Keyboard Controll: Stopping everything")
            self.__stop_all()

    def __set_status(self, text: str):
        self.__status_label.config(text=f"Status: {text}")

    def __start_recording(self):
        self.__outputController.stop()
        self.__inputRecorder.start()
        self.__set_status("Recording")

    def __stop_recording(self):
        self.__inputRecorder.stop()
        self.__set_status("Idle")

    def __start_controller(self):
        self.__inputRecorder.stop()
        self.__outputController.start()
        self.__set_status("Replaying")

    def __stop_controller(self):
        self.__outputController.stop()
        self.__set_status("Idle")

    def __stop_all(self):
        self.__stop_recording()
        self.__stop_controller()

    def __quit(self):
        self.__logger.info("Quit selected")
        self.__stop_all()
        self.__memMonitor.stop()
        self.stop()
        self.__root.destroy()

    def __emergency_stop(self):
        _exit(1)


def run_gui(inputRecorder, outputController, memMonitor):
    root = tk.Tk()
    BotGUI(root, inputRecorder, outputController, memMonitor)
    root.mainloop()

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
        default=5,
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

    memMonitor = MemoryMonitor()

    run_gui(input_recorder, output_controller, memMonitor)


if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()
    logging.shutdown()