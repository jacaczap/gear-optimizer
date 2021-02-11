from dataclasses import dataclass


@dataclass
class Requirements:
    max_strength: int
    min_constraints: int
    bonus: int
    fire: int
    frost: int
    poison: int
    ether: int

    def __post_init__(self):
        self.max_strength = int(self.max_strength)
        self.min_constraints = int(self.min_constraints)
        self.bonus = int(self.bonus)
        self.fire = int(self.fire)
        self.frost = int(self.frost)
        self.poison = int(self.poison)
        self.ether = int(self.ether)
