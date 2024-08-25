import numpy as np
import time
import threading
from MaterialOptimizerGA import MaterialOptimizerGA
from library import material_lib, market_library

class MachineComponent:
    def __init__(self, name):
        self.name = name
        self.cost = 0  # Cost per unit
        self.mass = 0  # kg.
        self.position = (0, 0, 0)  # 3D coordinates (x, y, z) in meters
        self.velocity = (0, 0, 0)  # m/s of the center of mass
        self.forces = {}  # dictionary of forces applied on the component
        self.acceleration = (0, 0, 0)  # m/s^2 of the center of mass
        self.volume = 0 # in m^3
        self.momentum = (0, 0, 0)  # kg*m/s of the center of mass
        self.temperature = 25.0  # Initial temperature in Celsius
        self.pressure = 101.3  # Initial pressure in kPa
        self.vibration_intensity = 0.0
        self.temperature_sensor = []
        self.pressure_sensor = []
        self.vibration_sensor = []
        self.force_sensor = []
        self.rotation_speed_sensor = []
        self.current_sensor = []
        self.surface_area = 0  # main cross_sectional_area of the component
        self.stress = 0
        self.strain = 0
        self.wear = 0
        self.material = None
        self.friction = 0  # Friction coefficient
        self.cycles = 1e6   # Number of cycles for fatigue analysis
        self.material_properties = {"density": 0, "resistance": 0, "wear": 0, "friction": 0} # dictionary of proprerties from the component material
        self.simulation_active = False  # Flag to control the sensor threads
        self.mesh = None  # Mesh data for visualization

    def set_mesh(self, mesh):
        self.mesh = mesh

    def simulate_temperature(self):
        base_temp = 50  # Base temperature in Celsius
        while self.simulation_active:
            # Adjust base temperature with friction-induced heat (example)
            friction_heat = sum([np.linalg.norm(force["vector"]) for force in self.forces.values()]) * 0.001
            temp = base_temp + friction_heat + np.random.normal(0, 2)  # Add noise to simulate real data
            self.temperature_sensor.append(temp)
            time.sleep(1)  # Simulate real-time delay

    def simulate_pressure(self):
        base_pressure = 101.3  # Base pressure in kPa
        while self.simulation_active:
            applied_force = np.linalg.norm(self.calculate_net_force())
            if self.surface_area > 0:
                pressure = base_pressure + (applied_force / self.surface_area) + np.random.normal(0, 0.05)
            else:
                pressure = base_pressure + np.random.normal(0, 0.05)
            self.pressure_sensor.append(pressure)
            time.sleep(1)

    def simulate_vibration(self):
        while self.simulation_active:
            # Adjust vibration based on applied forces (simple harmonic response)
            vibration = self.simulate_vibration_response(np.linalg.norm(self.calculate_net_force()), 0.1) 
            vibration_with_noise = max(vibration + np.random.normal(0, 0.05), 0)
            self.vibration_sensor.append(vibration_with_noise)
            time.sleep(1)

    def start_sensors(self):
        self.simulation_active = True
        threading.Thread(target=self.simulate_temperature).start()
        threading.Thread(target=self.simulate_pressure).start()
        threading.Thread(target=self.simulate_vibration).start()

    def stop_sensors(self):
        self.simulation_active = False

    def calculate_net_force(self):
        """Calculates the sum of all forces acting on the component."""
        net_force = [0, 0, 0]  # Reset net force
        for force_data in self.forces.values():
            net_force = [net_force[i] + force_data["vector"][i] for i in range(3)]
        return net_force
    
    def simulate_vibration_response(self, force, damping_coefficient):
        omega_n = self.calculate_natural_frequency()
        # Calculate amplitude and ensure it's non-negative
        try:
            amplitude = force / (self.mass * max(((omega_n ** 2) - damping_coefficient ** 2), 1e-6))
        except ZeroDivisionError:
            amplitude = 0  # Handle division by zero cases

        # Add noise and ensure non-negative amplitude
        amplitude = max(amplitude + np.random.normal(0, 0.01), 0)
        return amplitude

    def calculate_natural_frequency(self):
        if self.mass == 0:
            raise ValueError("Mass is zero. Please set a valid mass before calculating the natural frequency.")
        stiffness = 200000  # Example stiffness, in N/m
        natural_frequency = (1 / (2 * np.pi)) * ((stiffness / self.mass) ** 0.5)
        return natural_frequency

    def apply_force(self, name, force_vector, contact_point, duration):
        """
        Applies a force to the component for a specific duration.

        Args:
            name (str): A unique identifier for the force.
            force_vector (tuple): The force vector (fx, fy, fz) in Newtons.
            contact_point (tuple): The point of force application (x, y, z) in meters, relative to the component's origin.
            duration (int): The duration for which the force is applied (in time units, s.i., seconds).
        """
        if name in self.forces:
            # Handle existing forces (e.g., update duration, modify vector)
            self.forces[name]["duration"] = duration
        else:
            self.forces[name] = {
                "vector": force_vector,
                "contact_point": contact_point,
                "duration": duration,
            }

    def update_position(self):
        self.position = tuple(p + v for p, v in zip(self.position, self.velocity))

    def update_velocity(self):
        self.velocity = tuple(v + a for v, a in zip(self.velocity, self.acceleration))

    def update(self):
        self.update_position()
        self.update_velocity()

    def calculate_momentum(self):
        self.momentum = tuple(self.mass * v for v in self.velocity)

    def calculate_friction_force(self, normal_force):
        material_name = self.material
        if material_name in material_lib:
            friction_coefficient = material_lib[material_name]["friction"]
            friction_force = friction_coefficient * normal_force
            return friction_force
        else:
            raise ValueError("Material not found in the material library.")

    def detect_collision(self, other_component):
        # Simple bounding box collision detection example
        for vertex in self.geometry:
            if vertex in other_component.geometry:
                return True
        return False

    def resolve_collision(self, other_component):
        # Assuming elastic collision for simplicity
        if self.detect_collision(other_component):
            # Exchange velocities along the collision normal
            self.velocity, other_component.velocity = other_component.velocity, self.velocity

    def update_thermal_expansion(self):
        thermal_coefficient = 0.000012  # Example coefficient for steel
        delta_temperature = self.temperature - 20  # Assuming 20°C as reference
        expansion_factor = 1 + thermal_coefficient * delta_temperature
        self.geometry = [(x * expansion_factor, y * expansion_factor, z * expansion_factor) for x, y, z in self.geometry]
        self.volume *= expansion_factor ** 3

    def calculate_stress_due_to_thermal(self):
        thermal_coefficient = 0.000012  # Example coefficient for steel
        delta_temperature = self.temperature - 20
        youngs_modulus = 200e9  # Pa, for steel
        self.stress += thermal_coefficient * delta_temperature * youngs_modulus

    def update_wear(self, time_interval):
        """Updates the component's wear based on stress, strain, and material properties."""
        base_wear_rate = material_lib[self.material]["wear"]
        stress_factor = 1.0
        if self.stress > 0: 
            stress_limit = material_lib[self.material].get("resistance", float("inf")) * 0.8
            stress_factor = 1 + (self.stress / stress_limit) ** 2
        strain_factor = 1.0
        if self.strain > 0:
            strain_limit = 0.02
            strain_factor = 1 + (self.strain / strain_limit) ** 3
        total_wear_rate = base_wear_rate * stress_factor * strain_factor * time_interval
        self.wear += total_wear_rate

    def calculate_stress(self, force_magnitud):
        if self.surface_area == 0:
            raise ValueError("Surface area is zero. Please set a valid surface area before calculating stress.")
        self.stress = force_magnitud / self.surface_area

    def update_temperature(self, external_temperature, internal_heat_generation):
        # Dynamic temperature update
        self.temperature = self.temperature + internal_heat_generation - (self.temperature - external_temperature) * 0.1

    def update_dynamic_parameters(self, force_magnitud, area, external_temperature, internal_heat_generation, time_interval):
        self.surface_area = area
        self.calculate_stress(force_magnitud)
        self.update_temperature(external_temperature, internal_heat_generation)
        self.update_wear(time_interval)
    

    def calculate_strain(self):
        youngs_modulus = 200e9  # Pa, for steel
        self.strain = self.stress / youngs_modulus

    def calculate_velocity_after_time(self, time_interval):
        if self.mass == 0:
            raise ValueError("Mass is zero. Please set a valid mass before calculating velocity.")
        net_force = self.calculate_net_force()
        self.acceleration = tuple(f / self.mass for f in net_force)
        self.velocity = tuple(v + a * time_interval for v, a in zip(self.velocity, self.acceleration))
        return self.velocity
    
    def calculate_stiffness(self):
        if not self.material or self.volume == 0:
            raise ValueError("Material or volume not set. Please ensure these properties are initialized.")
        youngs_modulus = material_lib[self.material]["resistance"]
        cross_sectional_area = self.surface_area
        length = 1.0
        self.stiffness = (youngs_modulus * cross_sectional_area) / length
        return self.stiffness
    
    def calculate_kinetic_energy(self):
        self.kinetic_energy = 0.5 * self.mass * sum(v ** 2 for v in self.velocity)
        return self.kinetic_energy

    def calculate_potential_energy(self, gravity, reference_height):
        self.potential_energy = self.mass * gravity * (self.position[2] - reference_height)
        return self.potential_energy

    def calculate_net_force(self):
        self.net_force = [0, 0, 0]
        forces_to_remove = []
        for name, force_data in self.forces.items():
            if force_data["duration"] > 0:
                self.net_force = [self.net_force[i] + force_data["vector"][i] for i in range(3)]
                force_data["duration"] -= 1
            else:
                forces_to_remove.append(name)
        for name in forces_to_remove:
            del self.forces[name]
        
        # Update force sensor with the magnitude of the net force
        self.force_sensor.append(np.linalg.norm(self.net_force))
        
        return self.net_force


    #method for seting desired target properties for material design according to forces.
    def derive_target_properties(self):
        # Fatigue limit estimation, assuming the fatigue life is inversely proportional to cycles
        fatigue_life_constant = 1e8  # Example constant, to be refined
        fatigue_limit = self.stress / (self.cycles / fatigue_life_constant)
        
        # Derive target properties based on dynamic attributes
        target_properties = {
            "density": self.mass / self.volume if self.volume > 0 else 7000,
            "resistance": self.stress * 1.5,  # 50% safety margin
            "thermal_expansion": 1e-5,  # Example value based on thermal stability needs
            "wear": self.wear / (self.friction + 1e-6),
            "fatigue_limit": fatigue_limit
        }
        return target_properties   
    

    def optimize_material_ga(self, weight_factors):
        target_properties = self.derive_target_properties()
        material_optimizer_ga = MaterialOptimizerGA(material_lib)
        optimized_material = material_optimizer_ga.optimize_material(target_properties, weight_factors)
        self.material_properties = optimized_material
        return optimized_material
    def update_temperature_sensor(self):
        base_temp = 50  # Base temperature in Celsius
        friction_heat = sum([np.linalg.norm(force["vector"]) for force in self.forces.values()]) * 0.001
        temp = base_temp + friction_heat + np.random.normal(0, 2)  # Add noise to simulate real data
        self.temperature_sensor.append(temp)

    def update_pressure_sensor(self):
        base_pressure = 101.3  # Base pressure in kPa
        applied_force = np.linalg.norm(self.calculate_net_force())
        if self.surface_area > 0:
            pressure = base_pressure + (applied_force / self.surface_area) + np.random.normal(0, 0.05)
        else:
            pressure = base_pressure + np.random.normal(0, 0.05)
        self.pressure_sensor.append(pressure)

    def update_vibration_sensor(self):
        vibration = self.simulate_vibration_response(np.linalg.norm(self.calculate_net_force()), 0.1) 
        vibration_with_noise = max(vibration + np.random.normal(0, 0.05), 0)
        self.vibration_sensor.append(vibration_with_noise)

    def validate_attributes(self):
        errors = []
        if self.mass <= 0:
            errors.append("Mass is not set or invalid.")
        if not hasattr(self, 'surface_area') or self.surface_area <= 0:
            errors.append("Surface area is not set or invalid.")
        if not hasattr(self, 'stiffness') or self.stiffness <= 0:
            errors.append("Stiffness is not set or invalid.")
        if not hasattr(self, 'damping') or self.damping < 0:
            errors.append("Damping is not set or invalid.")
        # Add more checks as necessary...
        return errors

    def simulate(self, time_units):
        validation_errors = self.validate_attributes()
        if validation_errors:
            raise ValueError(f"Component {self.name} cannot start simulation due to: " + ", ".join(validation_errors))
        self.start_sensors()
        for _ in range(time_units):
            self.calculate_net_force() 
            self.acceleration = tuple(f / self.mass for f in self.net_force)
            self.update_velocity()
            self.update_position()
            self.acceleration = (0, 0, 0) 
            self.calculate_kinetic_energy()
            self.calculate_potential_energy(gravity=9.8, reference_height=0)
            self.calculate_stress(sum(self.net_force))
            self.calculate_strain()
            self.update_wear(1)
            # Manually Update sensor data for this time unit
            self.update_temperature_sensor()
            self.update_pressure_sensor()
            self.update_vibration_sensor()
            print(f"data on force sensor : {self.force_sensor}, on pressure sensor: {self.pressure_sensor}, on temperature sensor: {self.temperature_sensor}") ,

        self.stop_sensors()
        
    def update_properties(self, properties):
        for key, value in properties.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"{self.__class__.__name__} has no attribute '{key}'")


