
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import math
from machine_component import MachineComponent
from assembler import Assembler
from machine import Machine
import numpy as np

class Machine3DVisualization(QOpenGLWidget):
    def __init__(self, machine, camera_position=(0, 0, 10), look_at_point=(0, 0, 0), camera_up_vector=(0, 0, 1), parent=None):
        super().__init__(parent)
        self.components = machine.components
        self.connections = machine.connections
        self.camera_position = camera_position
        self.look_at_point = look_at_point
        self.camera_up_vector = camera_up_vector

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
            *self.camera_up_vector          # Up vector
        )

        glColor3f(0.9, 0.6, 0.2)  # Set drawing color to yellow-orange

        # Draw components as cylinders
        for component in self.components:
            self.draw_cylinder(position = component.position, radius=0.5, height=1, upvector = component.upvector)

        # Draw connections as lines from component positions to relative positions
        glBegin(GL_LINES)
        for conn in self.connections:
            component1_name = conn['component1']
            component2_name = conn['component2']
            for component in self.components:
                if component.name == component1_name:
                    component1 = component
            for component in self.components:
                if component.name == component2_name:
                    component2 = component
            component1_pos = component1.position
            component2_pos = component2.position

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

    def draw_cylinder(self, position, radius, height, upvector):
        num_segments = 12  # Number of segments to approximate the circular base
        half_height = height / 2.0

        # Normalize the upvector
        upvector = np.array(upvector)
        upvector = upvector / np.linalg.norm(upvector)

        # Default cylinder direction (along the z-axis)
        default_dir = np.array([0, 0, 1])

        # Calculate the rotation axis and angle
        rotation_axis = np.cross(default_dir, upvector)
        rotation_angle = np.arccos(np.dot(default_dir, upvector))

        # Convert the rotation axis and angle to degrees
        rotation_angle_degrees = np.degrees(rotation_angle)

        # Apply rotation to align cylinder with the upvector
        glPushMatrix()
        glTranslatef(position[0], position[1], position[2])
        if np.linalg.norm(rotation_axis) > 1e-6:  # Avoid invalid rotation if axis is zero
            glRotatef(rotation_angle_degrees, rotation_axis[0], rotation_axis[1], rotation_axis[2])

        # Draw the top and bottom circles
        for z in [-half_height, half_height]:
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0, z)  # Center of the circle
            for i in range(num_segments + 1):
                angle = 2 * math.pi * i / num_segments
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                glVertex3f(x, y, z)
            glEnd()

        # Draw the side of the cylinder
        glBegin(GL_QUAD_STRIP)
        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, -half_height)
            glVertex3f(x, y, half_height)
        glEnd()

        # Restore the previous matrix state
        glPopMatrix()

class AnimationSceneWidget(QWidget):
    def __init__(self, machine, time_interval, total_time, camera_position=(0, 0, 10), look_at_point=(0, 0, 0)):
        super().__init__()
        self.time_interval = time_interval
        self.total_time = total_time
        self.current_time = 0

        self.visualization = Machine3DVisualization(machine, camera_position, look_at_point)
        
        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.visualization)

        # Add buttons
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.play_button.clicked.connect(self.start_animation)
        self.stop_button.clicked.connect(self.stop_animation)
        
        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Set up the timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)

    def start_animation(self):
        self.timer.start(int(self.time_interval * 1000))  # Start the timer with time_interval in milliseconds

    def stop_animation(self):
        self.timer.stop()  # Stop the timer

    def update_animation(self):
        if self.current_time < self.total_time:
            self.current_time += self.time_interval
            #assembler.calculate_dynamics(self.time_interval)
            self.visualization.update()  # Repaint the visualization
        else:
            self.timer.stop()  # Stop the animation when the total time is reached

class DirectAnimationWidget(QWidget):
    def __init__(self, machine, time_interval, total_time, camera_position=(0, 0, 10), look_at_point=(0, 0, 0), positions = [], upvectors = []):
        super().__init__()
        self.positions = positions
        self.upvectors = upvectors
        #self.components = components
        #self.connections = connections
        self.time_interval = time_interval
        self.total_time = total_time
        self.current_time = 0

        self.visualization = Machine3DVisualization(machine, camera_position, look_at_point)
        
        # Create the layout
        layout = QVBoxLayout()
        layout.addWidget(self.visualization)

        # Add buttons
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.play_button.clicked.connect(self.start_animation)
        self.stop_button.clicked.connect(self.stop_animation)
        
        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Set up the timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)

    def start_animation(self):
        self.timer.start(int(self.time_interval * 1000))  # Start the timer with time_interval in milliseconds

    def stop_animation(self):
        self.timer.stop()  # Stop the timer

    def update_animation(self):
        if self.current_time < self.total_time:
            position = self.positions[int(self.current_time)]
            upvector = self.upvectors[int(self.current_time)]

            for component in machine.components:
                component.position = position[component.name]
                component.upvector = upvector[component.name]

            self.current_time += self.time_interval
            self.visualization.update()  # Repaint the visualization
        else:
            self.timer.stop()  # Stop the animation when the total time is reached

class MainWindow(QMainWindow):
    def __init__(self, machine, time_interval, total_time, positions, upvectors):
        super().__init__()
        self.setWindowTitle("3D Machine Animation")
        self.setGeometry(100, 100, 800, 600)

        self.animation_widget = DirectAnimationWidget(machine, time_interval, total_time, positions, upvectors)
        #self.animation_widget = AnimationSceneWidget(machine, time_interval, total_time)
        self.setCentralWidget(self.animation_widget)

def run_animation(machine, time_interval, total_time, camera_position, look_at_point, positions, upvectors):
    app = QApplication(sys.argv)
    window = MainWindow(machine, time_interval, total_time, positions, upvectors)
    window.animation_widget.visualization.camera_position = camera_position
    window.animation_widget.visualization.look_at_point = look_at_point
    window.animation_widget.positions = positions
    window.animation_widget.upvectors = upvectors
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
    
    # Placing the component in the 3D space
    component1.position = (0, 0, 0)
    component2.position = (0, 0, 0)
    component3.position = (0, 0, 0)

    
    # Add components to machine
    machine.add_component(component1)
    machine.add_component(component2)
    machine.add_component(component3)
    
    # Define degrees of freedom
    hinge_dof = {'rotation': ['z']}
    slider_dof = {'translation': ['x']}

    # Add connections with DOF and relative positions
    machine.add_connection(component1, component2, "hinge", hinge_dof, relative_position1=(0, 0, 1), relative_position2=(0, 1, 0))
    machine.add_connection(component2, component3, "slider", slider_dof, relative_position1=(2, 0, 0), relative_position2=(0, 0, 2))
    component1.apply_force("init1", (-0.1, 0, 0),(0, 0, 1), 4)
    component2.apply_force("init2", (0, 0, 0.1),(1, 0, 0), 2)
    connections = machine.connections
    components = machine.components

    # Example camera and look-at settings
    camera_position = (20, 20, 20)
    look_at_point = (0, 0, 0)
    positions, upvectors = machine.simulate(10)
    
    print(positions)
    # Run the animation
    run_animation(machine, time_interval=1, total_time=10, camera_position=camera_position, look_at_point=look_at_point, positions=positions, upvectors=upvectors)
