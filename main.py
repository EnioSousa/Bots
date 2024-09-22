from mouse.mouse_recorder import MouseRecorder
from mem.mem import MemoryMonitor
from ser.ser import Serialize

import logging
from log.log import setup_logging

import sys

def main():
    ser = Serialize("mouse_events.pkl")
    mouseRecorder = MouseRecorder(ser)
    memMonitor = MemoryMonitor()

    print("Press q to exit")

    print("Press s to start recording")
    print("Press d to stop recording")

    print("Press f to start bot")

    for line in sys.stdin:
        line = line.strip()

        if line.lower() == 'q':
            print("Exiting...")
            mouseRecorder.stop()
            memMonitor.stop()
            break

        elif line.lower() == 's':
            print("Starting")
            mouseRecorder.start()
            memMonitor.start()
        elif line.lower() == 'd':
            print("Stopping")
            mouseRecorder.stop()
            memMonitor.stop()

        elif line.lower() == 'f':
            mouseRecorder.stop()
            mouse_events = ser.deserialize()

            for event in mouse_events:
                print(event)

        else:
            print("Invalid event")

if __name__ == "__main__":
    setup_logging()
    logging.info("Start run")
    main()