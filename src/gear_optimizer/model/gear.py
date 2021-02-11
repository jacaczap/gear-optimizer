from dataclasses import dataclass

from gear_optimizer.model.item import Item


@dataclass
class Gear:
    weapon: Item
    shield: Item
    helmet: Item
    armour: Item
    greave: Item
    boots: Item
