#this module create the machine object with its attributes and methods, for machinery and apparatus simulations.
from typing import Any
from machine_component import MachineComponent
from library import material_lib
from dynamics import Dynamics
import numpy as np

        


class Machine:
    def __init__(self, name):
        self.name = name
        self.components = []
        self.add_component(MachineComponent("Ground")) # all machine must have an initial component named "Ground", which represent the ground wher the machine is placed.        
        self.components[0].material = "steel"
        self.components[0].position = (0,0,0)
        self.components[0].mass = 10^30 # the ground has an infinite mass, so it doesn't move during the simulation
        self.status = "off"
        self.speed = 0
        self.power_consumption = 0
        self.operating_cost = 0
        self.manufacturing_cost = 0
        self.wear_and_maintenance = {}
        self.center_of_mass = (0, 0, 0)
        self.structural_integrity = {}
        self.connections = []  # Traditional two-component connections
        self.multi_component_connections = []  # Multi-component connections

    def add_component(self, component = MachineComponent(Any)):
        """Adds a MachineComponent to the machine."""
        if isinstance(component, MachineComponent):
            # unique name only
            if not component.name in [c.name for c in self.components]:
                self.components.append(component)
            else:
                raise TypeError(f"Component with name '{component.name}' already exists in the machine.")
        else:
            raise TypeError("Only MachineComponent objects can be added.")

    def calculate_total_mass(self):
        """Calculates the total mass of the machine by summing the masses of all components."""
        return sum(component.mass for component in self.components)

    def calculate_power_consumption(self, time_period):
        """Calculates the power consumption of the machine based on the kinetic energy of its components."""
        total_kinetic_energy = 0 
        for component in self.components:
            component.calculate_dynamics(time_period)  # Assuming this method calculates the kinetic energy of the component
            total_kinetic_energy += component.kinetic_energy
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

    #THIS SECTION ARTICULATE THE CONNECTIONS BETWEEN COMPONENTS

    def add_connection(self, component1: MachineComponent, component2: MachineComponent, connection_type: str, 
                       degrees_of_freedom: dict, relative_position1: tuple = (0, 0, 0), relative_position2: tuple = (0, 0, 0)):
        """
        Adds a traditional connection between two components with specific degrees of freedom and relative positions.
        """
        connection = {
            "component1": component1.name,
            "component2": component2.name,
            "connection_type": connection_type,
            "degrees_of_freedom": degrees_of_freedom,
            "relative_position1": relative_position1,
            "relative_position2": relative_position2
        }
        self.connections.append(connection)
        print(f"Connection added between {component1.name} and {component2.name} as {connection_type} with DOF: {degrees_of_freedom}.")
#TODO 1: Implement the _apply_connection method to apply the constraints of the connection to the components. This could involve updating the position, velocity, and acceleration of the components based on their connection.
    def add_multi_component_connection(self, components: list, connection_type: str, degrees_of_freedom: dict, relative_positions: list):
        """
        Adds a multi-component connection with specific degrees of freedom and relative positions.
        """
        if len(components) != len(relative_positions):
            raise ValueError("The number of components and relative positions must match.")

        connection = {
            "components": components,
            "connection_type": connection_type,
            "degrees_of_freedom": degrees_of_freedom,
            "relative_positions": relative_positions
        }
        self.multi_component_connections.append(connection)
        component_names = ', '.join([c.name for c in components])
        print(f"Multi-component connection added between {component_names} as {connection_type} with DOF: {degrees_of_freedom}.")
#TODO 2: Implement the _apply_multi_component_connection method to apply the constraints of the multi-component connection to the components. This could involve updating the position, velocity, and acceleration of the components based on their connection.
    def _apply_parallel_connection(self, components, degrees_of_freedom, relative_positions):
        """
        Apply parallel connection constraints among the components.
        This maintains parallelism between the components.
        """
        # Example logic for parallelism
        base_position = components[0].position
        for i, component in enumerate(components[1:], start=1):
            corrected_position = tuple(bp + rp1 - rp2 for bp, rp1, rp2 in zip(base_position, relative_positions[0], relative_positions[i]))
            component.position = corrected_position
            component.velocity = components[0].velocity
            component.acceleration = components[0].acceleration
        print(f"Parallel connection applied among components with DOF: {degrees_of_freedom}.")
#TODO 3: Implement the _apply_serial_connection method to apply the constraints of the serial connection to the components. This could involve updating the position, velocity, and acceleration of the components based on their connection.
    def _apply_bi_directional_connection(self, components, degrees_of_freedom, relative_positions):
        """
        Apply bi-directional connection constraints among the components.
        This allows bi-directional control among the components.
        """
        # Example logic for bi-directional control
        # Implement the bi-directional connection logic here based on the DOFs and relative positions
        print(f"Bi-directional connection applied among components with DOF: {degrees_of_freedom}.")

    # Add more methods for other specific multi-component connections as needed

    def calculate_connection_dynamics(self, time_interval, component1, component2):
        """
        Calculate the dynamics for all connections within the machine for the given time interval.
        This includes updating positions, velocities, and forces.
        """
        # Handle traditional connections
        for connection in self.connections:
            component1_name = connection["component1"]
            component2__name = connection["component2"]
            connection_type = connection["connection_type"]
            degrees_of_freedom = connection["degrees_of_freedom"]
            relative_position1 = connection["relative_position1"]
            relative_position2 = connection["relative_position2"]

            #if component1_name == component1.name and component2__name == component2.name:
            if connection_type == "fixed":
                self._apply_fixed_connection(component1, component2, relative_position1, relative_position2)
            elif connection_type == "hinge":
                self._apply_hinge_connection(component1, component2, degrees_of_freedom, relative_position1, relative_position2)
            elif connection_type == "slider":
                self._apply_slider_connection(component1, component2, degrees_of_freedom, relative_position1, relative_position2)
            #else:
            #    raise ValueError("The components do not match the connection.")
        if self.connections:
            print(f"connection dynamics calculated for: {component1.name} and {component2.name} for this time interval.: {time_interval}")

        # Handle multi-component connections
        for connection in self.multi_component_connections:
            components = connection["components"]
            connection_type = connection["connection_type"]
            degrees_of_freedom = connection["degrees_of_freedom"]
            relative_positions = connection["relative_positions"]

            if connection_type == "parallel":
                self._apply_parallel_connection(components, degrees_of_freedom, relative_positions)
            elif connection_type == "bi-directional":
                self._apply_bi_directional_connection(components, degrees_of_freedom, relative_positions)
            # Add additional connection types here

    def _apply_fixed_connection(self, component1, component2, relative_position1, relative_position2):
        """
        Apply fixed connection constraints between two components.
        This restricts all relative motion between the components.
        """
        self.get_component_by_name(component1)
        corrected_position = tuple(c1 + rp1 + rp2 for c1, rp1, rp2 in zip(component1.position, relative_position1, relative_position2))
        component2.position = corrected_position
        component2.velocity = component1.velocity
        component2.acceleration = component1.acceleration
        
            
        # Calculate and apply reaction forces
        reaction_force_vector = []
        for i in range(3):  # Assuming 3D space (x, y, z)
            reaction_force = (component2.mass * component2.acceleration[i]) - (component1.mass * component1.acceleration[i]) 
            reaction_force_vector.append(reaction_force)

        # Apply reaction forces directly to the forces dictionary of each component
        component1.apply_force(
            name="fixed_connection_reaction",
            force_vector=tuple(-f for f in reaction_force_vector),  # Apply in the opposite direction
            contact_point=relative_position1,
            duration=1
        )
        component2.apply_force(
            name="fixed_connection_reaction",
            force_vector=tuple(reaction_force_vector),  # Apply in the correct direction
            contact_point=relative_position2,
            duration=1
        )

        print(f"Fixed connection applied between {component1.name} and {component2.name} at relative positions {relative_position1} and {relative_position2}.")
        print(f"Reaction forces applied: {reaction_force_vector}")# Calculate the reaction force to maintain the fixed connection

    def _apply_hinge_connection(self, component1, component2, degrees_of_freedom, relative_position1, relative_position2):
        """
        Apply hinge connection constraints between two components.
        This restricts relative motion to rotational movement around specific axes and calculates the necessary reaction forces and torques.
        """
        # Correct the position of component2 based on the hinge connection
        corrected_position = tuple(c1 + rp1 + rp2 for c1, rp1, rp2 in zip(component1.position, relative_position1, relative_position2))
        component2.position = corrected_position

        # Adjust velocity and acceleration based on allowed DOF
        new_velocity = list(component2.velocity)
        new_acceleration = list(component2.acceleration)

        for axis, idx in zip(['x', 'y', 'z'], range(3)):
            if 'rotation' in degrees_of_freedom:
                if axis not in degrees_of_freedom['rotation']:
                    new_velocity[idx] = 0  # Restrict velocity if rotation around this axis is not allowed
                    new_acceleration[idx] = 0  # Restrict acceleration as well

        component2.velocity = tuple(new_velocity)
        component2.acceleration = tuple(new_acceleration)

        # Calculate and apply reaction forces and torques to maintain the hinge constraint
        for i, axis in enumerate(['x', 'y', 'z']):
            if axis not in degrees_of_freedom.get('rotation', []):
                # Calculate the reaction force to prevent rotation around this axis
                reaction_force = (component2.mass * component2.acceleration[i]) - (component1.mass * component1.acceleration[i])

                # Apply the reaction force to both components
                force_name = f"hinge_reaction_force_{axis}"
                component1.apply_force(
                    name=force_name,
                    force_vector=tuple(-reaction_force if j == i else 0.0 for j in range(3)),
                    contact_point=relative_position1,
                    duration=1
                )
                component2.apply_force(
                    name=force_name,
                    force_vector=tuple(reaction_force if j == i else 0.0 for j in range(3)),
                    contact_point=relative_position2,
                    duration=1
                )

                # Calculate torque: τ = r × F, where r is the position vector, F is the reaction force vector
                r_vector = tuple(cp2 - cp1 for cp1, cp2 in zip(relative_position1, relative_position2))
                torque_vector = (
                    r_vector[1] * reaction_force - r_vector[2] * reaction_force,  # Torque around x-axis
                    r_vector[2] * reaction_force - r_vector[0] * reaction_force,  # Torque around y-axis
                    r_vector[0] * reaction_force - r_vector[1] * reaction_force   # Torque around z-axis
                )
                
                # Update the torque for both components
                component1.torque = component1.update_torque()
                component2.torque = component2.update_torque()

        print(f"Hinge connection applied between {component1.name} and {component2.name} with DOF: {degrees_of_freedom} at relative positions {relative_position1} and {relative_position2}.")


    def _apply_slider_connection(self, component1, component2, degrees_of_freedom, relative_position1, relative_position2):
        """
        Apply slider connection constraints between two components.
        This restricts relative motion to translational movement along specific axes.
        """
        corrected_position = tuple(c1 + rp1 + rp2 for c1, rp1, rp2 in zip(component1.position, relative_position1, relative_position2))
        component2.position = corrected_position

        # Adjust velocity and acceleration based on allowed DOF
        new_velocity = list(component2.velocity)
        new_acceleration = list(component2.acceleration)

        if 'translation' in degrees_of_freedom:
            if 'x' not in degrees_of_freedom['translation']:
                new_velocity[0] = 0
                new_acceleration[0] = 0
            if 'y' not in degrees_of_freedom['translation']:
                new_velocity[1] = 0
                new_acceleration[1] = 0
            if 'z' not in degrees_of_freedom['translation']:
                new_velocity[2] = 0
                new_acceleration[2] = 0

        component2.velocity = tuple(new_velocity)
        component2.acceleration = tuple(new_acceleration)

        print(f"Slider connection applied between {component1.name} and {component2.name} with DOF: {degrees_of_freedom} at relative positions {relative_position1} and {relative_position2}.")



#THIS METHOD ARTICULATE THE SIMULATION 
    def simulate(self, time_duration):
        """Simulates the machine's behavior over a given number of time units."""
        positions, upvectors = [], []
        component_positions = []
        component_upvectors = []
        for _ in range(time_duration):
            i = 0
            for component in self.components:
                if component.name == "Ground":  # Skip the ground component
                    continue
                else:
                    component.calculate_dynamics(1)
                    validation_errors = component.validate_attributes()
                    if validation_errors:
                        raise ValueError(f"Component {component.name} cannot start simulation due to: " + ", ".join(validation_errors))
                    # Initialize lists to store positions and upvectors
                    print(component.position)
                    component.start_sensors()
                    component.acceleration = (0, 0, 0)
                    # We need to fix the connection between component and its effects
                    self.calculate_connection_dynamics(1, self.components[i], component)
                    i += 1
                    print (i)
                    #for connection in self.connections:
                    #    component2 = connection["component2"]
                    #component.position = component2.position          
                    #component.upvector = component2.upvector
                    #component.velocity = component2.velocity
                    #component.acceleration = component2.acceleration
                    #component.forces = component2.forces
                    component.update(1)
                    component.acceleration = tuple(f / component.mass for f in component.net_force)
                    component.calculate_damping
                    # Store the current position and upvector
                    component_positions.append({'name': component.name, 'position': component.position})
                    component_upvectors.append({'name': component.name, 'upvector': component.upvector})
                
                    component.calculate_stress(sum(component.net_force))
                    component.calculate_strain()
                    component.update_wear(1)
                    # Manually Update sensor data for this time unit
                    component.update_temperature_sensor()
                    component.update_pressure_sensor()
                    component.update_vibration_sensor()
                    print(f"name: {component.name} on position: {component.position}")
                    #print(f"data on force sensor : {self.force_sensor}, on pressure sensor: {self.pressure_sensor}, on temperature sensor: {self.temperature_sensor}, position of component: {self.position}, velocity: {self.velocity}") ,
                    component.stop_sensors()
                    #update the forces and reaction with connections from assembler instance
                    #self.assembler.calculate_dynamics(1)
            positions.append({})
            upvectors.append({})
            # Populate the positions and upvectors with data from each component
            for component in self.components:
                positions[_][component.name] = component_positions[_]['position']
                upvectors[_][component.name] = component_upvectors[_]['upvector']

        return positions, upvectors
   
    def get_component_by_name(self, name):
        for component in self.components:
            if component.name == name:
                return component
        return None
    
if __name__ == "__main__":
    # Example usage of the Machine class
    machine = Machine("Robotic Arm")
    component1 = MachineComponent("Base")
    component2 = MachineComponent("Arm")
    component3 = MachineComponent("Claw")

    # Setting material of components
    component1.material = "steel"
    component2.material = "steel"
    component3.material = "steel"
    component1.apply_force("init", (-10, 5, 0),(0, 0, 0.2), 4)
    component2.apply_force("init2", (0, 0, -0.1),(1, 0, 0), 2)    
    #component1.acceleration = (0,1,0)
    #component2.acceleration = (0,3,1)
    # Add components to machine
    machine.add_component(component1)
    machine.add_component(component2)
    machine.add_component(component3)

    # Create assembler
    

    # Define degrees of freedom
    hinge_dof = {'rotation': ['z']}
    slider_dof = {'translation': ['x']}

    # Add connections with DOF and relative positions
    machine.add_connection(machine.components[1], machine.components[2], "hinge", hinge_dof, relative_position1=(0, 0, 1), relative_position2=(0, 0, 1.5))
    machine.add_connection(machine.components[2], machine.components[3], "slider", slider_dof, relative_position1=(0, 0, 0.5), relative_position2=(0, 0, 0))
    
    positions, upvectors = machine.simulate(10)

    print(positions, upvectors) 

