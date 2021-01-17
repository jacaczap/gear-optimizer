from dataclasses import dataclass

from gear_optimizer.model.gear import Gear
from gear_optimizer.model.gear_stats import GearStats


@dataclass
class GearWithStats:
    gear: Gear
    stats: GearStats
