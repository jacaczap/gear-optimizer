from typing import Dict
import parse

from gear_optimizer.armory.online_armory import templates


def parse_armory_room_file(armory_room_file: str) -> Dict[str, int]:
    result = parse.search(templates.ARMORY_ROOM_TEMPLATE, armory_room_file)
    return result.named
