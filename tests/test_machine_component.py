
from src.machine_component import MachineComponent

# Creating two machine components
component1 = MachineComponent("Gear")
component2 = MachineComponent("Bolt")

component1.material = "steel"
component2.material = "copper"
# Setting a valid surface area (in square meters)
component1.surface_area = 0.01  # Example: 0.01 m^2
component2.surface_area = 0.02  # Example: 0.01 m^2
# Setting a valid mass (in kilograms)
component1.mass = 5.0  # Example: 5 kg
component2.mass = 3.0  # Example: 5 kg

# Setting volume (in cubic meters) for the components
component1.volume = 0.05  # m^3, example volume
component2.volume = 0.04

# Calculating stiffness based on material and geometry
component1.calculate_stiffness()
# Applying forces and simulating a scenario
component1.apply_force("force_1", (100, 0, 0), (0, 0, 0))
component2.apply_force("force_2", (-100, 0, 0), (0, 0, 0))

# Detecting and resolving collision
if component1.detect_collision(component2):
    component1.resolve_collision(component2)

# Calculating and updating wear
wear_rate = 0.0000001
component1.update_wear(wear_rate)

# Calculating stress and strain
force_applied = 1000  # N
component1.calculate_stress(force_applied)
component1.calculate_strain()

# Simulating vibration
damping_coefficient = 0.05
vibration_response = component1.simulate_vibration_response(force_applied, damping_coefficient)

# Calculating energy
kinetic_energy = component1.calculate_kinetic_energy()
potential_energy = component1.calculate_potential_energy(9.81, 0)
velocity_after_time = component1.calculate_velocity_after_time(1)
# Print some results
print(f"Stress: {component1.stress} N/m²")
print(f"strain: {component1.strain} N/m")
print(f"Collision Detected: {component1.detect_collision(component2)}")
print(f"Vibration Amplitude: {vibration_response}")
print(f"Kinetic Energy: {kinetic_energy} J")
print(f"Potential Energy: {potential_energy} J")
print(f"velocity after time: {velocity_after_time}")
