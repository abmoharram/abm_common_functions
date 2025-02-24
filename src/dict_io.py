import os
import pickle
import time
from typing import Any

from base_class import BaseClass


class DictIO(BaseClass):
    def __init__(self, filepath: str, load: bool = True):
        """Initialize the class with a filepath and load the data if it exists."""
        super().__init__()
        self.filepath = filepath
        if load:
            if os.path.exists(filepath):
                self.load()
            else:
                self.data: dict[str, Any] = {}
                self._set_first_timestamp()

    def _set_last_read_timestamp(self) -> None:
        self.data["_last_read_timestamp"] = time.time()

    def _get_last_read_timestamp(self) -> float:
        return self.data.get("_last_read_timestamp", None)

    def _set_first_timestamp(self) -> None:
        self.data["_first_timestamp"] = time.time()

    def _get_first_timestamp(self) -> float:
        return self.data.get("first_timestamp", None)

    def _set_last_memory_update_timestamp(self) -> None:
        self.data["_last_memory_update_timestamp"] = time.time()

    def _get_last_memory_update_timestamp(self) -> float:
        return self.data.get("_last_memory_update_timestamp", None)

    def _set_last_write_timestamp(self) -> None:
        self.data["_last_write_timestamp"] = time.time()

    def _get_last_write_timestamp(self) -> float:
        return self.data.get("_last_write_timestamp", None)

    def _is_saved(self) -> bool:
        """Check if the data is saved to the file."""
        if not os.path.exists(self.filepath):
            return False

        if getattr(self, "data", None) is None:
            return False

        if self.data.get("_last_write_timestamp", None) is None:
            return False

        if self._get_last_memory_update_timestamp() > self._get_last_write_timestamp():
            return False

        return True

    def save(self) -> None:
        """Save the data to the file."""
        if self._is_saved():
            return

        try:
            path = os.path.dirname(self.filepath)
            if not os.path.exists(path):
                os.makedirs(path)

            self._set_last_write_timestamp()

            with open(self.filepath, "wb") as f:
                pickle.dump(self.data, f)
        except Exception as e:
            error_message = f"Error saving data to {self.filepath}: {e}"
            self.logger.error(error_message)
            raise Exception(error_message)

    def load(self, overwrite: bool = False) -> None:
        """Load the data from the file.

        If the data is not saved, it will raise an error.
        If overwrite is False, it will raise an error if the data is not saved.
        """
        if (not self._is_saved()) and (not overwrite):
            error_message = "Loading will overwrite the in-memory updates."
            self.logger.error(error_message)

        with open(self.filepath, "rb") as f:
            self.data = pickle.load(f)

        self._set_last_read_timestamp()

    def __getitem__(self, key: str):
        self._set_last_read_timestamp()
        return self.data[key]

    def __setitem__(self, key: str, value: Any):
        self._set_last_memory_update_timestamp()
        self.data[key] = value

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        result = f"DictIO: File:{self.filepath}\n"
        is_saved = "Yes ✅" if self._is_saved() else "Mo ❌"
        result += f"Is the file saved: {is_saved}\n"
        keys = sorted(self.data.keys())
        for key in keys:
            result += f"{key}: {self.data[key]}\n"
        return result
