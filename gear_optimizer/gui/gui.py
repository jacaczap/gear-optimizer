import os
import pickle
import tkinter as tk
import tkinter.filedialog
from collections import namedtuple

import gear_optimizer.constants
from gear_optimizer.constants import INPUT_PICKLE_FILE
from gear_optimizer.model import GearWithStats
from gear_optimizer.optimizer import optimizer
from gear_optimizer.gui import gear_printer
from gear_optimizer.gui.armory_gui import ArmoryGui
from gear_optimizer.gui import row_service

Input = namedtuple('Input', ['stats', 'weapon', 'shield', 'shield_stats', 'weights', 'requirements', 'filename'])


class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gear Optimizer")
        self.filename_entry = tk.Entry(self.root)
        self._load_initial_input()

    def start_optimizer_with_gui(self):
        stats = row_service.show_row('Statystyki -', self.stat_fields, 1, self.root)
        weapon = row_service.show_row('Broń -', self.weapon_fields, 2, self.root)
        shield = row_service.show_row('Tarcza -', self.shield_fields, 3, self.root)
        shield_stats = row_service.show_row('Tarcza -', self.shield_stats_fields, 4, self.root)
        weights = row_service.show_row('Wagi -', self.weight_fields, 5, self.root)
        requirements = row_service.show_row('Wymagania -', self.requirements, 6, self.root)
        self._filename_row(7)

        user_input_fields = Input(stats, weapon, shield, shield_stats, weights, requirements, self.filename)

        tk.Button(self.root, text='Start', command=lambda i=user_input_fields: self._process_input(i)).grid(row=9,
                                                                                                            column=0,
                                                                                                            sticky=tk.W,
                                                                                                            pady=4)
        tk.Button(self.root, text='Odczytaj uzbrojenie do pliku',
                  command=self._open_armory_gui).grid(row=9,
                                                      column=1,
                                                      sticky=tk.W,
                                                      pady=4)
        tk.Button(self.root, text='Wyjście', command=self.root.quit).grid(row=9,
                                                                          column=2,
                                                                          sticky=tk.W,
                                                                          pady=4)
        self.root.mainloop()

    def _filename_row(self, row_number):
        tk.Label(self.root, text="Plik z wyposażeniem:").grid(row=row_number)
        self.filename_entry.grid(row=row_number, column=2)
        self.filename_entry.insert(0, self.filename)

        tk.Button(self.root, text='Wybierz', command=self._set_filename_from_dialog).grid(row=row_number,
                                                                                          column=3,
                                                                                          sticky=tk.W,
                                                                                          pady=4)

    def _set_filename_from_dialog(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.filename_entry.insert(0, self.filename)

    def _process_input(self, user_input_fields: Input):
        user_input_values = self._read_user_input_values(user_input_fields)
        self._save_user_input(user_input_values)
        optimized_gear = optimizer.optimize_gear(user_input_values)
        optimized_gear.reverse()
        self._show_output(optimized_gear)

    def _read_user_input_values(self, user_input_fields: Input) -> Input:
        stats = row_service.read_int_fields(user_input_fields.stats)
        weapon = row_service.read_fields(user_input_fields.weapon)
        shield = row_service.read_fields(user_input_fields.shield)
        shield_stats = row_service.read_fields(user_input_fields.shield_stats)
        weights = row_service.read_fields(user_input_fields.weights)
        requirements = row_service.read_fields(user_input_fields.requirements)
        return Input(stats, weapon, shield, shield_stats, weights, requirements, user_input_fields.filename)

    def _load_initial_input(self):
        if os.path.exists(INPUT_PICKLE_FILE):
            self._load_last_input_from_pickle()
        else:
            self._load_default_input()

    def _load_last_input_from_pickle(self):
        with open(INPUT_PICKLE_FILE, 'rb') as last_input_file:
            last_input: Input = pickle.load(last_input_file)
        self.stat_fields = last_input.stats
        self.weapon_fields = last_input.weapon
        self.shield_fields = last_input.shield
        self.shield_stats_fields = last_input.shield_stats
        self.weight_fields = last_input.weights
        self.requirements = last_input.requirements
        self.filename = last_input.filename

    def _load_default_input(self):
        self.stat_fields = {gear_optimizer.constants.PLAYER_STRENGTH: 100,
                            gear_optimizer.constants.MIN_CONSTRAINTS: -10}
        self.weapon_fields = {gear_optimizer.constants.NAME: 'Kama', gear_optimizer.constants.STRENGTH: 21,
                              gear_optimizer.constants.CONSTRAINTS: -2}
        self.shield_fields = {gear_optimizer.constants.NAME: 'Honor', gear_optimizer.constants.STRENGTH: 74,
                              gear_optimizer.constants.CONSTRAINTS: -3}
        self.shield_stats_fields = {gear_optimizer.constants.BONUS: 281, gear_optimizer.constants.FIRE: 28,
                                    gear_optimizer.constants.FROST: 0, gear_optimizer.constants.POISON: 0,
                                    gear_optimizer.constants.ETHER: 0}
        self.weight_fields = {gear_optimizer.constants.BONUS: 1, gear_optimizer.constants.FIRE: 1 / 4,
                              gear_optimizer.constants.FROST: 1 / 4, gear_optimizer.constants.POISON: 1 / 4,
                              gear_optimizer.constants.ETHER: 1 / 4}
        self.requirements = {gear_optimizer.constants.BONUS: 0, gear_optimizer.constants.FIRE: 0,
                             gear_optimizer.constants.FROST: 0, gear_optimizer.constants.POISON: 0,
                             gear_optimizer.constants.ETHER: 0}
        self.filename = './guild_eq.csv'

    def _save_user_input(self, user_input: Input):
        with open(INPUT_PICKLE_FILE, 'wb') as last_input_file:
            pickle.dump(user_input, last_input_file)

    def _open_armory_gui(self):
        armory_gui = ArmoryGui(self.root)
        armory_gui.read_armory_to_csv()

    def _show_output(self, gears_with_stats: list[GearWithStats]):
        output_window = tk.Toplevel(self.root)
        output_window.title("Wyniki")
        scroll_y = tk.Scrollbar(output_window)
        scroll_x = tk.Scrollbar(output_window, orient=tk.HORIZONTAL)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        output_field = tk.Text(output_window, wrap="none", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        scroll_y.config(command=output_field.yview)
        scroll_x.config(command=output_field.xview)
        output_field.pack(side=tk.LEFT, fill=tk.BOTH)
        gear_results = gear_printer.get_gears_as_string(gears_with_stats)
        output_field.insert(tk.END, gear_results)
