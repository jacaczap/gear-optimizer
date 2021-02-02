import os
import pickle
import tkinter as tk
import tkinter.filedialog

from gear_optimizer.constants import INPUT_PICKLE_FILE
from gear_optimizer.gui import defaults
from gear_optimizer.gui import row_service
from gear_optimizer.gui.offline_armory_gui import OfflineArmoryGui
from gear_optimizer.gui.online_armory_gui import OnlineArmoryGui
from gear_optimizer.gui.output_displayer import _show_output
from gear_optimizer.model import UserInput
from gear_optimizer.optimizer import optimizer


class Application:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gear Optimizer")
        self._load_initial_input()
        self._prepare_window()

    def start_optimizer_with_gui(self):
        self.root.mainloop()

    def _prepare_window(self):
        self.stats_entry = row_service.show_row('Statystyki -', self.stat_fields, 1, self.root)
        self.weapon_entry = row_service.show_row('Broń -', self.weapon_fields, 2, self.root)
        self.shield_entry = row_service.show_row('Tarcza -', self.shield_fields, 3, self.root)
        self.shield_stats_entry = row_service.show_row('Tarcza -', self.shield_stats_fields, 4, self.root)
        self.weights_entry = row_service.show_row('Wagi -', self.weight_fields, 5, self.root)
        self.requirements_entry = row_service.show_row('Wymagania -', self.requirements_fields, 6, self.root)

        self._prepare_button(text='Start', command=self._optimize_gear, row=8, column=0)
        self._prepare_button(text='Odczytaj uzbrojenie\ndo pliku offline', command=self._open_offline_armory_gui, row=8,
                             column=1)
        self._prepare_button(text='Odczytaj uzbrojenie\ndo pliku online', command=self._open_online_armory_gui, row=8,
                             column=2)
        self._prepare_button(text='Wyjście', command=self.root.quit, row=8, column=5)

    def _prepare_button(self, text, command, row, column):
        tk.Button(self.root, text=text, command=command).grid(row=row,
                                                              column=column,
                                                              sticky=tk.W,
                                                              pady=4)

    def _load_initial_input(self):
        if os.path.exists(INPUT_PICKLE_FILE):
            self._load_last_input_from_pickle()
        else:
            self._load_default_input()

    def _load_last_input_from_pickle(self):
        with open(INPUT_PICKLE_FILE, 'rb') as last_input_file:
            last_input: UserInput = pickle.load(last_input_file)
        self.stat_fields = last_input.stats
        self.weapon_fields = last_input.weapon
        self.shield_fields = last_input.shield
        self.shield_stats_fields = last_input.shield_stats
        self.weight_fields = last_input.weights
        self.requirements_fields = last_input.requirements
        self.file_path = last_input.filename

    def _load_default_input(self):
        self.stat_fields = defaults.stat_fields
        self.weapon_fields = defaults.weapon_fields
        self.shield_fields = defaults.shield_fields
        self.shield_stats_fields = defaults.shield_stats_fields
        self.weight_fields = defaults.weight_fields
        self.requirements_fields = defaults.requirements_fields
        self.file_path = defaults.file_path

    def _optimize_gear(self):
        self.file_path = tkinter.filedialog.askopenfilename(initialdir=os.path.dirname(self.file_path),
                                                            initialfile=os.path.basename(self.file_path),
                                                            filetypes=[('CSV', '.csv')])
        if not self.file_path:
            return
        user_input_values = self._read_user_input_values()
        self._save_user_input(user_input_values)
        optimized_gear = optimizer.optimize_gear(user_input_values)
        _show_output(self.root, optimized_gear)

    def _read_user_input_values(self) -> UserInput:
        stats = row_service.read_int_fields(self.stats_entry)
        weapon = row_service.read_fields(self.weapon_entry)
        shield = row_service.read_fields(self.shield_entry)
        shield_stats = row_service.read_fields(self.shield_stats_entry)
        weights = row_service.read_fields(self.weights_entry)
        requirements = row_service.read_fields(self.requirements_entry)
        return UserInput(stats, weapon, shield, shield_stats, weights, requirements, self.file_path)

    def _save_user_input(self, user_input: UserInput):
        with open(INPUT_PICKLE_FILE, 'wb') as last_input_file:
            pickle.dump(user_input, last_input_file)

    def _open_offline_armory_gui(self):
        armory_gui = OfflineArmoryGui(self.root)
        armory_gui.read_armory_to_csv()

    def _open_online_armory_gui(self):
        armory_gui = OnlineArmoryGui(self.root)
        armory_gui.read_armory_to_csv()
