from contextlib import contextmanager
from functools import wraps
from typing import (
    Any,
    ClassVar,
    Final,
    Generic,
    Iterator,
    MutableMapping,
    Optional,
    TypeVar,
    cast,
)

import immutables
import yaml

from .sym_config_file import SymConfigFile


def fail_ok(f):
    @wraps(f)
    def wrapper(cls, *args, **kwargs):
        with cls.fail_ok():
            return f(cls, *args, **kwargs)

    return wrapper


ConfigSchema = TypeVar("ConfigSchema")


class ConfigBase(Generic[ConfigSchema], MutableMapping[str, Any]):
    __slots__ = ["file", "config"]

    __fail_ok: ClassVar[bool] = False

    file: Final[SymConfigFile]
    config: Final[ConfigSchema]

    def __init__(self) -> None:
        self.file = SymConfigFile(file_name="config.yml", uid_scope=False)
        with self.file as f:
            self.__load(f)

    def __load(self, fh):
        self.config = cast(ConfigSchema, yaml.safe_load(stream=fh) or {})

    def __flush(self, fh) -> None:
        fh.seek(0)
        fh.truncate()
        yaml.safe_dump(self.config, stream=fh)

    def __getitem__(self, key: str) -> Any:
        item = self.config[key]
        if isinstance(item, dict):
            return immutables.Map(item)
        return item

    def __delitem__(self, key: str) -> None:
        with self.atomic() as f:
            del self.config[key]
            self.__flush(f)

    def __setitem__(self, key: str, value: Any) -> None:
        with self.atomic() as f:
            if isinstance(value, immutables.Map):
                value = dict(value)
            self.config[key] = value
            self.__flush(f)

    def __iter__(self) -> Iterator[str]:
        return cast(Iterator[str], iter(self.config))

    def __len__(self) -> int:
        return len(self.config)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(self.file)})"

    @classmethod
    @contextmanager
    def fail_ok(cls):
        cls.__fail_ok = True
        yield
        cls.__fail_ok = False

    @contextmanager
    def atomic(self):
        with self.file.update(fail_ok=self.__class__.__fail_ok) as f:
            self.__load(f)
            yield f

    @classmethod
    def reset(cls):
        setattr(cls, "__instance", cls())

    @classmethod
    def instance(cls) -> "ConfigBase":
        if not hasattr(cls, "__instance"):
            cls.reset()
        return getattr(cls, "__instance")

    @classmethod
    def get_default(cls, key) -> Optional[str]:
        return cls.instance().get(f"default_{key}")

    @classmethod
    def is_logged_in(cls):
        return "email" in cls.instance()

    @classmethod
    def get_email(cls) -> str:
        return cls.instance()["email"]
