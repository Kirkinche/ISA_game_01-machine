import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from machine_component import MachineComponent
from stl import mesh


class CADVisualizer:
    def __init__(self, component):
        self.component = component

    def visualize(self):
        if self.component.mesh is None:
            raise ValueError("Mesh data is not available for this component.")
        
        vertices = self.component.mesh["vertices"]
        faces = self.component.mesh["faces"]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the mesh
        ax.add_collection3d(Poly3DCollection(vertices[faces], facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        # Setting the aspect ratio of the plot to be equal
        ax.set_box_aspect([1, 1, 1])

        # Autoscale the plot
        scale = vertices.flatten('F')
        ax.auto_scale_xyz(scale, scale, scale)

        plt.show()

        def import_mesh_from_file(self, file_path):
            # Implement the logic to import mesh data from a file
            # This could be a .stl, .obj, or any other format reader
            # make a automatic detection of file format between .stl, .obj, .npy etc.
            # For now, let's assume it's a .npy file with a dictionary containing "vertices" and "faces" keys
            
            # Using an existing stl file:
            #your_mesh = mesh.Mesh.from_file(file_path)

            return np.load(file_path, allow_pickle=True).item()
        

import numpy as np

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
