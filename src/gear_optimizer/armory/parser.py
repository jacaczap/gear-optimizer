import parse

from gear_optimizer.armory import templates
from gear_optimizer.model import Item


def parse_equipment_line_to_item(equipment_line: str) -> Item:
    try:
        return _parse_line(equipment_line)
    except Exception as e:
        print(f'When parsing {equipment_line} \nException raised: {e}')


def _parse_line(equipment_line: str) -> Item:
    name_and_bonus = _get_required_value_from_line(equipment_line, templates.NAME_AND_BONUS_TEMPLATE)
    return Item(name=_clean_item_name(name_and_bonus['name']),
                bonus=name_and_bonus['bonus'],
                constraints=_get_required_value_from_line(equipment_line, templates.CONSTRAINT_TEMPLATE)[0],
                strength=_get_required_value_from_line(equipment_line, templates.STRENGTH_TEMPLATE)[0],
                fire=_get_optional_value_from_line(equipment_line, templates.FIRE_TEMPLATE),
                frost=_get_optional_value_from_line(equipment_line, templates.FROST_TEMPLATE),
                poison=_get_optional_value_from_line(equipment_line, templates.POISON_TEMPLATE),
                ether=_get_optional_value_from_line(equipment_line, templates.ETHER_TEMPLATE)
                )


def _get_required_value_from_line(equipment_line: str, template: str):
    result = parse.search(template, equipment_line)
    if result is None:
        raise ValueError(f'Error when parsing: {equipment_line}')
    return result


def _get_optional_value_from_line(equipment_line: str, template: str):
    result = parse.search(template, equipment_line)
    if result is None:
        return 0
    return result[0]


def _clean_item_name(item_name: str) -> str:
    cleared_1 = item_name.removeprefix('<span class=mana><i>')
    cleared_2 = cleared_1.removeprefix('<span class=song><i>')
    return cleared_2.removesuffix(' </i></span>')
