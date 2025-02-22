# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 00:38:09 2025

@author: Tom W
"""

# Astronaugrapher: Main Driver Script
# Orchestrates the Astronaugrapher suite, handling user input, data retrieval, simulation, and visualization.

import AstroGUI as gui_module
import AstroQuery as horizons
import AstroSolve as solver_module
import AstroPlot as plotter_module


def main():
    """
    Main function that initializes the GUI, collects user parameters, retrieves data, runs simulations, and displays results.
    """
    # Initialize GUI and get user parameters
    gui = gui_module.AstroGUI()
    user_params = gui.get_simulation_parameters()

    # Retrieve Horizons data if requested
    if user_params['use_horizons']:
        horizons_data = horizons.retrieve_data(
            user_params['bodies'],
            EPHEM_TYPE=user_params['ephem_type'],
            CENTER=user_params['center'],
            START_TIME=user_params['start_date'],
            #STOP_TIME=user_params['end_date'],
            STEP_SIZE=f"{user_params['step_size']} s",
            OUT_UNITS=user_params['out_units'],
            VEC_TABLE=user_params['vec_table'],
            REF_PLANE=user_params['ref_plane'],
            REF_SYSTEM=user_params['ref_system'],
            VEC_CORR=user_params['vec_corr'],
            ANG_FORMAT=user_params['ang_format'],
            CSV_FORMAT=user_params['csv_format'],
            OBJ_DATA=user_params['obj_data']
        )
    else:
        horizons_data = None

    # Run the orbit solver with the user parameters and Horizons data
    orbit_solver = solver_module.AstroSolve(user_params, horizons_data)
    trajectories = orbit_solver.run_simulation()

    # Plot the results within the GUI
    plotter = plotter_module.AstroPlot(gui.root)
    plotter.plot_trajectories(trajectories, user_params['bodies'])

    # Finalize GUI operations
    gui.root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
