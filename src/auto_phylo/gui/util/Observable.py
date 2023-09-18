from typing import List, Callable


class Observable:
    def __init__(self):
        self._callbacks: List[Callable[[], None]] = []

    def _notify_observers(self) -> None:
        for callback in self._callbacks:
            callback()

    def add_callback(self, callback: Callable[[], None]) -> None:
        self._callbacks.append(callback)

    def has_callback(self, callback: Callable[[], None]) -> bool:
        return callback in self._callbacks

    def remove_callback(self, callback: Callable[[], None]) -> None:
        self._callbacks.remove(callback)

    def remove_all_callbacks(self) -> None:
        self._callbacks.clear()
