from model.gear_with_stats import GearWithStats
from model.item import Item


def print_gear(gear_with_stats: GearWithStats):
    gear = gear_with_stats.gear
    stats = gear_with_stats.stats
    items: list[Item] = list(vars(gear).values())
    item_names = list(map(lambda item: item.name, items))
    print(f'{stats} {item_names}')
