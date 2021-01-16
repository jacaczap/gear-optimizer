from dataclasses import dataclass

from model.gear import Gear
from model.gear_stats import GearStats


@dataclass
class GearWithStats:
    gear: Gear
    stats: GearStats
