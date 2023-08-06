import os
from pathlib import Path
from typing import Any, Hashable, ItemsView, ValuesView, KeysView, Iterator, Dict

import dill


class _Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class _DBManager:
    def __init__(self) -> None:
        self.file_name = Path(os.path.expanduser("~")) / ".boydem" / "boydem.pickle"
        self.file_name.parent.mkdir(parents=True, exist_ok=True)
        self.file = None

    def set(self, obj: Any) -> None:
        with self.file_name.open("wb") as f:
            dill.dump(obj, f)

    def delete(self, obj: Any) -> None:
        self.set(obj)

    def clear(self) -> None:
        self.file_name.unlink(missing_ok=True)

    def get(self) -> Dict:
        try:
            with self.file_name.open("rb") as f:
                obj = dill.load(f)
        except FileNotFoundError:
            obj = dict()
        except EOFError:
            self.file_name.unlink()
            obj = dict()
        return obj


class _Boydem(metaclass=_Singleton):
    def __init__(self):
        self.__dict__ = _db_manager.get()

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.__setattr__(key, value)

    def __getitem__(self, item: Any) -> Any:
        return self.__getattr__(item)

    def __delitem__(self, key: Any) -> Any:
        self.__delattr__(key)

    def __setattr__(self, key: Hashable, value: Any) -> None:
        if key == "__dict__":
            super().__setattr__("__dict__", value)
        else:
            self.__dict__[key] = value
        _db_manager.set(self.__dict__)

    def __getattr__(self, item: Any) -> Any:
        return self.__dict__[item]

    def __delattr__(self, item: Any) -> None:
        del self.__dict__[item]
        _db_manager.delete(self.__dict__)

    def keys(self) -> KeysView:
        return self.__dict__.keys()

    def values(self) -> ValuesView:
        return self.__dict__.values()

    def items(self) -> ItemsView:
        return self.__dict__.items()

    def clear(self) -> None:
        self.__dict__.clear()
        _db_manager.clear()

    def __contains__(self, item: Hashable) -> bool:
        return item in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self) -> Iterator:
        return iter(self.items())

    def __repr__(self):
        items = self.__dict__.items()
        if items:
            res = "\n".join([f"{key}: {value}" for key, value in items])
        else:
            res = "Nothing here 😳"
        return res


_db_manager = _DBManager()
boydem = _Boydem()


__all__ = ["boydem"]
