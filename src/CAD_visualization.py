# CAD_visualization.py

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from machine_component import MachineComponent
from stl import mesh

class CADVisualizer(FigureCanvas):
    def __init__(self, component, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.ax = fig.add_subplot(111, projection='3d')
        super().__init__(fig)
        self.setParent(parent)

        self.component = component

        if self.component.mesh is None:
            raise ValueError("Mesh data is not available for this component.")
        
        self.vertices = self.component.mesh["vertices"]
        self.faces = self.component.mesh["faces"]

        self.plot_mesh()

    def plot_mesh(self):
        # Plot the mesh
        self.ax.add_collection3d(Poly3DCollection(self.vertices[self.faces], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Setting the aspect ratio of the plot to be equal
        self.ax.set_box_aspect([1, 1, 1])

        # Autoscale the plot
        scale = self.vertices.flatten('F')
        self.ax.auto_scale_xyz(scale, scale, scale)

        self.draw()


class MeshGenerator:
    @staticmethod
    def create_cube_mesh():
        # Create a simple cube mesh
        vertices = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [1, 1, 0],
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 1, 1],
            [0, 1, 1]
        ])

        faces = np.array([
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [2, 3, 7, 6],
            [0, 3, 7, 4],
            [1, 2, 6, 5]
        ])

        return {"vertices": vertices, "faces": faces}


if __name__ == '__main__':
    # Create a component
    component = MachineComponent("TestComponent")

    # Generate a mesh using MeshGenerator
    mesh = MeshGenerator.create_cube_mesh()

    # Assign the generated mesh to the component
    component.set_mesh(mesh)

    # Visualize the component
    visualizer = CADVisualizer(component)
    visualizer.visualize()
