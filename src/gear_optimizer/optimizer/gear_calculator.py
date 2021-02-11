import itertools
from typing import Iterator, List, Tuple

from gear_optimizer.items.item_filter import filter_items_by_type
from gear_optimizer.items.item_finder import get_items_of_type
from gear_optimizer.model import Gear
from gear_optimizer.model import GearStats
from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item
from gear_optimizer.model import ItemType
from gear_optimizer.model import ScoreWeights


def convert_to_gear_with_stats(items: List[Item], weapon: Item, shield: Item, score_weights: ScoreWeights) -> Iterator[
    GearWithStats]:
    helmets = get_items_of_type(items, ItemType.helmet)
    armours = get_items_of_type(items, ItemType.armour)
    greaves = get_items_of_type(items, ItemType.greave)
    boots = get_items_of_type(items, ItemType.boots)

    items_possibilities = itertools.product(helmets, armours, greaves, boots)
    return map(lambda gear_possibility: _convert_to_gear_with_stats(gear_possibility, weapon, shield, score_weights),
               items_possibilities)


def _convert_to_gear_with_stats(gear_possibility: Tuple[Item], weapon: Item, shield: Item,
                                score_weights: ScoreWeights) -> GearWithStats:
    helmet = next(filter_items_by_type(gear_possibility, ItemType.helmet))
    armour = next(filter_items_by_type(gear_possibility, ItemType.armour))
    greave = next(filter_items_by_type(gear_possibility, ItemType.greave))
    boots = next(filter_items_by_type(gear_possibility, ItemType.boots))
    gear = Gear(weapon=weapon, shield=shield, helmet=helmet, armour=armour, greave=greave, boots=boots)
    return _calculate_gear_with_stats(gear, score_weights)


def _calculate_gear_with_stats(gear: Gear, score_weights: ScoreWeights) -> GearWithStats:
    stats = GearStats()
    for item in vars(gear).values():
        if item is None:
            continue
        stats.bonus += item.bonus
        stats.constraints += item.constraints
        stats.strength += item.strength
        stats.fire += item.fire
        stats.frost += item.frost
        stats.poison += item.poison
        stats.ether += item.ether
    stats.score = _calculate_gear_score(stats, score_weights)
    return GearWithStats(gear=gear, stats=stats)


def _calculate_gear_score(stats: GearStats, weights: ScoreWeights) -> float:
    bonus_score = stats.bonus * weights.bonus
    fire_score = stats.fire * weights.fire
    frost_score = stats.frost * weights.frost
    poison_score = stats.poison * weights.poison
    ether_score = stats.ether * weights.ether
    return bonus_score + fire_score + frost_score + poison_score + ether_score
