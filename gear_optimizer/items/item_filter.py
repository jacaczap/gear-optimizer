from typing import Any, Iterator

from gear_optimizer.model import ItemType, Item


def filter_items_by_type(items: Any, item_type: ItemType) -> Iterator[Item]:
    return filter(lambda item: item.type is item_type, items)
