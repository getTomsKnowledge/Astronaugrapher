"""
@project: Astronaugrapher
@author: Tom W and ChatGPT
@date: 02/21/2025
@summary: MatPlotLib plotting of AstroSolve trajectories.
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AstroPlot:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame

    def plot_trajectories(self, trajectories, body_names):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i, name in enumerate(body_names):
            traj = trajectories[:, i, :]
            ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], label=name)
        ax.legend()
        self._embed_plot(fig)

    def _embed_plot(self, fig):
        for widget in self.parent_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, self.parent_frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()