from typing import List

from gear_optimizer.items.item_filter import filter_items_by_type
from gear_optimizer.model import Item, ItemType


def get_items_of_type(items: List[Item], item_type: ItemType) -> List[Item]:
    items_of_type = list(filter_items_by_type(items, item_type))
    empty_item = Item('', 0, 0, 0)
    empty_item.type = item_type
    items_of_type.append(empty_item)
    return items_of_type
