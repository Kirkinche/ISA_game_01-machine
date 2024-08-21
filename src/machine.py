#this module create the machine object with its attributes and methods, for machinery and apparatus simulations.
from typing import Any
from machine_component import MachineComponent


class Machine:
    def __init__(self, name):
        self.name = name
        self.components = [MachineComponent(name)]
        self.status = "off"
        self.speed = 0
        self.power_consumption = 0
        self.operating_cost = 0
        self.manufacturing_cost = 0
        self.wear_and_maintenance = {}
        self.center_of_mass = (0, 0, 0)
        self.structural_integrity = {}

    def add_component(self, component = MachineComponent(Any)):
        """Adds a MachineComponent to the machine."""
        if isinstance(component, MachineComponent):
            self.components.append(component)
        else:
            raise TypeError("Only MachineComponent objects can be added.")

    def calculate_total_mass(self):
        """Calculates the total mass of the machine by summing the masses of all components."""
        return sum(component.mass for component in self.components)

    def calculate_power_consumption(self, time_period):
        """Calculates the power consumption of the machine based on the kinetic energy of its components."""
        total_kinetic_energy = sum(component.calculate_kinetic_energy() for component in self.components)
        power_consumption = total_kinetic_energy / time_period  # Power = Energy / Time
        return power_consumption

    def calculate_operating_cost(self, time_period, energy_cost_per_kwh):
        """Estimates the operating cost of the machine over a given time period."""
        power_consumption_kw = self.calculate_power_consumption(time_period) / 1000  # Convert W to kW
        energy_cost = power_consumption_kw * time_period * energy_cost_per_kwh
        # Additional costs (e.g., labor, maintenance) could be added here
        return energy_cost

    def calculate_manufacturing_cost(self, component_costs):
        """Calculates the total manufacturing cost based on the cost of individual components."""
        total_cost = 0
        for component in self.components:
            total_cost += component_costs.get(component.name, 0)
        return total_cost

    def calculate_wear_and_maintenance(self):
        """Estimates the wear of each component and suggests a maintenance schedule."""
        wear_data = {}
        for component in self.components:
            wear_data[component.name] = component.wear  # Simply using the wear attribute for now
        # In a real scenario, this could trigger alerts or suggest maintenance times
        return wear_data

    def calculate_center_of_mass(self):
        """Calculates the overall center of mass of the machine."""
        total_mass = self.calculate_total_mass()
        if total_mass == 0:
            return (0, 0, 0)

        center_of_mass = [0, 0, 0]
        for component in self.components:
            for i in range(3):
                center_of_mass[i] += component.mass * component.center_of_mass[i]
        
        center_of_mass = tuple(coord / total_mass for coord in center_of_mass)
        return center_of_mass

    def calculate_structural_integrity(self):
        """Assesses the structural integrity of the machine by checking stress on critical components."""
        stress_data = {}
        for component in self.components:
            if component.stress > component.calculate_stress_due_to_thermal():
                stress_data[component.name] = component.stress
        return stress_data

    def estimate_environmental_impact(self):
        """Estimates the environmental impact of the machine."""
        impact = 0
        for component in self.components:
            # Simplified model: sum up impacts based on material and mass
            material_density = material_lib.get(component.material, {}).get("density", 0)
            impact += material_density * component.mass
        return impact
