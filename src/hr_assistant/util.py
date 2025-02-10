import collections.abc
import json
import threading
from pathlib import Path


class BoundedJSONBuffer(collections.abc.MutableSequence):
    """
    A thread-safe bounded buffer for storing JSON-serializable objects to a file.

    This class implements a bounded buffer using a deque to store JSON-serializable objects.
    It ensures thread-safety by using a lock for all operations that modify the buffer.
    When the buffer exceeds its capacity, it automatically flushes its contents to a specified file.

    Any remaining items in the buffer are flushed when the instance is deleted or garbage collected.

    Parameters
    ----------
        storage_path : Path
            The file path where the buffer contents will be stored when flushed.
        capacity : int
            The maximum number of items the buffer can hold before it is flushed. Defaults to 100.
    """

    def __init__(self, storage_path: Path, capacity: int = 100):
        self.capacity = capacity
        self._buffer = []
        self._storage_path = storage_path
        self._file = storage_path.open("a")
        self._lock = threading.RLock()

    def _maybe_flush(self):
        """Flush the buffer to disk, if necessary."""
        if len(self._buffer) > self.capacity:
            self.flush()

    def __getitem__(self, index):
        with self._lock:
            return self._buffer[index]

    def __setitem__(self, index, value):
        with self._lock:
            self._buffer[index] = value
            self._maybe_flush()

    def __delitem__(self, index):
        with self._lock:
            del self._buffer[index]

    def __del__(self):
        # Flush any remaining items when the object is deleted / garbage collected
        try:
            with self._lock:
                self.flush()
        finally:
            self._file.close()

    def __len__(self):
        with self._lock:
            return len(self._buffer)

    def insert(self, index, value):
        with self._lock:
            self._buffer.insert(index, value)
            self._maybe_flush()

    def append(self, value):
        with self._lock:
            self._buffer.append(value)
            self._maybe_flush()

    def clear(self):
        with self._lock:
            self._buffer.clear()

    def flush(self):
        """Flush the buffer contents to the underlying file and clear the buffer."""
        with self._lock:
            for item in self._buffer:
                self._file.write(json.dumps(item) + "\n")
            self._file.flush()
            self._buffer.clear()
