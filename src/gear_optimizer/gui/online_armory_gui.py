import tkinter as tk
import tkinter.filedialog

from gear_optimizer.armory import armory_service


class OnlineArmoryGui:
    def __init__(self, root: tk.Tk):
        self.armory_window = tk.Toplevel(root)
        self.armory_window.title("Zbrojownia online")
        self.session_identifier = tk.Entry(self.armory_window)
        self.session_identifier.grid(row=1, column=1)

    def read_armory_to_csv(self):
        tk.Label(self.armory_window, text='Wklej identyfikator sesji: ').grid(row=1, column=0)
        tk.Button(self.armory_window, text='Zapisz do csv', command=self._start).grid(row=3,
                                                                                      column=0,
                                                                                      sticky=tk.W,
                                                                                      pady=4)
        tk.Button(self.armory_window, text='Anuluj', command=self.armory_window.destroy).grid(row=3,
                                                                                              column=1,
                                                                                              sticky=tk.W,
                                                                                              pady=4)

    def _start(self):
        filename = tkinter.filedialog.asksaveasfilename(initialfile='guild_eq', defaultextension='csv')
        session_identifier = self.session_identifier.get()
        armory_service.read_online_armory_to_csv(session_identifier, filename)
        self.armory_window.destroy()
