# main_mechanical.py

from machine import Machine
from machine_component import MachineComponent
from machine_library import initialize_machine_with_all_components, machine_components
from MaterialOptimizerGA import MaterialOptimizerGA
from market_library import market_library
from drive import Drive

class MechanicalSystemManager:
    def __init__(self):
        self.machines = {}
        self.material_optimizer = None
        
    def add_machine(self, machine_name):
        #add a new machine to the machines dictionary
        self.machines[machine_name] = Machine(name=machine_name)
    
    def initialize_machine(self, machine_name):
        if machine_name in machine_components:
            machine = initialize_machine_with_all_components(machine_name, machine_components, market_library)
            print(self.machines)
            # Initialize necessary properties
            for component in machine.components:
                if component.mass == 0:
                    component.mass = 10  # Default mass
                if not hasattr(component, 'stiffness'):
                    component.stiffness = 1000  # Default stiffness
                if not hasattr(component, 'damping'):
                    component.damping = 0.05  # Default damping

            self.machines[machine_name] = machine
            print(f"Machine '{machine_name}' initialized with components: {self.machines[machine_name].components}")
        else:
            print(f"Machine '{machine_name}' not found in machine components library.")

    def display_machine_components(self, machine_name):
        if machine_name in self.machines:
            machine = self.machines[machine_name]
            return [comp.name for comp in machine.components]
        else:
            print(f"Machine '{machine_name}' not found.")
            return []

    def modify_component(self, machine_name, component_name, new_properties):
        if machine_name in self.machines:
            machine = self.machines[machine_name]
            for component in machine.components:
                if component.name == component_name:
                    component.update_properties(new_properties)
                    print(f"Component '{component_name}' in '{machine_name}' updated.")
                    return
            print(f"Component '{component_name}' not found in '{machine_name}'.")
        else:
            print(f"Machine '{machine_name}' not found.")

    def get_sensor_data(self, machine_name):
        if machine_name in self.machines:
            machine = self.machines[machine_name]
            sensor_data = {}
            for component in machine.components:
                sensor_data.update({
                    "temperature": component.temperature_sensor,
                    "pressure": component.pressure_sensor,
                    "vibration": component.vibration_sensor
                })
            return sensor_data
        else:
            print(f"Machine '{machine_name}' not found.")
            return {}

    def run_simulation(self, machine_name, time_units):
        if machine_name in self.machines:
            #we need to apply forces before simulation on each component.
            machine = self.machines[machine_name].simulate(time_units)
            print(f"Running simulation for '{machine_name}'...")
            # Call the simulate method (this will be activated later)
            # self.machines[machine_name].simulate(time_units)
        else:
            print(f"Machine '{machine_name}' not found.")

    def save_machine_data(self, machine_name, file_path):
        if machine_name in self.machines:
            machine = self.machines[machine_name]
            machine_data = {
                "name": machine.name,
                "components": [
                    {
                        "name": component.name,
                        "cost": component.cost,
                        "mass": component.mass,
                        "position": component.position,
                        "velocity": component.velocity,
                        "forces": component.forces,
                        "acceleration": component.acceleration,
                        "volume": component.volume,
                        "momentum": component.momentum,
                        "temperature": component.temperature,
                        "pressure": component.pressure,
                        "vibration_intensity": component.vibration_intensity,
                        "temperature_sensor": component.temperature_sensor,
                        "pressure_sensor": component.pressure_sensor,
                        "vibration_sensor": component.vibration_sensor,
                        "force_sensor": component.force_sensor,
                        "rotation_speed_sensor": component.rotation_speed_sensor,
                        "current_sensor": component.current_sensor,
                        "surface_area": component.surface_area,
                        "stress": component.stress,
                        "strain": component.strain,
                        "wear": component.wear,
                        "material": component.material,
                        "friction": component.friction,
                        "cycles": component.cycles,
                        "material_properties": component.material_properties,
                    }
                    for component in machine.components
                ]
            }
            Drive.write_to_json(file_path, machine_data)
        else:
            print(f"Machine '{machine_name}' not found.")

    def load_machine_data(self, file_path):
        machine_data = Drive.read_from_json(file_path)
        if machine_data:
            # Reconstruct the machine from the loaded data
            machine_name = machine_data["name"]
            components_data = machine_data["components"]
            components = []
            i=0
            for comp_data in components_data:                
                component_load = MachineComponent(comp_data["name"])
                component_load.cost = comp_data.get("cost", 0)
                component_load.mass=comp_data.get("mass", 0),
                component_load.position=tuple(comp_data.get("position", (0, 0, 0))),
                component_load.velocity=tuple(comp_data.get("velocity", (0, 0, 0))),
                component_load.forces=comp_data.get("forces", {}),
                component_load.acceleration=tuple(comp_data.get("acceleration", (0, 0, 0))),
                component_load.volume=comp_data.get("volume", 0),
                component_load.momentum=tuple(comp_data.get("momentum", (0, 0, 0))),
                component_load.temperature=comp_data.get("temperature", 25.0),
                component_load.pressure=comp_data.get("pressure", 101.3),
                component_load.vibration_intensity=comp_data.get("vibration_intensity", 0.0),
                component_load.temperature_sensor=comp_data.get("temperature_sensor", []),
                component_load.pressure_sensor=comp_data.get("pressure_sensor", []),
                component_load.vibration_sensor=comp_data.get("vibration_sensor", []),
                component_load.force_sensor=comp_data.get("force_sensor", []),
                component_load.rotation_speed_sensor=comp_data.get("rotation_speed_sensor", []),
                component_load.current_sensor=comp_data.get("current_sensor", []),
                component_load.surface_area=comp_data.get("surface_area", 0),
                component_load.stress=comp_data.get("stress", 0),
                component_load.strain=comp_data.get("strain", 0),
                component_load.wear=comp_data.get("wear", 0),
                component_load.material=comp_data.get("material", None),
                component_load.friction=comp_data.get("friction", 0),
                component_load.cycles=comp_data.get("cycles", 1e6),
                component_load.material_properties=comp_data.get("material_properties", {"density": 0, "resistance": 0, "wear": 0, "friction": 0}),
                components.append(component_load)
            self.machines[machine_name] = Machine(name=machine_name)
            self.machines[machine_name].components = components    
            print(f"Machine '{machine_name}' loaded from {file_path}.")

    def apply_force(self, machine_name, component_name, force_name, force_vector, contact_point, duration):
        if machine_name in self.machines:
            machine = self.machines[machine_name]
            component = machine.get_component_by_name(component_name)
            if component:
                component.apply_force(force_name, force_vector, contact_point, duration)
                print(f"Force '{force_name}' applied to '{component_name}' in '{machine_name}'.")
            else:
                print(f"Component '{component_name}' not found in '{machine_name}'.")
        else:
            print(f"Machine '{machine_name}' not found.") 

# Example usage:
if __name__ == "__main__":
    manager = MechanicalSystemManager()
    manager.initialize_machine("electric_motor")
