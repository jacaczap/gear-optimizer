from typing import List

from gear_optimizer.csv_mapper import csv_reader
from gear_optimizer.items import item_finder
from gear_optimizer.model import ItemType, Item


def find_bad_eq(filename: str):
    items = csv_reader.read_gear_csv(filename)
    for item_type in [ItemType.armour, ItemType.helmet, ItemType.greave, ItemType.boots]:
        items_of_type = item_finder.get_items_of_type(items, item_type)
        _find_obviously_better_items(items_of_type)


def _find_obviously_better_items(items: List[Item]):
    for item in items:
        for other_item in items:
            if item == other_item:
                continue
            worse_strength = item.strength >= other_item.strength
            worse_constraints = item.constraints <= other_item.constraints
            worse_bonus = item.bonus <= other_item.bonus
            worse_fire = item.fire <= other_item.fire
            worse_frost = item.frost <= other_item.frost
            worse_poison = item.poison <= other_item.poison
            worse_ether = item.ether <= other_item.ether
            if all([worse_strength, worse_constraints, worse_bonus, worse_fire, worse_frost, worse_poison,
                    worse_ether]):
                print(f'{item}\nis clearly worse than\n{other_item}')
                break


if __name__ == '__main__':
    find_bad_eq('../../guild_eq.csv')
