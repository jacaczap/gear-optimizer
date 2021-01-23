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
        quantities = {constants.ARMOURS: 21, constants.HELMETS: 14, constants.GREAVES: 8, constants.BOOTS: 6}

        expected_first_armour = Item(name='Ciężka kolczuga', strength=162, constraints=-8, bonus=470, fire=0, frost=0,
                                     poison=0, ether=0, type=ItemType.armour)
        expected_last_armour = Item(name='Łachman', strength=3, constraints=-1, bonus=9, fire=0, frost=0, poison=0,
                                    ether=0, type=ItemType.armour)
        expected_first_helmet = Item(name='Czarny diadem', strength=51, constraints=-2, bonus=212, fire=0, frost=0,
                                     poison=20, ether=78, type=ItemType.helmet)
        expected_last_helmet = Item(name='Wilczy hełm', strength=4, constraints=-2, bonus=33, fire=0, frost=0, poison=0,
                                    ether=0, type=ItemType.helmet)
        expected_first_greave = Item(name='Lekkie nagolenice z Diamentem', strength=99, constraints=-3, bonus=454,
                                     fire=0, frost=49, poison=0, ether=0, type=ItemType.greave)
        expected_last_greave = Item(name='Żelazne nagolenice', strength=92, constraints=-4, bonus=392, fire=0, frost=0,
                                    poison=0, ether=0, type=ItemType.greave)
        expected_first_boots = Item(name='Bojowe kozaki', strength=117, constraints=-4, bonus=537, fire=0, frost=0,
                                    poison=0, ether=0, type=ItemType.boots)
        expected_last_boots = Item(name='Wygodne buty z Diamentem', strength=118, constraints=-2, bonus=643, fire=0,
                                   frost=0, poison=0, ether=0, type=ItemType.boots)

        # when
        equipment_in_armory = reader.read_armory(armory_php, quantities)

        # then
        for item in equipment_in_armory:
            print(item)
            self.assertNotIn('span', item.name)
            self.assertIsInstance(item.bonus, int)
            self.assertIsInstance(item.constraints, int)
            self.assertIsInstance(item.strength, int)
            self.assertIsInstance(item.fire, int)
            self.assertIsInstance(item.frost, int)
            self.assertIsInstance(item.poison, int)
            self.assertIsInstance(item.ether, int)
        self.assertEqual(len(equipment_in_armory), 49)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.armour), 21)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.helmet), 14)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.greave), 8)
        self.assertEqual(self._count_items_of_type(equipment_in_armory, ItemType.boots), 6)
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
