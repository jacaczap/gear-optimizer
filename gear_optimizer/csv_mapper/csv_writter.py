import csv
from dataclasses import fields, asdict
from typing import List, Dict

from gear_optimizer.model import Item


def save_gear_to_csv(file_name: str, items: List[Item]):
    item_fields = fields(Item)
    field_names = list(map(lambda item: item.name, item_fields))
    rows = _prepare_rows(items)
    with open(file_name, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names, dialect=PolishExcel)
        writer.writeheader()
        writer.writerows(rows)


def _prepare_rows(items: List[Item]):
    item_dicts = map(asdict, items)
    return map(_change_type_to_string, item_dicts)


def _change_type_to_string(item_dict: Dict[str, any]) -> Dict[str, any]:
    item_dict['type'] = str(item_dict['type'])
    return item_dict


class PolishExcel(csv.excel):
    delimiter = ';'
