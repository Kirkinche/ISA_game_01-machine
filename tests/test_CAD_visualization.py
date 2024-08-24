import sys, os
#INHOUSE MODULES:
script_directory_src1 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/machine_component.py"))
script_directory_src2 = os.path.dirname(os.path.abspath("E:/APIs/ISA_game_01/src/CAD_visualization.py"))
sys.path.append(script_directory_src1)
sys.path.append(script_directory_src2)

#import unittest
import time
from machine_component import MachineComponent
from CAD_visualization import CADVisualizer, MeshGenerator

#class TestCadVisualization(unittest.TestCase):
#    def setUp(self):
        # Initialize a MachineComponent object for testing
#        self.component = MachineComponent("TestComponent")
