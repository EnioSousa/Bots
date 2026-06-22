import threading

class AtomicCounter:
    def __init__(self, initial: int = 0):
        self._value = initial
        self._lock = threading.Lock()

    def increment(self, delta: int = 1) -> int:
        with self._lock:
            self._value += delta
            return self._value

    def get(self) -> int:
        with self._lock:
            return self._value