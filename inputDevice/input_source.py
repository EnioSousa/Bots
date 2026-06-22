from abc import ABC, abstractmethod
from typing import Callable

from inputDevice.input_event import InputPayload

class InputSource(ABC):
    """
    Abstract interface for a device that can produce device-specific events

    Implementations are responsible for hooking into the OS-level input
    mechanism (e.g. pynput on Windows/macOS, evdev on Linux) and invoking
    the registered callback whenever a new event occurs.

    This abstraction allows InputRecorder to remain platform-agnostic
    it only knows how to start/stop sources and receive events through
    a uniform callback, regardless of how each source captures input
    under the hood.
    """

    @abstractmethod
    def register_callback(self, callback: Callable[[InputPayload], None]) -> None:
        """
        Register a callback to be invoked every time this source produces
        a new Event

        Args:
            callback: A function accepting a single InputPayload context
        """
        raise NotImplementedError

    @abstractmethod
    def start(self) -> None:
        """
        Begin listening for input events on this device.
        """
        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:
        """
        Stop listening for input events on this device.
        """
        raise NotImplementedError