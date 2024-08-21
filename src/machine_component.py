#this module create the machine_component object  with its attributes and methods, for mechanical simulations in an apparatus or similar.
# All is in S.I. units. 
class MachineComponent:
    def __init__(self, name):
        self.name = name
        self.mass = 0  # kg.
        self.position = (0, 0, 0)  # 3D coordinates (x, y, z) in meters
        self.velocity = (0, 0, 0)  # m/s of the center of mass
        self.forces = {}  # dictionary of forces applied on the component
        self.acceleration = (0, 0, 0)  # m/s^2 of the center of mass
        self.momentum = (0, 0, 0)  # kg*m/s of the center of mass
        self.resistance = 0
        self.wear = 0
        self.friction = 0
        self.constraints = {
            "fixed": False,
            "locked": False,
        }
        self.geometry = []  # list of 3D coordinates that define the vertex of the shape of the component
        self.center_of_mass = (0, 0, 0)  # 3D coordinates (x, y, z) in meters
        self.shape = None
        self.color = None
        self.texture = None
        self.volume = 0
        self.material = None
        self.surface_area = 0
        self.temperature = 0
        self.pressure = 0
        self.density = 0
        self.stress = 0
        self.stiffness = 0  # Stiffness in N/m
        self.freedom_degree = {
            "translation": [True, True, True],
            "rotation": [True, True, True]}

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def remove_constraint(self, constraint):
        self.constraints.remove(constraint)

    def apply_force(self, name, force_vector, contact_point):
        self.forces[name] = (force_vector, contact_point)

    def update_position(self):
        self.position = tuple(p + v for p, v in zip(self.position, self.velocity))

    def update_velocity(self):
        self.velocity = tuple(v + a for v, a in zip(self.velocity, self.acceleration))
        self.acceleration = (0, 0, 0)

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

    # 1. Collision Detection and Response
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

    # 2. Thermal Expansion/Contraction
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

    # 3. Friction and Wear Calculation
    def update_wear(self, rate_of_wear):
        self.wear += rate_of_wear  # Simplified wear update based on a given rate

    # 4. Stress and Strain Calculations
    def calculate_stress(self, force):
        if self.surface_area == 0:
            raise ValueError("Surface area is zero. Please set a valid surface area before calculating stress.")
        cross_sectional_area = self.surface_area  # Assuming stress = Force / Area
        self.stress = force / cross_sectional_area

    def calculate_strain(self):
        youngs_modulus = 200e9  # Pa, for steel
        self.strain = self.stress / youngs_modulus


    def calculate_velocity_after_time(self, time_interval):
        """
        Calculate the velocity of the component after a specific time interval 
        given the forces currently applied on the component.
        
        Parameters:
        time_interval (float): The time interval over which to calculate the velocity (in seconds).
        
        Returns:
        tuple: The new velocity of the component (vx, vy, vz) in m/s.
        """
        if self.mass == 0:
            raise ValueError("Mass is zero. Please set a valid mass before calculating velocity.")
        
        # Sum up all the forces to find the net force
        net_force = [0, 0, 0]
        for force_vector, _ in self.forces.values():
            net_force = [net_force[i] + force_vector[i] for i in range(3)]
        
        # Calculate acceleration (a = F/m)
        self.acceleration = tuple(f / self.mass for f in net_force)
        
        # Update velocity (v = u + at)
        self.velocity = tuple(v + a * time_interval for v, a in zip(self.velocity, self.acceleration))
        
        return self.velocity
    
    # Method to calculate stiffness based on material and geometry
    def calculate_stiffness(self):
        if not self.material or self.volume == 0:
            raise ValueError("Material or volume not set. Please ensure these properties are initialized.")
        
        youngs_modulus = material_lib[self.material]["resistance"]  # Use the material's resistance as a proxy for Young's modulus
        cross_sectional_area = self.surface_area  # Simplification; in reality, you may need a more specific calculation
        
        # Example formula for stiffness of a bar (stiffness = (Young's modulus * Area) / Length)
        length = 1.0  # Placeholder, this should be based on the geometry of the component
        self.stiffness = (youngs_modulus * cross_sectional_area) / length
        return self.stiffness
    # Modified natural frequency calculation to use the component's stiffness
    def calculate_natural_frequency(self):
        if self.mass == 0:
            raise ValueError("Mass is zero. Please set a valid mass before calculating the natural frequency.")
        if self.stiffness == 0:
            raise ValueError("Stiffness is zero. Please calculate or set stiffness before calculating natural frequency.")
        
        self.natural_frequency = (1 / (2 * 3.1416)) * ((self.stiffness / self.mass) ** 0.5)
        return self.natural_frequency
    
    def simulate_vibration_response(self, force, damping_coefficient):
        # Simple damped harmonic oscillator model
        omega_n = self.calculate_natural_frequency()
        self.amplitude = force / (self.mass * ((omega_n ** 2) - damping_coefficient ** 2))
        return self.amplitude

    # 6. Energy Calculation
    def calculate_kinetic_energy(self):
        self.kinetic_energy = 0.5 * self.mass * sum(v ** 2 for v in self.velocity)
        return self.kinetic_energy

    def calculate_potential_energy(self, gravity, reference_height):
        self.potential_energy = self.mass * gravity * (self.position[2] - reference_height)
        return self.potential_energy

#provide a set of material and resistance in si units in a dictionnary variable, such as steel, copper, bronze, aluminium, etc. with their density, resistance, wear, friction, etc.
#Density: Measured in kilograms per cubic meter (kg/m³)
#Resistance: Measured in Pascals (Pa), which is equivalent to Newtons per square meter (N/m²)
#Wear: Measured in meters per second (m/s) or another unit of wear rate
#Friction: Dimensionless (ratio)

material_lib = {
    "steel": {"density": 7850, "resistance": 200000000000, "wear": 0.000000001, "friction": 0.6},
    "copper": {"density": 8960, "resistance": 167800000000, "wear": 0.000000002, "friction": 0.4},
    "bronze": {"density": 8800, "resistance": 100000000000, "wear": 0.000000003, "friction": 0.5},
    "aluminium": {"density": 2700, "resistance": 69000000000, "wear": 0.000000004, "friction": 0.6},
    "titanium": {"density": 4500, "resistance": 110000000000, "wear": 0.000000005, "friction": 0.5},
    "carbon_fiber": {"density": 1800, "resistance": 200000000000, "wear": 0.000000006, "friction": 0.4},
    "glass": {"density": 2500, "resistance": 70000000000, "wear": 0.000000007, "friction": 0.9},
    "rubber": {"density": 1200, "resistance": 100000000, "wear": 0.000000008, "friction": 1.0},
    "plastic": {"density": 1000, "resistance": 3000000000, "wear": 0.000000009, "friction": 0.8},
    "wood": {"density": 700, "resistance": 1000000000, "wear": 0.000000010, "friction": 0.7},
    "water": {"density": 1000, "resistance": 0, "wear": 0, "friction": 0.01},
    "air": {"density": 1.225, "resistance": 0, "wear": 0, "friction": 0.005},
    "vacuum": {"density": 0, "resistance": 0, "wear": 0, "friction": 0},
    "concrete": {"density": 2400, "resistance": 20000000000, "wear": 0.000000011, "friction": 0.6},
    "granite": {"density": 2700, "resistance": 100000000000, "wear": 0.000000012, "friction": 0.6},
    "marble": {"density": 2500, "resistance": 70000000000, "wear": 0.000000013, "friction": 0.6},
    "ice": {"density": 917, "resistance": 2000000000, "wear": 0.000000014, "friction": 0.1},
    "snow": {"density": 300, "resistance": 100000000, "wear": 0.000000015, "friction": 0.2},
    }

    


        

