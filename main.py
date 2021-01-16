import gui

FILE_NAME = "E://OneDrive/jacy/i-rpg/guild_eq.csv"
FILE_NAME_LINUX = "./guild_eq.csv"

if __name__ == '__main__':
    # celebrian_strength = 210
    # celebrian_constraints = -13
    # celebrian_weapon = Item(name='kama', strength=21, constraints=-2, bonus=0)
    # celebrian_shield = Item(name='migdalowa', strength=25, constraints=-3, bonus=128)
    # weights = ScoreWeights(bonus=1.0, fire=1 / 4, frost=1 / 4, poison=1 / 4, ether=1 / 4)
    # optimize_gear(celebrian_strength, celebrian_constraints, celebrian_weapon, celebrian_shield, weights)
    app = gui.Application()
    app.start_optimizer_with_gui()
