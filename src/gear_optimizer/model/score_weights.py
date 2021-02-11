from dataclasses import dataclass


@dataclass
class ScoreWeights:
    bonus: float
    fire: float
    frost: float
    poison: float
    ether: float

    def __post_init__(self):
        self.bonus = float(self.bonus)
        self.fire = float(self.fire)
        self.frost = float(self.frost)
        self.poison = float(self.poison)
        self.ether = float(self.ether)
