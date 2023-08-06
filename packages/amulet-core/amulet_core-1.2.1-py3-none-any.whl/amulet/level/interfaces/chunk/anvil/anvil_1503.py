from __future__ import annotations

from .anvil_1484 import (
    Anvil1484Interface,
)


class Anvil1503Interface(Anvil1484Interface):
    def __init__(self):
        Anvil1484Interface.__init__(self)
        self.features["height_map"] = "C|V3"

    @staticmethod
    def minor_is_valid(key: int):
        return 1503 <= key < 1908


export = Anvil1503Interface
