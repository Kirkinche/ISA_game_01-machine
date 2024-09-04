
from machine import Machine
from machine_component import MachineComponent
from dynamics import Dynamics
import numpy as np
class Assembler:
    def __init__(self, machine: Machine):
        self.machine = machine
        self.connections = []  # Traditional two-component connections
        self.multi_component_connections = []  # Multi-component connections

    def add_connection(self, component1: MachineComponent, component2: MachineComponent, connection_type: str, 
                       degrees_of_freedom: dict, relative_position1: tuple = (0, 0, 0), relative_position2: tuple = (0, 0, 0)):
        """
        Adds a traditional connection between two components with specific degrees of freedom and relative positions.
        """
        connection = {
            "component1": component1,
            "component2": component2,
            "connection_type": connection_type,
            "degrees_of_freedom": degrees_of_freedom,
            "relative_position1": relative_position1,
            "relative_position2": relative_position2
        }
        self.connections.append(connection)
        print(f"Connection added between {component1.name} and {component2.name} as {connection_type} with DOF: {degrees_of_freedom}.")

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

    def _apply_bi_directional_connection(self, components, degrees_of_freedom, relative_positions):
        """
        Apply bi-directional connection constraints among the components.
        This allows bi-directional control among the components.
        """
        # Example logic for bi-directional control
        # Implement the bi-directional connection logic here based on the DOFs and relative positions
        print(f"Bi-directional connection applied among components with DOF: {degrees_of_freedom}.")

    # Add more methods for other specific multi-component connections as needed

    def calculate_dynamics(self, time_interval):
        """
        Calculate the dynamics for all connections within the machine for the given time interval.
        This includes updating positions, velocities, and forces.
        """
        # Handle traditional connections
        for connection in self.connections:
            component1 = connection["component1"]
            component2 = connection["component2"]
            connection_type = connection["connection_type"]
            degrees_of_freedom = connection["degrees_of_freedom"]
            relative_position1 = connection["relative_position1"]
            relative_position2 = connection["relative_position2"]

            if connection_type == "fixed":
                self._apply_fixed_connection(component1, component2, relative_position1, relative_position2)
            elif connection_type == "hinge":
                self._apply_hinge_connection(component1, component2, degrees_of_freedom, relative_position1, relative_position2)
            elif connection_type == "slider":
                self._apply_slider_connection(component1, component2, degrees_of_freedom, relative_position1, relative_position2)


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


    def simulate(self, time_interval, total_time):
        """
        Simulate the machine's behavior over the total time by updating each component's dynamics.
        """
        steps = int(total_time / time_interval)
        for _ in range(steps):
            self.calculate_dynamics(time_interval)
            self.machine.simulate(time_interval)
        print(f"Simulation completed for {total_time} time units.")

    def _apply_fixed_connection(self, component1, component2, relative_position1, relative_position2):
        """
        Apply fixed connection constraints between two components.
        This restricts all relative motion between the components.
        """
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

# Example usage:
if __name__ == "__main__":
    # Create machine and components
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
    assembler = Assembler(machine)

    # Define degrees of freedom
    hinge_dof = {'rotation': ['z']}
    slider_dof = {'translation': ['x']}

    # Add connections with DOF and relative positions
    assembler.add_connection(component1, component2, "hinge", hinge_dof, relative_position1=(0, 0, 1), relative_position2=(0, 0, 1.5))
    assembler.add_connection(component2, component3, "slider", slider_dof, relative_position1=(0, 0, 0.5), relative_position2=(0, 0, 0))

