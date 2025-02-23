import AstroGUI as gui_module
import AstroQuery as horizons
import AstroSolve as solver_module
import AstroPlot as plotter_module

def main(user_params, horizons_data):
    """
    Main function that initializes the GUI, collects user parameters, retrieves data, runs simulations, and displays results.
    """
    # Run the orbit solver with the user parameters and Horizons data
    orbit_solver = solver_module.AstroSolve(user_params, horizons_data)
    trajectories = orbit_solver.run_simulation()

    return trajectories