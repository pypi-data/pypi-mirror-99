from abc import ABC, abstractmethod
from os import PathLike

from adcircpy.forcing.base import Forcing


class WindForcing(Forcing, ABC):
    def __init__(self, nws: int, interval_seconds: int):
        super().__init__(interval_seconds)
        self.NWS = nws

    @abstractmethod
    def write(self, directory: PathLike, overwrite: bool = False):
        raise NotImplementedError
