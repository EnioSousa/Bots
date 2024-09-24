from mouse.mouse_recorder import MouseRecorder
from mouse.mouse_controller import MouseController
from mem.mem import MemoryMonitor
from ser.ser import Serialize

import logging
from log.log import setup_logging

import sys

def main():
    ser = Serialize("mouse_events.pkl")
    mouseRecorder = MouseRecorder(ser)
    mouseController = MouseController(ser)
    memMonitor = MemoryMonitor()

    print("Press a to start")
    print("Press s to exit")

    print("Press d to start recording")
    print("Press f to stop recording")

    print("Press g to start controller")
    print("Press h to stop controller")

    for line in sys.stdin:
        line = line.strip()

        if line.lower() == 'a':
            print("Starting...")
            memMonitor.start()
        elif line.lower() == 's':
            print("Exiting...")
            mouseRecorder.stop()
            mouseController.stop()
            memMonitor.stop()
            break

        elif line.lower() == 'd':
            mouseController.stop()
            mouseRecorder.start()
        elif line.lower() == 'f':
            mouseRecorder.stop()

        elif line.lower() == 'g':
            mouseRecorder.stop()
            mouseController.start()
        elif line.lower() == 'h':
            mouseController.stop()

        else:
            print("Invalid event")

if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()