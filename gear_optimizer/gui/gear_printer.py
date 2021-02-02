import os

from typing import List

from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item


def get_gears_as_string(gears_with_stats: List[GearWithStats]) -> str:
    gear_lines = map(lambda gs: _get_result_line(gs), gears_with_stats)
    new_line = os.linesep
    return new_line.join(gear_lines)


def _get_result_line(gear_with_stats: GearWithStats) -> str:
    gear = gear_with_stats.gear
    stats = gear_with_stats.stats
    items: List[Item] = list(vars(gear).values())
    item_names = list(map(lambda item: f'{item.name} +{item.bonus}', items))
    return f'{stats} {item_names}'
