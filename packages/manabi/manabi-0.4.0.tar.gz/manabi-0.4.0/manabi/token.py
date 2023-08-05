import calendar
import struct
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional

from attr import Factory, dataclass
from branca import Branca  # type: ignore

from .util import cattrib, from_string


def now() -> int:
    return calendar.timegm(datetime.utcnow().timetuple())


@dataclass
class TTL:
    initial: int = cattrib(int)
    refresh: int = cattrib(int)

    @classmethod
    def from_dictionary(cls, config: dict) -> "TTL":
        initial = config["manabi"]["initial"]
        refresh = config["manabi"]["refresh"]
        return cls(initial, refresh)


@dataclass
class Key:
    data: bytes = cattrib(bytes, lambda x: len(x) == 32)

    @classmethod
    def from_dictionary(cls, config: dict) -> "Key":
        return cls(from_string(config["manabi"]["key"]))


@dataclass
class Config:
    key: Key = cattrib(Key)
    ttl: TTL = cattrib(TTL)

    @classmethod
    def from_dictionary(cls, config: dict) -> "Config":
        return cls(Key.from_dictionary(config), TTL.from_dictionary(config))


class State(Enum):
    valid = 1, "the token is intact, path is valid and ttl ok"
    expired = 2, "the token is intact, path valid but the ttl is expired"
    not_valid_yet = 3, "the token intact, but not valid yet, clockskew?"
    invalid = 4, "the token is not valid, authentication failed"


@dataclass
class Token:
    key: Key = cattrib(Key)
    path: Optional[Path] = cattrib(Path, default=None)
    timestamp: Optional[int] = cattrib(
        int, default=Factory(lambda: now()), optional=True
    )
    ciphertext: str = cattrib(str, default=None)

    def as_url(self) -> str:
        if self.path is None:
            raise ValueError("path may not be None")
        path = self.path.name
        return f"{self.encode()}/{path}"

    def path_as_url(self) -> str:
        return f"/{self.path}"

    def encode(self) -> str:
        if self.path is None:
            raise ValueError("path may not be None")
        if self.timestamp is None:
            self.timestamp = now()
        self.ciphertext = _encode(self.key.data, str(self.path), self.timestamp)
        return self.ciphertext

    @classmethod
    def from_token(cls, token: "Token", timestamp: int = None) -> "Token":
        if timestamp is None:
            return cls(token.key, token.path, now())
        else:
            return cls(token.key, token.path, timestamp)

    @classmethod
    def from_ciphertext(cls, key: Key, ciphertext: str) -> "Token":
        assert ciphertext
        branca = Branca(key.data)
        try:
            timestamp = branca.timestamp(ciphertext)
        except (struct.error, ValueError):
            return cls(key, None, None)
        try:
            token_path = Path(branca.decode(ciphertext).decode("UTF-8"))
        except RuntimeError:
            return cls(key, None, timestamp)
        return cls(key, token_path, timestamp, ciphertext)

    def check(self, ttl: Optional[int] = None) -> State:
        if self.path is None or self.timestamp is None:
            return State.invalid
        if ttl is not None:
            future = self.timestamp + ttl
            past = self.timestamp - 1
            t = now()
            if t < past:
                return State.not_valid_yet
            if t > future:
                return State.expired
        return State.valid

    def refresh(self, ttl: TTL) -> State:
        return self.check(ttl.refresh)

    def initial(self, ttl: TTL) -> State:
        return self.check(ttl.initial)


def _encode(key: bytes, path: str, now: Optional[int] = None) -> str:
    f = Branca(key)
    p = path.encode("UTF-8")
    ciphertext = f.encode(p, now)
    return ciphertext


def _decode(key: bytes, ciphertext: str, ttl=None) -> str:
    f = Branca(key)
    return f.decode(ciphertext, ttl).decode("UTF-8")
