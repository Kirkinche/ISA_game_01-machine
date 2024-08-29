# main_gui.py

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QScrollArea, QListWidget, QListWidgetItem, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QFileDialog
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction, QIcon
from main_mechanical import MechanicalSystemManager
from CAD_visualization import CADVisualizer



class MechanicalSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechanical System Manager")
        self.setGeometry(100, 100, 800, 600)

        # Initialize mechanical system manager
        self.manager = MechanicalSystemManager()

        # Create main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Machine and Component Selection
        self.machine_label = QLabel("Select Machine:", self)
        self.layout.addWidget(self.machine_label)

        self.machine_combo = QComboBox(self)
        self.machine_combo.currentIndexChanged.connect(self.populate_component_selector)
        self.layout.addWidget(self.machine_combo)

        self.component_label = QLabel("Select Component:", self)
        self.layout.addWidget(self.component_label)

        self.component_combo = QComboBox(self)
        self.layout.addWidget(self.component_combo)

        # Scroll Area for viewing components
        self.scroll_area = QScrollArea(self)
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_layout = QVBoxLayout(self.scroll_area_widget)
        self.layout.addWidget(self.scroll_area)

        # adding the actions
        initialize_machine_action = QAction("Initialize Machine", self)
        initialize_machine_action.triggered.connect(self.initialize_machine)
        View_Components_action = QAction("View Components", self)
        View_Components_action.triggered.connect(self.view_components)
        Run_Simulation_action = QAction("Run Simulation", self)
        Run_Simulation_action.triggered.connect(self.run_simulation)
        Modify_Component_action = QAction("Modify Component", self)
        Modify_Component_action.triggered.connect(self.modify_component)
        Display_Sensor_Data_action = QAction("Display Sensor Data", self)
        Display_Sensor_Data_action.triggered.connect(self.display_sensors)
        Force_on_Component_action = QAction("Force on Component", self)
        Force_on_Component_action.triggered.connect(self.force_on_component)
        Save_Machine_Data_action = QAction("Save Machine Data", self)
        Save_Machine_Data_action.triggered.connect(self.save_machine_data)
        Load_Machine_Data_action = QAction("Load Machine Data", self)
        Load_Machine_Data_action.triggered.connect(self.load_machine_data)

        # adding a menu bar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction(Save_Machine_Data_action)
        file_menu.addAction(Load_Machine_Data_action)

        machine_menu = menu_bar.addMenu("Machine")
        machine_menu.addAction(initialize_machine_action)
        machine_menu.addAction(View_Components_action)
        machine_menu.addAction(Run_Simulation_action)

        component_menu = menu_bar.addMenu("Component")
        component_menu.addAction(Modify_Component_action)
        component_menu.addAction(Display_Sensor_Data_action)
        component_menu.addAction(Force_on_Component_action)
        
        self.output_label = QLabel("", self)
        self.layout.addWidget(self.output_label)

        # Visualization Panel
        self.visualization_panel = None  # To hold the CADVisualizer instance

        self.refresh_machine_list()

    def populate_component_selector(self):
        self.component_combo.clear()  # Clear existing items
        machine_name = self.machine_combo.currentText()
        if machine_name in self.manager.machines:
            components = [component.name for component in self.manager.machines[machine_name].components]
            self.component_combo.addItems(components)

    def view_components(self):
        machine_name = self.machine_combo.currentText()
        components = self.manager.display_machine_components(machine_name)

        # Clear the existing layout
        for i in reversed(range(self.scroll_layout.count())):
            widget_to_remove = self.scroll_layout.itemAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Add components to the layout
        for component in components:
            label = QLabel(component, self)
            self.scroll_layout.addWidget(label)

        self.output_label.setText(f"Components in '{machine_name}' displayed.")

    def initialize_machine(self):
        machine_name = self.machine_combo.currentText()
        if machine_name:
            self.manager.initialize_machine(machine_name)
            self.output_label.setText(f"Machine '{machine_name}' initialized.")
            self.refresh_machine_list()
        else:
            self.output_label.setText("No machine selected.")

    def modify_component(self):
        machine_name = self.machine_combo.currentText()
        components = self.manager.display_machine_components(machine_name)
        if components:
            component_name = components[0]  # Modify the first component for simplicity
            component = self.manager.machines[machine_name].get_component_by_name(component_name)
            dialog = ComponentEditorDialog(component)
            if dialog.exec():
                new_properties = dialog.get_new_properties()
                self.manager.modify_component(machine_name, component_name, new_properties)
                self.output_label.setText(f"Component '{component_name}' updated in '{machine_name}'.")

    def display_sensors(self):
        machine_name = self.machine_combo.currentText()
        sensor_data = self.manager.get_sensor_data(machine_name)
        self.output_label.setText(f"Sensor Data for '{machine_name}': {sensor_data}")

    def run_simulation(self):
        machine_name = self.machine_combo.currentText()
        if machine_name not in self.manager.machines:
            self.manager.initialize_machine(machine_name)
        
        self.manager.run_simulation(machine_name, 10)
        self.output_label.setText(f"Simulation run for machine '{machine_name}'.")

    def save_machine_data(self):
        machine_name = self.machine_combo.currentText()
        if machine_name:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Machine Data", "", "JSON Files (*.json);;All Files (*)")
            if file_path:
                self.manager.save_machine_data(machine_name, file_path)
                self.output_label.setText(f"Machine '{machine_name}' data saved to {file_path}.")
        else:
            self.output_label.setText("No machine selected to save.")

    def load_machine_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Machine Data", "", "JSON Files (*.json);;All Files (*)")
        if file_path:
            self.manager.load_machine_data(file_path)
            self.refresh_machine_list()  # Refresh the machine list after loading new data
            self.populate_component_selector()  # Populate components after loading
            self.output_label.setText(f"Machine data loaded from {file_path}.")

    def refresh_machine_list(self):
        # Clear and update the machine combo box with valid machine names
        self.machine_combo.clear()
        valid_machine_names = machine_components.keys()  # Assuming machine_components is imported
        self.machine_combo.addItems(valid_machine_names)
        self.populate_component_selector()  # Refresh components when machines are refreshed
    
    def force_on_component(self):
        machine_name = self.machine_combo.currentText()
        component_name = self.component_combo.currentText()
        if machine_name and component_name:  # Check if both machine and component are selected
            machine = self.manager.machines[machine_name]
            component = machine.get_component_by_name(component_name)
            if component:
                dialog = ComponentForceApplicationDialog(component, self.manager, machine_name)
                dialog.exec()  # Show the dialog for force input
            else:
                self.output_label.setText(f"Component '{component_name}' not found in '{machine_name}'.")
        else:
            self.output_label.setText("Please select both a machine and a component.")

class ComponentEditorDialog(QDialog):
    def __init__(self, component):
        super().__init__()
        self.setWindowTitle(f"Edit Component: {component.name}")
        
        # Scroll area setup
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        layout = QVBoxLayout(scroll_widget)
        
        # Form layout for all component attributes
        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)
        
        # Create input fields dynamically for each attribute of the component
        self.inputs = {}
        for attr_name in dir(component):
            if not callable(getattr(component, attr_name)) and not attr_name.startswith("__"):
                label = QLabel(attr_name.replace("_", " ").capitalize() + ":")
                line_edit = QLineEdit(str(getattr(component, attr_name)), self)
                self.form_layout.addRow(label, line_edit)
                self.inputs[attr_name] = line_edit
        
        # Buttons
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Set the layout for the dialog
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

    def get_new_properties(self):
        new_properties = {}
        for attr_name, line_edit in self.inputs.items():
            try:
                new_value = float(line_edit.text())
            except ValueError:
                new_value = line_edit.text()  # If it's not a number, keep it as a string
            new_properties[attr_name] = new_value
        return new_properties

class ComponentForceApplicationDialog(QDialog):
    def __init__(self, component, manager, machine_name):
        super().__init__()
        self.setWindowTitle(f"Force Application: {component.name}")
        self.component = component
        self.manager = manager
        self.machine_name = machine_name

        # Create input fields for force name, vector, contact point, and duration
        self.force_name_input = QLineEdit(self)
        self.force_vector_input = QLineEdit(self)
        self.contact_point_input = QLineEdit(self)
        self.duration_input = QLineEdit(self)
        
        # Create button to apply the force
        self.apply_button = QPushButton("Apply Force", self)
        self.apply_button.clicked.connect(self.apply_force)

        # Layout the dialog
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Force Name:"))
        layout.addWidget(self.force_name_input)
        layout.addWidget(QLabel("Force Vector e.g. 10, 0, 0:"))
        layout.addWidget(self.force_vector_input)
        layout.addWidget(QLabel("Contact Point e.g. 0, 0, 0:"))
        layout.addWidget(self.contact_point_input)
        layout.addWidget(QLabel("Duration (seconds):"))
        layout.addWidget(self.duration_input)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def apply_force(self):
        force_name = self.force_name_input.text()
        force_vector = tuple(map(float, self.force_vector_input.text().split(',')))
        contact_point = tuple(map(float, self.contact_point_input.text().split(',')))
        duration = int(self.duration_input.text())

        self.manager.apply_force(self.machine_name, self.component.name, force_name, force_vector, contact_point, duration)
        self.close()
    

if __name__ == "__main__":
    import sys
    from machine_library import machine_components  # Ensure machine_components is imported here
    app = QApplication(sys.argv)
    window = MechanicalSystemGUI()
    window.show()
    sys.exit(app.exec())
