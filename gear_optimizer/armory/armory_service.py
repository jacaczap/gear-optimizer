from gear_optimizer.armory import reader
from gear_optimizer.armory.online_armory import armory_getter
from gear_optimizer.csv_mapper import csv_writter
from typing import Dict


def read_php_armory_to_csv(php_armory: str, filename: str, quantities: Dict[str, int]):
    items = reader.read_armory(php_armory, quantities)
    csv_writter.save_gear_to_csv(filename, items)


def read_online_armory_to_csv(session_identifier: str, filename: str):
    quantities, php_armory = armory_getter.get_quantity_and_armory(session_identifier)
    items = reader.read_armory(php_armory, quantities)
    csv_writter.save_gear_to_csv(filename, items)
