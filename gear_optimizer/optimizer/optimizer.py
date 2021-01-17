import gear_optimizer.constants
from gear_optimizer.csv_reader import csv_reader
from gear_optimizer.model import GearWithStats
from gear_optimizer.model import Item
from gear_optimizer.model import Requirements
from gear_optimizer.model import ScoreWeights
from gear_optimizer.optimizer import gear_chooser


def optimize_gear(user_input) -> list[GearWithStats]:
    stats = user_input.stats
    in_weapon = user_input.weapon
    in_shield = user_input.shield
    in_shield_stats = user_input.shield_stats
    in_weights = user_input.weights
    in_requirements = user_input.requirements
    strength = int(stats[gear_optimizer.constants.PLAYER_STRENGTH])
    min_constraints = int(stats[gear_optimizer.constants.MIN_CONSTRAINTS])
    weapon = Item(name=in_weapon[gear_optimizer.constants.NAME], strength=in_weapon[gear_optimizer.constants.STRENGTH], constraints=in_weapon[
        gear_optimizer.constants.CONSTRAINTS],
                  bonus=0)
    shield = Item(name=in_shield[gear_optimizer.constants.NAME], strength=in_shield[gear_optimizer.constants.STRENGTH], constraints=in_shield[
        gear_optimizer.constants.CONSTRAINTS],
                  bonus=in_shield_stats[gear_optimizer.constants.BONUS], fire=in_shield_stats[
            gear_optimizer.constants.FIRE], frost=in_shield_stats[gear_optimizer.constants.FROST],
                  poison=in_shield_stats[gear_optimizer.constants.POISON], ether=in_shield_stats[
            gear_optimizer.constants.ETHER])
    weights = ScoreWeights(bonus=in_weights[gear_optimizer.constants.BONUS], fire=in_weights[
        gear_optimizer.constants.FIRE], frost=in_weights[gear_optimizer.constants.FROST],
                           poison=in_weights[gear_optimizer.constants.POISON], ether=in_weights[
            gear_optimizer.constants.ETHER])
    requirements = Requirements(max_strength=strength, min_constraints=min_constraints, bonus=in_requirements[
        gear_optimizer.constants.BONUS],
                                fire=in_requirements[gear_optimizer.constants.FIRE], frost=in_requirements[
            gear_optimizer.constants.FROST],
                                poison=in_requirements[gear_optimizer.constants.POISON], ether=in_requirements[
            gear_optimizer.constants.ETHER])
    return _optimize_gear(weapon, shield, weights, requirements, user_input.filename)


def _optimize_gear(weapon: Item, shield: Item, score_weights: ScoreWeights, requirements: Requirements,
                   filename: str) -> list[GearWithStats]:
    items = csv_reader.read_gear_csv(filename)
    gears = gear_chooser.choose_gear(items, weapon, shield, requirements, score_weights)
    truncated_gear = gears[-10:]
    return truncated_gear
