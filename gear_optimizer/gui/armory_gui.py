import tkinter as tk
import tkinter.filedialog

from armory import armory_service
from constants import BOOTS, GREAVES, HELMETS, ARMOURS
from gui import row_service
from gui.row_service import show_row


class ArmoryGui:
    def __init__(self, root: tk.Tk):
        self.armory_window = tk.Toplevel(root)
        self.armory_window.title("Zbrojownia")
        self.quantities_fields = {ARMOURS: 21, HELMETS: 14, GREAVES: 8, BOOTS: 6}
        self.armory_entry = tk.Entry(self.armory_window)
        self.armory_entry.grid(row=1, column=1)

    def read_armory_to_csv(self):
        tk.Label(self.armory_window, text='Wklej html ze zbrojowni: ').grid(row=1, column=0)
        quantities = show_row('Ilość w zbrojowni: ', self.quantities_fields, 2, self.armory_window)
        tk.Button(self.armory_window, text='Zapisz do csv', command=lambda q=quantities: self._start(q)).grid(row=3,
                                                                                                              column=0,
                                                                                                              sticky=tk.W,
                                                                                                              pady=4)
        tk.Button(self.armory_window, text='Anuluj', command=self.armory_window.destroy).grid(row=3,
                                                                                              column=1,
                                                                                              sticky=tk.W,
                                                                                              pady=4)

    def _start(self, quantities):
        filename = tkinter.filedialog.asksaveasfilename(initialfile='gear', defaultextension='csv')
        armory_html = self.armory_entry.get()
        quantities_dict = row_service.read_int_fields(quantities)
        armory_service.read_php_armory_to_csv(armory_html, filename, quantities_dict)
        self.armory_window.destroy()