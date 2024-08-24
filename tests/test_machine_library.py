import sys, os
#INHOUSE MODULES:
script_directory_src1 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/machine_component.py"))
script_directory_src2 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/machine.py"))
script_directory_src3 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/component_library.py"))
script_directory_src4 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/market_library.py"))

sys.path.append(script_directory_src1)
sys.path.append(script_directory_src2)
sys.path.append(script_directory_src3)
sys.path.append(script_directory_src4)


import unittest
from machine_component import MachineComponent
from market_library import market_library
from machine_library import initialize_abc_machine_library, initialize_full_machine_library, machine_components
from machine import MachineComponent

class TestMachineInitialization(unittest.TestCase):

    def setUp(self):
        # Example market library and machine components for testing
        self.market_library = market_library
        self.machine_components = machine_components
        self.machine_library = initialize_full_machine_library(self.machine_components, self.market_library)

    def test_machine_initialization(self):
        # Test for each machine in the library
        for machine_name, machine in self.machine_library.items():
            print(f"Machine: {machine_name}")
            components = machine.components
            self.assertIsInstance(components, list)
            self.assertGreater(len(components), 0)

            # Check if all components are correctly initialized
            for component_name, quantity in self.machine_components[machine_name].items():
                component_count = sum(1 for c in components if c.name == component_name)
                self.assertEqual(component_count, quantity)
                print(f" - Component: {component_name} (Quantity: {component_count})")

class TestMachineLibrary(unittest.TestCase):

    def setUp(self):
        # Create a mock market library for testing
        self.market_library = market_library # Use the actual market_library for testing
        # Initialize the machine library
        self.machine_library = initialize_abc_machine_library(self.market_library)

    def test_machine_library_initialization(self):
        # Check if the machine library is initialized correctly
        self.assertIsInstance(self.machine_library, dict)
        self.assertGreater(len(self.machine_library), 0)

        for machine_name, machine in self.machine_library.items():
            print(f"Machine: {machine_name}")
            components = machine.components
            self.assertIsInstance(components, list)
            self.assertGreater(len(components), 0)

            for component in components:
                self.assertIsInstance(component, MachineComponent)
                print(f" - Component: {component.name}")



if __name__ == '__main__':
    unittest.main()
