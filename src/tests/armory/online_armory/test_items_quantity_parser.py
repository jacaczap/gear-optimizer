import os
from unittest import TestCase

from gear_optimizer.armory.online_armory import items_quantity_parser


class Test(TestCase):
    def test_parse_armory_room_file(self):
        # given
        this_test_dir = os.path.dirname(__file__)
        with open(os.path.join(this_test_dir, 'armory_room.html'), encoding='utf-8') as armory_file:
            armory_php = armory_file.read()

        expected = {"Zbroje": 4, "Hełmy": 2, "Nagole": 4, "Buty": 3}

        # when
        result = items_quantity_parser.parse_armory_room_file(armory_php)

        # then
        self.assertEqual(expected, result)
