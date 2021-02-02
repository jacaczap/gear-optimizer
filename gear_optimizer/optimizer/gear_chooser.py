from typing import Iterator, List

from gear_optimizer.optimizer import gear_calculator
from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item
from gear_optimizer.model import Requirements
from gear_optimizer.model import ScoreWeights


def choose_gear(items: List[Item], weapon: Item, shield: Item, requirements: Requirements,
                score_weights: ScoreWeights) -> List[GearWithStats]:
    gears_with_stats = gear_calculator.convert_to_gear_with_stats(items, weapon, shield, score_weights)
    satisfying_gears = _filter_satisfying_gear(gears_with_stats, requirements)
    return sorted(satisfying_gears, key=lambda gear_with_stats: gear_with_stats.stats.score, reverse=True)


def _filter_satisfying_gear(gears_with_stats, requirements) -> Iterator[GearWithStats]:
    satisfying_gears = list(filter(lambda gear: _gear_satisfies_constraints(gear, requirements), gears_with_stats))
    best_satisfying_gears = filter(lambda gear: _no_gear_is_obviously_better(gear, satisfying_gears), satisfying_gears)
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


def _no_gear_is_obviously_better(this_gear: GearWithStats, other_gears: Iterator[GearWithStats]):
    this_stats = this_gear.stats
    for other_gear in other_gears:
        if this_gear == other_gear:
            continue
        other_stats = other_gear.stats
        worse_strength = this_stats.strength >= other_stats.strength
        worse_constraints = this_stats.constraints <= other_stats.constraints
        worse_bonus = this_stats.bonus <= other_stats.bonus
        worse_fire = this_stats.fire <= other_stats.fire
        worse_frost = this_stats.frost <= other_stats.frost
        worse_poison = this_stats.poison <= other_stats.poison
        worse_ether = this_stats.ether <= other_stats.ether
        if all([worse_strength, worse_constraints, worse_bonus, worse_fire, worse_frost, worse_poison, worse_ether]):
            return False
    return True
