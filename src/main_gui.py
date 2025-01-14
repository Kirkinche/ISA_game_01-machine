# main_gui.py
# this platform is for creating robotic machine, adding components to the machine, 
# specify them and performing calculation onto the machine such as total mass, power consumption, heat generated, noise generated, etc.



from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QHBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QScrollArea, QListWidget, QListWidgetItem, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QFileDialog
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QAction, QIcon
from main_mechanical import MechanicalSystemManager
from CAD_visualization import CADVisualizer
from machine_component import MachineComponent
from machine import Machine


class MechanicalSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Robotic System Manager")
        self.setGeometry(100, 100, 800, 600)

        # Initialize mechanical system manager
        self.manager = MechanicalSystemManager()
        self.machine_name_input = ""

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
        New_machine_action = QAction("New Machine", self)
        New_machine_action.triggered.connect(self.new_machine)
        Add_component_action = QAction("Add Component", self)
        Add_component_action.triggered.connect(self.add_component)        
        View_Components_action = QAction("View Components", self)
        View_Components_action.triggered.connect(self.view_components)
        View_machine_profile_action = QAction("View Machine Profile", self)
        View_machine_profile_action.triggered.connect(self.view_machine_profile)
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
        machine_menu.addAction(New_machine_action)
        machine_menu.addAction(initialize_machine_action)
        machine_menu.addAction(Add_component_action)
        machine_menu.addAction(View_Components_action)
        machine_menu.addAction(View_machine_profile_action)
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

    def new_machine(self):
        dialog = MachineNameDialog()
        
        if dialog.exec() == QDialog.DialogCode.Accepted:  # This will show the dialog modally
            machine_name = dialog.machine_name_input.text()  # Accessing the input text directly
            self.manager.add_machine(machine_name)
            print(self.manager.machines)  # Debugging line
        self.refresh_machine_list()

    def add_component(self):
        dialog = ComponentNameDialog()
        machine_name = self.machine_combo.currentText()
        if dialog.exec() == QDialog.DialogCode.Accepted:  # This will show the dialog modally
            component_name = dialog.component_name_input.text()  # Accessing the input text directly
            machine = self.manager.machines[machine_name]
            if machine:
                component = MachineComponent(component_name)  # Create a new component instance
                machine.add_component(component)  # Add the component to the machine
                self.populate_component_selector()  # Refresh the component selector
                self.output_label.setText(f"Component '{component_name}' added to '{machine_name}'.")
                self.view_components()
                print(self.manager.machines)  # Debugging line
            else:
                self.output_label.setText(f"Machine '{machine_name}' not found.")  # Display an error message

    def initialize_machine(self):
        machine_name = self.machine_combo.currentText()
        if machine_name:
            self.manager.initialize_machine(machine_name)
            self.output_label.setText(f"Machine '{machine_name}' initialized.")
            self.refresh_machine_list()
        else:
            self.output_label.setText("No machine selected.")
            
            
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

    def view_machine_profile(self):
        machine_name = self.machine_combo.currentText()
        profile_text = ""
        if machine_name in self.manager.machines:  # Check if the machine exists
            machine = self.manager.machines[machine_name]  # Get the machine instance
            profile_text = f"Machine Name: {machine.name}\n"  # Start the profile text with the machine name
            machine_total_mass = machine.calculate_total_mass()
            time_period = 3600 # Example time period in seconds (1 hour)
            energy_cost_per_kwh = 0.1641 #  energy cost per kWh in USD on 2024-09-08
            machine_operating_cost = machine.calculate_operating_cost(1,energy_cost_per_kwh)
            machine_power_consumption = machine.calculate_power_consumption(time_period)
            machine_manufacturing_cost = machine.calculate_manufacturing_cost()
        else:
            raise(TypeError("Machine not found"))
        profile_text += f"Total Mass: {machine_total_mass} kg\n"  # Add the total mass to the profile text
        profile_text += f"Operating Cost per hour and 0.1641 USD per kWh: {machine_operating_cost} USD\n"  # Add the operating cost to the profile text
        profile_text += f"Power Consumption: {machine_power_consumption} W\n"  # Add the power consumption to the profile text
        profile_text += f"Manufacturing Cost: {machine_manufacturing_cost} USD\n"  # Add the manufacturing cost to the profile text
        
        #display the machine data in the Data Display Dialog:
        dialog = DataDisplayDialog(profile_text)  # Create a new instance of the dialog
        dialog.exec()  # Show the dialog modally
        


    def modify_component(self):
        machine_name = self.machine_combo.currentText()
        components = self.manager.display_machine_components(machine_name)
        if components:
            component_name = self.component_combo.currentText()
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
        # Assuming machine_components is imported and combine them with the machine names from the manager 
        init_machine_names = machine_components.keys() 
        self.machine_combo.addItems(init_machine_names)
        new_machine_names = self.manager.machines.keys() 
        self.machine_combo.addItems(new_machine_names)
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

class DataDisplayDialog(QDialog):
    def __init__(self, profile_text):
        super().__init__()
        self.setWindowTitle("Data Display")
        self.profile_text = profile_text
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel(self.profile_text))
        self.setLayout(self.layout)        



class MachineNameDialog(QDialog): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Machine Name")
        self.layout = QVBoxLayout(self)
        #input box to enter machine name:
        self.machine_name_input = QLineEdit(self)
        self.layout.addWidget(self.machine_name_input)
        #ok and cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)
        
    def get_machine_name(self):
        return self.machine_name_input.text()


class ComponentNameDialog(QDialog): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Component Name")
        self.layout = QVBoxLayout(self)
        #input box to enter component name:
        self.component_name_input = QLineEdit(self)
        self.layout.addWidget(self.component_name_input)
        #ok and cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)
        self.setLayout(self.layout)
        
    def get_component_name(self):
        return self.component_name_input.text()

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
        tuple_attributes = ['position', 'upvector', 'velocity', 'net_force', 'torque', 'acceleration', 'momentum']
        
        for attr_name in dir(component):
            if not callable(getattr(component, attr_name)) and not attr_name.startswith("__"):
                attr_value = getattr(component, attr_name)
                
                # Handle tuple attributes (like position, velocity)
                if attr_name in tuple_attributes:
                    for i, label in enumerate(['x', 'y', 'z']):
                        line_edit = QLineEdit(str(attr_value[i]), self)
                        self.form_layout.addRow(QLabel(f"{attr_name} ({label}):"), line_edit)
                        self.inputs[f"{attr_name}_{label}"] = line_edit
                else:
                    # For scalar attributes, use a single field
                    label = QLabel(attr_name.replace("_", " ").capitalize() + ":")
                    line_edit = QLineEdit(str(attr_value), self)
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
        """Get the new properties as a dictionary and convert to the correct data type."""
        new_properties = {}
        tuple_attributes = ['position', 'upvector', 'velocity', 'net_force', 'torque', 'acceleration', 'momentum']
        
        # Initialize empty lists for the tuple attributes
        for attr in tuple_attributes:
            new_properties[attr] = []

        for attr_name in self.inputs:
            # Check if the input belongs to a tuple attribute (like position, velocity, etc.)
            for tuple_attr in tuple_attributes:
                if tuple_attr in attr_name:
                    # Extract the value for this component (x, y, or z)
                    try:
                        new_properties[tuple_attr].append(float(self.inputs[attr_name].text()))
                    except ValueError:
                        raise ValueError(f"Invalid input for {attr_name}. Must be a float.")
            
            # Convert the accumulated lists for tuple attributes into tuples
            for attr in tuple_attributes:
                if len(new_properties[attr]) == 3:
                    new_properties[attr] = tuple(new_properties[attr])

        # Handle other scalar attributes
        for attr_name in self.inputs:
            if not any(attr in attr_name for attr in tuple_attributes):
                value = self.inputs[attr_name].text()
                try:
                    if '.' in value:
                        new_properties[attr_name] = float(value)
                    else:
                        new_properties[attr_name] = int(value)
                except ValueError:
                    new_properties[attr_name] = value  # Keep as string if it can't be converted

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
