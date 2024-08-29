# quantum_tunneling_simulation.py
import numpy as np
from quantum_trajectory_simulator import QuantumTrajectorySimulator
from machine_component import MachineComponent

# Create a MachineComponent instance representing a quantum particle
particle = MachineComponent("quantum_tunneling_particle")
particle.mass = 1.0  # Mass of the particle
particle.position = (-1, 0, 0)  # Start left of a potential barrier
particle.velocity = (0.2, 0, 0)  # Initial velocity towards the barrier

# Set up the QuantumTrajectorySimulator
simulator = QuantumTrajectorySimulator(particle, temperature=0.5, time_interval=0.1)

# Define a potential barrier
barrier_position = 0  # Barrier at x=0
barrier_height = 1.5  # Height of the barrier

# Modify the cost function to simulate tunneling through the barrier
def evaluate_trajectory_with_tunneling(trajectory):
    total_cost = 0
    for position, velocity in trajectory:
        potential_energy = barrier_height if position[0] >= barrier_position else 0
        kinetic_energy = 0.5 * particle.mass * sum(v ** 2 for v in velocity)
        total_energy = kinetic_energy + potential_energy

        # Probability amplitude decays as the particle crosses the barrier
        if position[0] >= barrier_position:
            probability_amplitude = np.exp(-total_energy / barrier_height)
        else:
            probability_amplitude = np.exp(-total_energy / (2 * barrier_height))

        total_cost += -probability_amplitude

    return total_cost

# Inject the custom cost function into the simulator
simulator.evaluate_trajectory = evaluate_trajectory_with_tunneling

# Run the simulation
optimal_trajectory = simulator.run_simulation(iterations=500)

# Visualize the trajectory
simulator.visualize_trajectory(optimal_trajectory)
