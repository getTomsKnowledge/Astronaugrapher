"""
@project: Astronaugrapher
@author: Tom W and ChatGPT
@date: 02/21/2025
@description: Prompt user/take input, pass to other modules, 
display trajectory plot to user.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class AstroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Astronaugrapher")
        self.params = self.initialize_default_params()
        self._build_interface()

    def initialize_default_params(self):
        return {
            'use_horizons': tk.BooleanVar(value=True),
            'bodies': tk.StringVar(value="Sun, Earth, Mars"),
            'ephem_type': tk.StringVar(value="VECTORS"),
            'center': tk.StringVar(value="500@0"),
            'start_date': tk.StringVar(value="2025-01-01"),
            'end_date': tk.StringVar(value="2025-12-31"),
            'step_size': tk.DoubleVar(value=3600.0),
            'out_units': tk.StringVar(value="KM-S"),
            'vec_table': tk.StringVar(value="3"),
            'ref_plane': tk.StringVar(value="ECLIPTIC"),
            'ref_system': tk.StringVar(value="J2000"),
            'vec_corr': tk.StringVar(value="NONE"),
            'ang_format': tk.StringVar(value="DEG"),
            'csv_format': tk.StringVar(value="YES"),
            'obj_data': tk.StringVar(value="NO"),
        }

    def _build_interface(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        row = 0
        for label, var in self.params.items():
            ttk.Label(frame, text=label.replace('_', ' ').title() + ":").grid(row=row, column=0, sticky=tk.W)
            ttk.Entry(frame, textvariable=var).grid(row=row, column=1, sticky=tk.E)
            row += 1

        ttk.Button(frame, text="Submit", command=self._submit).grid(row=row, column=0, pady=10)
        ttk.Button(frame, text="Exit", command=self.root.quit).grid(row=row, column=1, pady=10)

    def _submit(self):
        try:
            datetime.strptime(self.params['start_date'].get(), "%Y-%m-%d")
            datetime.strptime(self.params['end_date'].get(), "%Y-%m-%d")
            self.root.quit()
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format.")

    def get_simulation_parameters(self):
        self.root.mainloop()
        params = {key: var.get() for key, var in self.params.items()}
        params['bodies'] = [body.strip() for body in params['bodies'].split(',')]
        params['run_time'] = (datetime.strptime(params['end_date'], "%Y-%m-%d") - datetime.strptime(params['start_date'], "%Y-%m-%d")).total_seconds()
        return params
