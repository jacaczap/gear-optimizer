import csv

from typing import List

from model.item import Item


def read_gear_csv(file_name: str) -> List[Item]:
    items = []
    with open(file_name, newline='') as csv_file:
        gear_reader = csv.DictReader(csv_file, dialect=PolishExcel)
        for item_row in gear_reader:
            item = convert_to_item(item_row)
            items.append(item)
    return items


def convert_to_item(item_row):
    return Item(**item_row)


class PolishExcel(csv.excel):
    delimiter = ';'
