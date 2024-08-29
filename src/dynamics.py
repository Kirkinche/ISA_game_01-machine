# dynamics.py

import numpy as np

class Dynamics:
    @staticmethod
    def update_velocity(component, time_interval):
        """
        Update the velocity of the component using the net force applied and time interval.
        v = u + at
        """
        net_force = component.calculate_net_force()
        component.acceleration = tuple(f / component.mass for f in net_force)
        component.velocity = tuple(v + a * time_interval for v, a in zip(component.velocity, component.acceleration))
        return component.velocity

    @staticmethod
    def update_position(component, time_interval):
        """
        Update the position of the component using the velocity and time interval.
        s = ut + 0.5 * a * t^2
        """
        component.position = tuple(p + v * time_interval + 0.5 * a * time_interval ** 2 
                                   for p, v, a in zip(component.position, component.velocity, component.acceleration))
        return component.position

    @staticmethod
    def calculate_torque(component):
        """
        Calculate torque based on applied forces and their moments arm from the center of mass.
        τ = r × F
        """
        torque = np.array([0.0, 0.0, 0.0])
        for force in component.forces.values():
            torque += np.cross(force["contact_point"], force["vector"])
        return torque

    @staticmethod
    def calculate_kinetic_energy(component):
        """
        Calculate the kinetic energy of the component.
        KE = 0.5 * m * v^2
        """
        kinetic_energy = 0.5 * component.mass * sum(v ** 2 for v in component.velocity)
        return kinetic_energy

    @staticmethod
    def calculate_potential_energy(component, gravity=9.8, reference_height=0):
        """
        Calculate the potential energy of the component.
        PE = m * g * h
        """
        potential_energy = component.mass * gravity * (component.position[2] - reference_height)
        return potential_energy

    @staticmethod
    def calculate_rotational_kinetic_energy(component):
        """
        Calculate the rotational kinetic energy for rotating components.
        KE_rotational = 0.5 * I * ω^2
        """
        moment_of_inertia = component.mass * (component.surface_area ** 2) / 12  # Simplified for rectangular prism
        rotational_kinetic_energy = 0.5 * moment_of_inertia * (component.torque ** 2)
        return rotational_kinetic_energy

    @staticmethod
    def detect_collision(component1, component2):
        """
        Detect if two components are colliding based on their positions and geometries.
        """
        # Simple collision detection logic (can be expanded)
        distance = np.linalg.norm(np.array(component1.position) - np.array(component2.position))
        combined_radius = component1.surface_area + component2.surface_area
        return distance < combined_radius

    @staticmethod
    def resolve_collision(component1, component2):
        """
        Resolve collision between two components, assuming elastic collision.
        """
        if Dynamics.detect_collision(component1, component2):
            # Swap velocities along the collision normal
            normal = np.array(component1.position) - np.array(component2.position)
            normal = normal / np.linalg.norm(normal)  # Normalize the collision normal
            v1_normal = np.dot(component1.velocity, normal) * normal
            v2_normal = np.dot(component2.velocity, normal) * normal

            component1.velocity = tuple(v1 - v2 + v2_normal for v1, v2 in zip(component1.velocity, v1_normal))
            component2.velocity = tuple(v2 - v1 + v1_normal for v1, v2 in zip(component2.velocity, v2_normal))

    @staticmethod
    def calculate_friction_force(component, normal_force):
        """
        Calculate the friction force on the component.
        F_friction = μ * F_normal
        """
        friction_coefficient = component.material_properties.get("friction", 0.5)  # Default to 0.5 if not set
        friction_force = friction_coefficient * normal_force
        return friction_force

    @staticmethod
    def calculate_drag_force(component, air_density=1.225, drag_coefficient=0.47):
        """
        Calculate the aerodynamic drag force on the component.
        F_drag = 0.5 * ρ * v^2 * Cd * A
        """
        velocity_magnitude = np.linalg.norm(component.velocity)
        drag_force = 0.5 * air_density * velocity_magnitude ** 2 * drag_coefficient * component.surface_area
        return drag_force

    @staticmethod
    def simulate_dynamics(component, time_interval, gravity=9.8, reference_height=0):
        """
        Run a full dynamic simulation for a component over a time interval.
        This includes updating position, velocity, and calculating energies.
        """
        Dynamics.update_velocity(component, time_interval)
        Dynamics.update_position(component, time_interval)
        kinetic_energy = Dynamics.calculate_kinetic_energy(component)
        potential_energy = Dynamics.calculate_potential_energy(component, gravity, reference_height)
        rotational_kinetic_energy = Dynamics.calculate_rotational_kinetic_energy(component)
        
        print(f"Kinetic Energy: {kinetic_energy}, Potential Energy: {potential_energy}, Rotational Kinetic Energy: {rotational_kinetic_energy}")
        
        return {
            "kinetic_energy": kinetic_energy,
            "potential_energy": potential_energy,
            "rotational_kinetic_energy": rotational_kinetic_energy
        }
