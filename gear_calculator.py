import itertools
from typing import Iterator, List, Tuple
from typing import Any

from model.gear import Gear
from model.gear_stats import GearStats
from model.gear_with_stats import GearWithStats
from model.item import Item
from model.item_type import ItemType
from model.score_weights import ScoreWeights


def convert_to_gear_with_stats(items: List[Item], weapon: Item, shield: Item, score_weights: ScoreWeights) -> Iterator[
    GearWithStats]:
    helmets = _get_items_of_type(items, ItemType.helmet)
    armours = _get_items_of_type(items, ItemType.armour)
    greaves = _get_items_of_type(items, ItemType.greave)
    boots = _get_items_of_type(items, ItemType.boots)

    items_possibilities = itertools.product(helmets, armours, greaves, boots)
    return map(lambda gear_possibility: _convert_to_gear_with_stats(gear_possibility, weapon, shield, score_weights),
               items_possibilities)


def _get_items_of_type(items: List[Item], item_type: ItemType) -> List[Item]:
    items_of_type = list(_filter_items_by_type(items, item_type))
    empty_item = Item('', 0, 0, 0)
    empty_item.type = item_type
    items_of_type.append(empty_item)
    return items_of_type


def _convert_to_gear_with_stats(gear_possibility: Tuple[Item], weapon: Item, shield: Item,
                                score_weights: ScoreWeights) -> GearWithStats:
    helmet = next(_filter_items_by_type(gear_possibility, ItemType.helmet))
    armour = next(_filter_items_by_type(gear_possibility, ItemType.armour))
    greave = next(_filter_items_by_type(gear_possibility, ItemType.greave))
    boots = next(_filter_items_by_type(gear_possibility, ItemType.boots))
    gear = Gear(weapon=weapon, shield=shield, helmet=helmet, armour=armour, greave=greave, boots=boots)
    return _calculate_gear_with_stats(gear, score_weights)


def _filter_items_by_type(items: Any, item_type: ItemType) -> Iterator[Item]:
    return filter(lambda item: item.type is item_type, items)


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
