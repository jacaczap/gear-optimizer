import csv_reader
import gear_chooser
import gear_printer
import user_input_keywords as kw
from gui import Input
from model.item import Item
from model.requirements import Requirements
from model.score_weights import ScoreWeights


def optimize_gear(user_input: Input):
    stats = user_input.stats
    in_weapon = user_input.weapon
    in_shield = user_input.shield
    in_shield_stats = user_input.shield_stats
    in_weights = user_input.weights
    in_requirements = user_input.requirements
    strength = int(stats[kw.PLAYER_STRENGTH].get())
    min_constraints = int(stats[kw.MIN_CONSTRAINTS].get())
    weapon = Item(name=in_weapon[kw.NAME].get(), strength=in_weapon[kw.STRENGTH].get(),
                  constraints=in_weapon[kw.CONSTRAINTS].get(), bonus=0)
    shield = Item(name=in_shield[kw.NAME].get(), strength=in_shield[kw.STRENGTH].get(),
                  constraints=in_shield[kw.CONSTRAINTS].get(), bonus=in_shield_stats[kw.BONUS].get(),
                  fire=in_shield_stats[kw.FIRE].get(), frost=in_shield_stats[kw.FROST].get(),
                  poison=in_shield_stats[kw.POISON].get(), ether=in_shield_stats[kw.ETHER].get())
    weights = ScoreWeights(bonus=in_weights[kw.BONUS].get(), fire=in_weights[kw.FIRE].get(),
                           frost=in_weights[kw.FROST].get(), poison=in_weights[kw.POISON].get(),
                           ether=in_weights[kw.ETHER].get())
    requirements = Requirements(max_strength=strength, min_constraints=min_constraints,
                                bonus=in_requirements[kw.BONUS].get(), fire=in_requirements[kw.FIRE].get(),
                                frost=in_requirements[kw.FROST].get(), poison=in_requirements[kw.POISON].get(),
                                ether=in_requirements[kw.ETHER].get())
    _optimize_gear(weapon, shield, weights, requirements, self.filename)


def _optimize_gear(weapon: Item, shield: Item, score_weights: ScoreWeights, requirements: Requirements, filename: str):
    items = csv_reader.read_gear_csv(filename)
    gears = gear_chooser.choose_gear(items, weapon, shield, requirements, score_weights)
    truncated_gear = gears[-10:]
    for gear in truncated_gear:
        gear_printer.print_gear(gear)
    return truncated_gear
