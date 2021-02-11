from typing import Union

from gear_optimizer.model import Item, GearStats


def is_clearly_worse(item: Union[Item, GearStats], other_item: Union[Item, GearStats]):
    worse_strength = item.strength >= other_item.strength
    worse_constraints = item.constraints <= other_item.constraints
    worse_bonus = item.bonus <= other_item.bonus
    worse_fire = item.fire <= other_item.fire
    worse_frost = item.frost <= other_item.frost
    worse_poison = item.poison <= other_item.poison
    worse_ether = item.ether <= other_item.ether
    return all([worse_strength, worse_constraints, worse_bonus, worse_fire, worse_frost, worse_poison, worse_ether])
