# trajectory_simulator.py may be applicable to quantum particle displacement simulation.

import numpy as np
from dynamics import Dynamics
from mcmc import MetropolisAlgorithm
from machine_component import MachineComponent

class ComponentTrajectorySimulator:
    def __init__(self, component, temperature=1.0, time_interval=1.0):
        self.component = component
        self.time_interval = time_interval
        self.metropolis = MetropolisAlgorithm(component, temperature=temperature)

    def propose_new_trajectory(self, perturbation_factors):
        """ Propose a new trajectory by perturbing position and velocity. """
        proposed_trajectory = []
        current_component = self.component

        for t in range(int(10 / self.time_interval)):  # Simulate for 10 seconds
            # Perturb position and velocity
            position_perturbation = np.random.normal(0, perturbation_factors["position"], size=3)
            velocity_perturbation = np.random.normal(0, perturbation_factors["velocity"], size=3)

            new_position = tuple(p + perturbation for p, perturbation in zip(current_component.position, position_perturbation))
            new_velocity = tuple(v + perturbation for v, perturbation in zip(current_component.velocity, velocity_perturbation))

            current_component.position = new_position
            current_component.velocity = new_velocity

            # Update dynamics for the new state
            Dynamics.update_velocity(current_component, self.time_interval)
            Dynamics.update_position(current_component, self.time_interval)
            Dynamics.calculate_torque(current_component)

            proposed_trajectory.append((new_position, new_velocity))

        return proposed_trajectory

    def evaluate_trajectory(self, trajectory):
        """ Evaluate the trajectory based on energy consumption, distance to obstacles, etc. """
        total_energy = 0
        for position, velocity in trajectory:
            kinetic_energy = 0.5 * self.component.mass * sum(v ** 2 for v in velocity)
            potential_energy = self.component.mass * 9.8 * position[2]
            total_energy += kinetic_energy + potential_energy

        # Example: penalize high energy consumption and deviations from desired position
        return total_energy

    def run_simulation(self, iterations=1000, perturbation_factors=None):
        if perturbation_factors is None:
            perturbation_factors = {"position": 10, "velocity": 0.1}

        best_trajectory = self.propose_new_trajectory(perturbation_factors)
        best_cost = self.evaluate_trajectory(best_trajectory)

        for i in range(iterations):
            new_trajectory = self.propose_new_trajectory(perturbation_factors)
            new_cost = self.evaluate_trajectory(new_trajectory)

            acceptance_prob = self.metropolis.acceptance_probability(best_cost, new_cost)
            if np.random.uniform(0, 1) < acceptance_prob:
                best_trajectory = new_trajectory
                best_cost = new_cost
                print(f"Iteration {i}: Accepted new trajectory with cost {best_cost}")
            else:
                print(f"Iteration {i}: Rejected new trajectory with cost {new_cost}")

        return best_trajectory

    def visualize_trajectory(self, trajectory):
        """ Optional: Visualize the trajectory using matplotlib or another visualization tool. """
        import matplotlib.pyplot as plt

        positions = np.array([pos for pos, vel in trajectory])
        plt.plot(positions[:, 0], positions[:, 1], label='Trajectory')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Component Trajectory')
        plt.legend()
        plt.show()

# Example usage:

if __name__ == "__main__":
    component = MachineComponent("robotic_arm")
    component.mass = 50.0  # kg
    component.position = (10, 0, 0)  # Starting at origin
    component.velocity = (1, 0, 0)  # Initial velocity along the x-axis

    simulator = ComponentTrajectorySimulator(component, temperature=1.0, time_interval=1)
    optimal_trajectory = simulator.run_simulation(iterations=500)

    simulator.visualize_trajectory(optimal_trajectory)
