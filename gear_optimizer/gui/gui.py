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

Input = namedtuple('Input', ['stats', 'weapon', 'shield', 'shield_stats', 'weights', 'requirements', 'filename'])


class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.filename_entry = tk.Entry(self.root)
        self._load_initial_input()

    def start_optimizer_with_gui(self):
        stats = self._show_row('Statystyki -', self.stat_fields, 1)
        weapon = self._show_row('Broń -', self.weapon_fields, 2)
        shield = self._show_row('Tarcza -', self.shield_fields, 3)
        shield_stats = self._show_row('Tarcza -', self.shield_stats_fields, 4)
        weights = self._show_row('Wagi -', self.weight_fields, 5)
        requirements = self._show_row('Wymagania -', self.requirements, 6)
        self._filename_row(7)

        user_input_fields = Input(stats, weapon, shield, shield_stats, weights, requirements, self.filename)

        tk.Button(self.root, text='Start', command=lambda i=user_input_fields: self._process_input(i)).grid(row=9,
                                                                                                            column=0,
                                                                                                            sticky=tk.W,
                                                                                                            pady=4)
        tk.Button(self.root, text='Wyjście', command=self.root.quit).grid(row=9,
                                                                          column=1,
                                                                          sticky=tk.W,
                                                                          pady=4)
        self.root.mainloop()

    def _show_row(self, title, fields, row_number):
        entries = {}
        column = 1
        tk.Label(self.root, text=title).grid(row=row_number)

        for field in fields:
            entry = tk.Entry(self.root)
            tk.Label(self.root, text=f'{field}:').grid(row=row_number, column=column)
            entry.grid(row=row_number, column=column + 1)
            entry.insert(0, fields[field])
            entries[field] = entry
            column += 2
        return entries

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
        self._show_output(optimized_gear)

    def _read_user_input_values(self, user_input_fields: Input) -> Input:
        stats = self._read_fields(user_input_fields.stats)
        weapon = self._read_fields(user_input_fields.weapon)
        shield = self._read_fields(user_input_fields.shield)
        shield_stats = self._read_fields(user_input_fields.shield_stats)
        weights = self._read_fields(user_input_fields.weights)
        requirements = self._read_fields(user_input_fields.requirements)
        return Input(stats, weapon, shield, shield_stats, weights, requirements, user_input_fields.filename)

    def _read_fields(self, user_input_fields):
        values = {}
        for field in user_input_fields:
            values[field] = user_input_fields[field].get()
        return values

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
        self.stat_fields = {gear_optimizer.constants.PLAYER_STRENGTH: 100, gear_optimizer.constants.MIN_CONSTRAINTS: -10}
        self.weapon_fields = {gear_optimizer.constants.NAME: 'Kama', gear_optimizer.constants.STRENGTH: 21, gear_optimizer.constants.CONSTRAINTS: -2}
        self.shield_fields = {gear_optimizer.constants.NAME: 'Honor', gear_optimizer.constants.STRENGTH: 74, gear_optimizer.constants.CONSTRAINTS: -3}
        self.shield_stats_fields = {gear_optimizer.constants.BONUS: 281, gear_optimizer.constants.FIRE: 28, gear_optimizer.constants.FROST: 0, gear_optimizer.constants.POISON: 0, gear_optimizer.constants.ETHER: 0}
        self.weight_fields = {gear_optimizer.constants.BONUS: 1, gear_optimizer.constants.FIRE: 1 / 4, gear_optimizer.constants.FROST: 1 / 4, gear_optimizer.constants.POISON: 1 / 4, gear_optimizer.constants.ETHER: 1 / 4}
        self.requirements = {gear_optimizer.constants.BONUS: 0, gear_optimizer.constants.FIRE: 0, gear_optimizer.constants.FROST: 0, gear_optimizer.constants.POISON: 0, gear_optimizer.constants.ETHER: 0}
        self.filename = './guild_eq.csv'

    def _save_user_input(self, user_input: Input):
        with open(INPUT_PICKLE_FILE, 'wb') as last_input_file:
            pickle.dump(user_input, last_input_file)

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
