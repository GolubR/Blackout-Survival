from collections import defaultdict
from dataclasses import dataclass, field


@dataclass(frozen=False)
class User:
    backpack: list[str] = field(default_factory=list)
    backpackcap: int = 0
    upgradec: int = 0
    current_location: float = 1.
    remtime: int = 0

    hp: int = 100
    damage: int = 10
    armor: int = 0
    money: int = 5000
    upgrade: dict = field(default_factory=lambda: {"trademachine": 1.})
    equipment: defaultdict[str, str | None] = field(default_factory=lambda: defaultdict(lambda: None))
