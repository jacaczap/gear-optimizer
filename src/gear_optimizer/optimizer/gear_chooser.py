from typing import Iterator, List

from gear_optimizer.optimizer import gear_calculator
from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item
from gear_optimizer.model import Requirements
from gear_optimizer.model import ScoreWeights
from gear_optimizer.items import items_comparator


def choose_gear(items: List[Item], weapon: Item, shield: Item, requirements: Requirements,
                score_weights: ScoreWeights) -> List[GearWithStats]:
    gears_with_stats = gear_calculator.convert_to_gear_with_stats(items, weapon, shield, score_weights)
    satisfying_gears = _filter_satisfying_gear(gears_with_stats, requirements)
    return satisfying_gears


def _filter_satisfying_gear(gears_with_stats, requirements) -> List[GearWithStats]:
    satisfying_gears = filter(lambda gear: _gear_satisfies_constraints(gear, requirements), gears_with_stats)
    top_gear = _get_only_top_gear(satisfying_gears)
    best_satisfying_gears = list(filter(lambda gear: _no_gear_is_obviously_better(gear, top_gear), top_gear))
    return best_satisfying_gears


def _gear_satisfies_constraints(gear_with_stats: GearWithStats, requirements: Requirements):
    stats = gear_with_stats.stats
    satisfies_strength = stats.strength <= requirements.max_strength
    satisfies_constraints = stats.constraints >= requirements.min_constraints
    satisfies_bonus = stats.bonus >= requirements.bonus
    satisfies_fire = stats.fire >= requirements.fire
    satisfies_frost = stats.frost >= requirements.frost
    satisfies_poison = stats.poison >= requirements.poison
    satisfies_ether = stats.ether >= requirements.ether
    if all([satisfies_strength, satisfies_constraints, satisfies_bonus, satisfies_fire, satisfies_frost,
            satisfies_poison, satisfies_ether]):
        return True
    return False


def _get_only_top_gear(gears: Iterator[GearWithStats]):
    sorted_gear = sorted(gears, key=lambda gear_with_stats: gear_with_stats.stats.score, reverse=True)
    if len(sorted_gear) > 300:
        return sorted_gear[:300]
    return sorted_gear


def _no_gear_is_obviously_better(this_gear: GearWithStats, other_gears: List[GearWithStats]):
    this_stats = this_gear.stats
    for other_gear in other_gears:
        if this_gear == other_gear:
            continue
        other_stats = other_gear.stats
        is_clearly_worse = items_comparator.is_clearly_worse(this_stats, other_stats)
        if is_clearly_worse:
            return False
    return True
