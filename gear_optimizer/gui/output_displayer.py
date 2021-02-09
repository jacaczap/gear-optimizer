import tkinter as tk
from typing import List

from gear_optimizer.gui import gear_printer
from gear_optimizer.model import GearWithStats


def _show_output(root, gears_with_stats: List[GearWithStats]):
    output_window = tk.Toplevel(root)
    output_window.title("Wyniki")
    scroll_y = tk.Scrollbar(output_window)
    scroll_x = tk.Scrollbar(output_window, orient=tk.HORIZONTAL)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
    output_field = tk.Text(output_window, wrap="none", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    scroll_y.config(command=output_field.yview)
    scroll_x.config(command=output_field.xview)
    output_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
    gear_results = gear_printer.get_gears_as_string(gears_with_stats)
    output_field.insert(tk.END, gear_results)
