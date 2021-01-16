import tkinter as tk
import tkinter.filedialog
from collections import namedtuple

import optimizer
import user_input_keywords as kw
from model.item import Item
from model.requirements import Requirements
from model.score_weights import ScoreWeights

Input = namedtuple('Input', ['stats', 'weapon', 'shield', 'shield_stats', 'weights', 'requirements', 'filename'])


class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.filename_entry = tk.Entry(self.root)
        self.stat_fields = {kw.PLAYER_STRENGTH: 100, kw.MIN_CONSTRAINTS: -10}
        self.weapon_fields = {kw.NAME: 'Kama', kw.STRENGTH: 21, kw.CONSTRAINTS: -2}
        self.shield_fields = {kw.NAME: 'Honor', kw.STRENGTH: 74, kw.CONSTRAINTS: -3}
        self.shield_fields2 = {kw.BONUS: 281, kw.FIRE: 28, kw.FROST: 0, kw.POISON: 0, kw.ETHER: 0}
        self.weight_fields = {kw.BONUS: 1, kw.FIRE: 1 / 4, kw.FROST: 1 / 4, kw.POISON: 1 / 4, kw.ETHER: 1 / 4}
        self.requirements = {kw.BONUS: 0, kw.FIRE: 0, kw.FROST: 0, kw.POISON: 0, kw.ETHER: 0}
        self.filename = './guild_eq.csv'

    def start_optimizer_with_gui(self):
        stats = self._show_row('Statystyki -', self.stat_fields, 1)
        weapon = self._show_row('Broń -', self.weapon_fields, 2)
        shield = self._show_row('Tarcza -', self.shield_fields, 3)
        shield_stats = self._show_row('Tarcza -', self.shield_fields2, 4)
        weights = self._show_row('Wagi -', self.weight_fields, 5)
        requirements = self._show_row('Wymagania -', self.requirements, 6)
        self._filename_row(7)

        user_input = Input(stats, weapon, shield, shield_stats, weights, requirements, self.filename)

        tk.Button(self.root, text='Start', command=lambda i=user_input: self._process_input(i)).grid(row=9,
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

    def _process_input(self, user_input: Input):
        optimized_gear = optimizer.optimize_gear(user_input)
