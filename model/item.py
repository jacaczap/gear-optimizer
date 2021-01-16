from dataclasses import dataclass

from model.item_type import ItemType


@dataclass
class Item:
    name: str
    strength: int
    constraints: int
    bonus: int
    fire: int = 0
    frost: int = 0
    poison: int = 0
    ether: int = 0
    type: ItemType = ItemType.other

    def __post_init__(self):
        self.strength = int(self.strength)
        self.constraints = int(self.constraints)
        self.bonus = int(self.bonus)
        self.fire = int(self.fire)
        self.frost = int(self.frost)
        self.poison = int(self.poison)
        self.ether = int(self.ether)
        self.type = ItemType(self.type)
