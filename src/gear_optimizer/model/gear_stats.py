from dataclasses import dataclass


@dataclass
class GearStats:
    bonus: int = 0
    constraints: int = 0
    strength: int = 0
    fire: int = 0
    frost: int = 0
    poison: int = 0
    ether: int = 0
    score: float = 0.0
