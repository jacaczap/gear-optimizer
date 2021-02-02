from gear_optimizer import constants

stat_fields = {constants.PLAYER_STRENGTH: 100,
               constants.MIN_CONSTRAINTS: -10}
weapon_fields = {constants.NAME: 'Kama',
                 constants.STRENGTH: 21,
                 constants.CONSTRAINTS: -2}
shield_fields = {constants.NAME: 'Honor',
                 constants.STRENGTH: 74,
                 constants.CONSTRAINTS: -3}
shield_stats_fields = {constants.BONUS: 281,
                       constants.FIRE: 28,
                       constants.FROST: 0,
                       constants.POISON: 0,
                       constants.ETHER: 0}
weight_fields = {constants.BONUS: 1,
                 constants.FIRE: 1 / 4,
                 constants.FROST: 1 / 4,
                 constants.POISON: 1 / 4,
                 constants.ETHER: 1 / 4}
requirements_fields = {constants.BONUS: 0,
                       constants.FIRE: 0,
                       constants.FROST: 0,
                       constants.POISON: 0,
                       constants.ETHER: 0}
file_path = './guild_eq.csv'
