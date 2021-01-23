from armory import reader
from csv_mapper import csv_writter


def read_php_armory_to_csv(php_armory: str, filename: str, quantities: dict[str, int]):
    items = reader.read_armory(php_armory, quantities)
    csv_writter.save_gear_to_csv(filename, items)
