import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import * 
from OpenGL.GLU import *
import numpy as np
from machine_component import MachineComponent
from assembler import Assembler
from machine import Machine
import math

class Machine3DVisualization(QOpenGLWidget):
    def __init__(self, components, connections, camera_position=(0, 0, 10), look_at_point=(0, 0, 0), up_vector=(0, 1, 0), parent=None):
        super().__init__(parent)
        self.components = components
        self.connections = connections
        self.camera_position = camera_position
        self.look_at_point = look_at_point
        self.up_vector = up_vector

    def initializeGL(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Set background color to white
        glEnable(GL_DEPTH_TEST)  # Enable depth testing for 3D rendering

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h, 0.1, 50.0)  # Field of view, aspect ratio, near, far
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(
            *self.camera_position,  # Camera position
            *self.look_at_point,     # Look-at point
            *self.up_vector          # Up vector
        )

        glColor3f(0.9, 0.6, 0.2)  # Set drawing color to yellow-orange (black is (0, 0, 0))

        # Draw components as cylinders
        for component in self.components:
            self.draw_cylinder(component.position, radius=0.5, height=1)  # Standard cylinder size

        # Draw connections as lines from component positions to relative positions
        glBegin(GL_LINES)
        for conn in self.connections:
            component1_pos = conn['component1'].position
            component2_pos = conn['component2'].position

            relative_position1 = conn['relative_position1']
            relative_position2 = conn['relative_position2']

            # Calculate the absolute positions based on the relative positions
            line_start_pos1 = [component1_pos[i] + relative_position1[i] for i in range(3)]
            line_start_pos2 = [component2_pos[i] - relative_position2[i] for i in range(3)]

            # Draw line from component1 to its relative position
            glVertex3fv(component1_pos)
            glVertex3fv(line_start_pos1)

            # Draw line from component2 to its relative position
            glVertex3fv(component2_pos)
            glVertex3fv(line_start_pos2)
        glEnd()

    def draw_cylinder(self, position, radius, height):
        """
        Draw a cylinder centered at `position` with the given `radius` and `height`.
        """
        num_segments = 12  # Number of segments to approximate the circular base
        half_height = height / 2.0

        # Draw the top and bottom circles
        for z in [-half_height, half_height]:
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(position[0], position[1], position[2] + z)  # Center of the circle
            for i in range(num_segments + 1):
                angle = 2 * math.pi * i / num_segments
                x = position[0] + radius * math.cos(angle)
                y = position[1] + radius * math.sin(angle)
                glVertex3f(x, y, position[2] + z)
            glEnd()

        # Draw the side of the cylinder
        glBegin(GL_QUAD_STRIP)
        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(position[0] + x, position[1] + y, position[2] - half_height)
            glVertex3f(position[0] + x, position[1] + y, position[2] + half_height)
        glEnd()

class MainWindow(QMainWindow):
    def __init__(self, components, connections):
        super().__init__()
        self.setWindowTitle("3D Machine Visualization")
        self.setGeometry(100, 100, 800, 600)
        
        camera_position = (5, 5, 10)  # Example camera position
        look_at_point = (0, 0, 0)     # Example look-at point
        up_vector = (0, 1, 0)         # Default up vector (y-axis)

        self.visualization = Machine3DVisualization(components, connections, camera_position, look_at_point, up_vector)
        self.setCentralWidget(self.visualization)

def run_visualization(components, connections, camera_position, look_at_point):
    app = QApplication(sys.argv)
    window = MainWindow(components, connections)
    window.visualization.camera_position = camera_position
    window.visualization.look_at_point = look_at_point
    window.show()
    sys.exit(app.exec())

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
    
    #placing the component in the 3D space:
    component1.position = (0, 0, 0)
    component2.position = (2, 0, 0)
    component3.position = (4, 0, 0)


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
    assembler.add_connection(component1, component2, "hinge", hinge_dof, relative_position1=(0, 1, 2), relative_position2=(1, 0, 0.5))
    assembler.add_connection(component2, component3, "slider", slider_dof, relative_position1=(0, 0, 2.5), relative_position2=(0, 3, 0))
    assembler.calculate_dynamics(1)

    connections = assembler.connections
    components = machine.components

    # Example camera and look-at settings
    camera_position = (10, 10, 10)
    look_at_point = (0, 0, 0)

    # Run the visualization
    run_visualization(components, connections, camera_position, look_at_point)

