import sys, os
#INHOUSE MODULES:
script_directory_src1 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/machine_component.py"))
sys.path.append(script_directory_src1)
import unittest
import time
from machine_component import MachineComponent
import math

def calculate_magnitude(vector):
    x, y, z = vector
    return math.sqrt(x**2 + y**2 + z**2)


class TestMachineComponent(unittest.TestCase):

    def setUp(self):
        # Initialize a MachineComponent object for testing
        self.component = MachineComponent("TestComponent")
        self.component.mass = 1000  # kg
        self.component.surface_area = 2  # m^2
        self.component.material = "steel"  # Using steel from material_lib

    def test_apply_force(self):
        # Apply a force to the component
        self.component.apply_force("test_force", (10, 0, 0), (1, 0, 0), duration=5)
        self.assertIn("test_force", self.component.forces)
        self.assertEqual(self.component.forces["test_force"]["vector"], (10, 0, 0))

    def test_calculate_net_force(self):
        # Apply multiple forces and calculate net force
        self.component.apply_force("force1", (10, 0, 0), (1, 0, 0), duration=5)
        self.component.apply_force("force2", (0, 50, 0), (1, 0, 0), duration=5)
        net_force = self.component.calculate_net_force()
        self.assertEqual(net_force, [10, 50, 0])

    def test_calculate_stress(self):
        # Calculate stress based on applied force and surface area
        force = 2000  # N
        self.component.calculate_stress(force)
        expected_stress = force / self.component.surface_area
        self.assertEqual(self.component.stress, expected_stress)

    def test_calculate_strain(self):
        # Calculate strain based on stress and material properties
        self.component.stress = 200000000  # Pa
        self.component.calculate_strain()
        expected_strain = self.component.stress / 200e9  # Young's modulus of steel
        self.assertAlmostEqual(self.component.strain, expected_strain)

    def test_simulate_temperature(self):
        # Test the temperature simulation method with real-time data printout
        self.component.start_sensors()
        print("Real-time Temperature Data:")
        for _ in range(5):  # Simulate and print data for 5 seconds
            time.sleep(1)
            print(f"Temperature: {self.component.temperature_sensor[-1]:.2f} °C")
        self.assertTrue(len(self.component.temperature_sensor) > 0)
        self.assertTrue(40 <= self.component.temperature_sensor[-1] <= 60)

    def test_simulate_pressure(self):
        # Test the pressure simulation method with real-time data printout
        self.component.start_sensors()
        print("Real-time Pressure Data:")
        for _ in range(5):  # Simulate and print data for 5 seconds
            time.sleep(1)
            pressure_value = self.component.pressure_sensor[-1]
            print(f"Pressure: {pressure_value:.2f} kPa")
            self.assertTrue(99 <= pressure_value <= 105.0, "Pressure is out of expected range")

    def test_simulate_vibration(self):
        # Test the vibration simulation method with real-time data printout
        self.component.start_sensors()
        print("Real-time Vibration Data:")
        for _ in range(5):  # Simulate and print data for 5 seconds
            time.sleep(1)
            vibration_value = self.component.vibration_sensor[-1]
            print(f"Vibration Intensity: {vibration_value:.2f} units")
            self.assertGreaterEqual(vibration_value, 0, "Vibration intensity should be non-negative")

    def test_update_position(self):
        # Test the update_position method
        self.component.velocity = (1, 1, 1)  # m/s
        self.component.update_position()
        print(f"position: {self.component.position}")
        self.assertEqual(self.component.position, (1, 1, 1))

    def test_calculate_kinetic_energy(self):
        # Test the kinetic energy calculation
        self.component.velocity = (10, 0, 0)  # m/s
        kinetic_energy = self.component.calculate_kinetic_energy()
        expected_ke = 0.5 * self.component.mass * 10 ** 2
        print(f"kinetic energy: {kinetic_energy}")
        self.assertEqual(kinetic_energy, expected_ke)

    def test_calculate_potential_energy(self):
        # Test the potential energy calculation
        self.component.position = (0, 0, 10)  # 10 meters above reference
        potential_energy = self.component.calculate_potential_energy(gravity=9.8, reference_height=0)
        expected_pe = self.component.mass * 9.8 * 10
        self.assertEqual(potential_energy, expected_pe)

    def test_update_wear(self):
        # Test the wear update method
        self.component.stress = 150000000  # Pa
        self.component.update_wear(1)  # Simulate for 1 time unit
        self.assertTrue(self.component.wear > 0)

    def tearDown(self):
        self.component.stop_sensors()  # Stop the sensor threads
        time.sleep(1)  # Give time for threads to terminate

    def testMaterialOptimizerGA(self):
        self.component.mass = 100  # kg
        self.component.volume = 0.01  # m^3
        self.component.stress = 300e6  # Pa
        self.component.temperature = 150  # Celsius
        self.component.wear = 1e-7
        self.component.friction = 0.3
        self.component.cycles = 1e6
        self.component.apply_force("force1", (10, 0, 0), (1, 0, 0), duration=5)
        self.component.apply_force("force2", (0, 50, 0), (1, 0, 0), duration=5)
        force_magnitud = calculate_magnitude(self.component.calculate_net_force())
        area = 0.1
        self.component.update_dynamic_parameters(force_magnitud, area, external_temperature = 20, internal_heat_generation = 10, time_interval=3)
        weight_factors = {
            "density": 0.6,
            "resistance": 0.2,
            "thermal_expansion": 0.2,
            "wear": 0.2,
            "fatigue_limit": 0.1
        }

        optimized_properties_ga = self.component.optimize_material_ga(weight_factors)
        print("Optimized Material Properties for Component using GA:", optimized_properties_ga)
    
    def testSimulate(self):
        self.component.apply_force("force1", (100, 0, 0), (1, 0, 0), duration=5)
        self.component.apply_force("force2", (0, 500, 0), (1, 0, 0), duration=5)
        self.component.simulate(10)


if __name__ == '__main__':
    unittest.main()
