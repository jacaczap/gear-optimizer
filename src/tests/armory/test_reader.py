import os
from unittest import TestCase

from gear_optimizer import constants
from gear_optimizer.armory import reader
from gear_optimizer.model import Item
from gear_optimizer.model import ItemType


class Test(TestCase):
    def test_read_armory(self):
        # given
        this_test_dir = os.path.dirname(__file__)
        with open(os.path.join(this_test_dir, 'armory.html'), encoding='utf-8') as armory_file:
            armory_php = armory_file.read()
        quantities = {constants.ARMOURS: 4, constants.HELMETS: 2, constants.GREAVES: 4, constants.BOOTS: 3}

        expected_first_armour = Item(name='Ornat', strength=54, constraints=-1, bonus=181, fire=0, frost=0,
                                     poison=0, ether=0, type=ItemType.armour)
        expected_last_armour = Item(name='Smocza zbroja płytow', strength=104, constraints=-6, bonus=359, fire=0, frost=0, poison=70,
                                    ether=0, type=ItemType.armour)
        expected_first_helmet = Item(name='Goblinska maska z Diamentem', strength=11, constraints=2, bonus=21, fire=39, frost=68,
                                     poison=0, ether=0, type=ItemType.helmet)
        expected_last_helmet = Item(name='Szyszak', strength=122, constraints=-2, bonus=336, fire=0, frost=0, poison=0,
                                    ether=0, type=ItemType.helmet)
        expected_first_greave = Item(name='Filcowe Spodnie', strength=28, constraints=-4, bonus=93,
                                     fire=0, frost=86, poison=0, ether=0, type=ItemType.greave)
        expected_last_greave = Item(name='Złodziejskie nagolennik', strength=76, constraints=1, bonus=240, fire=0, frost=0,
                                    poison=0, ether=0, type=ItemType.greave)
        expected_first_boots = Item(name='Buty z wężowej skóry', strength=18, constraints=-6, bonus=72, fire=0, frost=0,
                                    poison=31, ether=0, type=ItemType.boots)
        expected_last_boots = Item(name='Trupie buty z Diamentem', strength=8, constraints=0, bonus=16, fire=0,
                                   frost=73, poison=19, ether=0, type=ItemType.boots)

        # when
        equipment_in_armory = reader.read_armory(armory_php, quantities)

        # then
        for item in equipment_in_armory:
            self.assertNotIn('span', item.name)
            self.assertIsInstance(item.bonus, int)
            self.assertIsInstance(item.constraints, int)
            self.assertIsInstance(item.strength, int)
            self.assertIsInstance(item.fire, int)
            self.assertIsInstance(item.frost, int)
            self.assertIsInstance(item.poison, int)
            self.assertIsInstance(item.ether, int)
        self.assertEqual(len(equipment_in_armory), 13)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.armour), 4)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.helmet), 2)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.greave), 4)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.boots), 3)
        self.assertIn(expected_first_armour, equipment_in_armory)
        self.assertIn(expected_last_armour, equipment_in_armory)
        self.assertIn(expected_first_helmet, equipment_in_armory)
        self.assertIn(expected_last_helmet, equipment_in_armory)
        self.assertIn(expected_first_greave, equipment_in_armory)
        self.assertIn(expected_last_greave, equipment_in_armory)
        self.assertIn(expected_first_boots, equipment_in_armory)
        self.assertIn(expected_last_boots, equipment_in_armory)

    def _count_items_of_type(self, equipment_in_armory, item_type):
        return len(list(filter(lambda i: i.type is item_type, equipment_in_armory)))
