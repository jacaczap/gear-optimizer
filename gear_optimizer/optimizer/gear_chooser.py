from typing import Iterator, List

from gear_optimizer.optimizer import gear_calculator
from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item
from gear_optimizer.model import Requirements
from gear_optimizer.model import ScoreWeights


def choose_gear(items: List[Item], weapon: Item, shield: Item, requirements: Requirements,
                score_weights: ScoreWeights) -> List[GearWithStats]:
    gears_with_stats = gear_calculator.convert_to_gear_with_stats(items, weapon, shield, score_weights)
    satisfying_gears = filter_satisfying_gear(gears_with_stats, requirements)
    return sorted(satisfying_gears, key=lambda gear_with_stats: gear_with_stats.stats.score)


def filter_satisfying_gear(gears_with_stats, requirements) -> Iterator[GearWithStats]:
    satisfying_gears = filter(lambda gear_with_stats: _gear_satisfies_constraints(gear_with_stats, requirements),
                              gears_with_stats)
    return satisfying_gears


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
