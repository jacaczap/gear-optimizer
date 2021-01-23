from gear_optimizer.armory import parser
from gear_optimizer.model import Item
from gear_optimizer import constants
from gear_optimizer.model import ItemType


def read_armory(armory_html: str, quantities: dict[str, int]) -> list[Item]:
    armory_lines = armory_html.splitlines()
    item_lines = filter(_is_requested_item_line, armory_lines)
    items = list(map(parser.parse_equipment_line_to_item, item_lines))
    _verify_if_quantities_are_correct(items, quantities)
    _set_correct_item_type(items, quantities)

    return items


def _is_requested_item_line(armory_line: str):
    return _is_equipment_line(armory_line) and _is_not_weapon_nor_shield(armory_line)


def _is_equipment_line(armory_line: str):
    return '<td><li><span onmouseover="return ovldc(\'[LT]' in armory_line


def _is_not_weapon_nor_shield(armory_line: str):
    return 'Punkty ruchu na atak' not in armory_line and 'Bonus do bloków' not in armory_line


def _verify_if_quantities_are_correct(items: list[Item], quantities: dict[str, int]):
    quantity_from_html = len(items)
    quantity_from_user = sum(quantities.values())
    if quantity_from_user != quantity_from_html:
        raise ValueError(f'{quantity_from_html} items found in html, but user expected {quantity_from_user}')


def _set_correct_item_type(items: list[Item], quantities: dict[str, int]):
    quantity_of_armours = quantities[constants.ARMOURS]
    quantity_of_helmets = quantities[constants.HELMETS]
    quantity_of_greaves = quantities[constants.GREAVES]
    quantity_of_boots = quantities[constants.BOOTS]

    for armour_index in range(quantity_of_armours):
        items[armour_index].type = ItemType.armour

    helmets_end_index = quantity_of_armours + quantity_of_helmets
    for helmet_index in range(quantity_of_armours, helmets_end_index):
        items[helmet_index].type = ItemType.helmet

    greaves_end_index = helmets_end_index + quantity_of_greaves
    for greave_index in range(helmets_end_index, greaves_end_index):
        items[greave_index].type = ItemType.greave

    boots_end_index = greaves_end_index + quantity_of_boots
    for boots_index in range(greaves_end_index, boots_end_index):
        items[boots_index].type = ItemType.boots
