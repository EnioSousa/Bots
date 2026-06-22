from abc import ABC, abstractmethod
from typing import Set

from inputDevice.input_event import InputEvent, InputPayload, InputSource


class OutputHandler(ABC):
    """
    """
    
    @abstractmethod
    def get_supported_sources(self) -> Set[InputSource]:
        """
        Returns:
            Set[InputEvent.Source]: The set of sources this handler is
            able to replay (e.g. {InputEvent.Source.MOUSE}).
        """
        raise NotImplementedError
    
    @abstractmethod
    def handle_event(self, payload: InputPayload) -> None:
        """
        Replay a single payload using this handler's underlying mechanism
        (e.g. pynput mouse/keyboard Controller).

        Args:
            payload: The device-specific event to replay.
        """
        raise NotImplementedError