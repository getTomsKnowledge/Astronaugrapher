import numpy as np
from AstroCONST import AstroCONST

class AstroSolve:
    def __init__(self, user_params, horizons_data=None):
        self.bodies = user_params['bodies']
        self.step_size = float(user_params['step_size'])
        self.num_steps = int(user_params['run_time'] / self.step_size)
        self.positions, self.velocities, self.mu = self.initialize_states(horizons_data)
        self.time_array = np.linspace(0, user_params['run_time'], self.num_steps + 1, dtype=np.float64)

    def initialize_states(self, horizons_data):
        positions, velocities, mu = [], [], []
        for body in self.bodies:
            mu_value = AstroCONST.get_gravitational_parameter(body)
            mu.append(mu_value)
            positions.append(horizons_data.get(body, {}).get('positions', [[0.0, 0.0, 0.0]])[0])
            velocities.append(horizons_data.get(body, {}).get('velocities', [[0.0, 0.0, 0.0]])[0])
        return np.array(positions, dtype=np.float64), np.array(velocities, dtype=np.float64), np.array(mu, dtype=np.float64)

    def compute_accelerations(self, positions):
        acc = np.zeros_like(positions, dtype=np.float64)
        for i, pos_i in enumerate(positions):
            for j, pos_j in enumerate(positions):
                if i != j:
                    diff = pos_j - pos_i
                    norm = np.linalg.norm(diff)
                    if norm > 1e-12:
                        acc[i] += self.mu[j] * diff / (norm**3)
        return acc

    def run_simulation(self):
        trajectories = np.zeros((self.num_steps + 1, len(self.bodies), 3), dtype=np.float64)
        trajectories[0] = self.positions
        for step in range(1, self.num_steps + 1):
            acc = self.compute_accelerations(self.positions)
            self.velocities += 0.5 * acc * self.step_size
            self.positions += self.velocities * self.step_size
            acc = self.compute_accelerations(self.positions)
            self.velocities += 0.5 * acc * self.step_size
            trajectories[step] = self.positions
        return trajectories