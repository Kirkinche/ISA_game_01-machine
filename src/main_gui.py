# main_gui.py

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QScrollArea, QListWidget, QListWidgetItem, QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QFileDialog
from PyQt6.QtCore import QTimer
from main_mechanical import MechanicalSystemManager

class MechanicalSystemGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mechanical System Manager")
        self.setGeometry(100, 100, 400, 300)
        self.simulation_running = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_sensor_data)
       
        # Initialize mechanical system manager
        self.manager = MechanicalSystemManager()
        
        # Create main widget and layout
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout(self.main_widget)

        # Machine selection
        self.machine_label = QLabel("Select Machine:", self)
        self.layout.addWidget(self.machine_label)
        
        self.machine_combo = QComboBox(self)
        self.layout.addWidget(self.machine_combo)
        
        # Buttons
        self.initialize_button = QPushButton("Initialize Machine", self)
        self.initialize_button.clicked.connect(self.initialize_machine)
        self.layout.addWidget(self.initialize_button)

        self.view_components_button = QPushButton("View Components", self)
        self.view_components_button.clicked.connect(self.view_components)
        self.layout.addWidget(self.view_components_button)

        self.run_simulation_button = QPushButton("Run Simulation", self)
        self.run_simulation_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(self.run_simulation_button)
        
        self.stop_simulation_button = QPushButton("Stop Simulation", self)
        self.stop_simulation_button.clicked.connect(self.stop_simulation)
        self.layout.addWidget(self.stop_simulation_button)       

        self.modify_component_button = QPushButton("Modify Component", self)
        self.modify_component_button.clicked.connect(self.modify_component)
        self.layout.addWidget(self.modify_component_button)

        self.display_sensors_button = QPushButton("Display Sensor Data", self)
        self.display_sensors_button.clicked.connect(self.display_sensors)
        self.layout.addWidget(self.display_sensors_button)

        # Add Save and Load buttons
        self.save_button = QPushButton("Save Machine Data", self)
        self.save_button.clicked.connect(self.save_machine_data)
        self.layout.addWidget(self.save_button)

        self.load_button = QPushButton("Load Machine Data", self)
        self.load_button.clicked.connect(self.load_machine_data)
        self.layout.addWidget(self.load_button)
        self.output_label = QLabel("", self)
        self.layout.addWidget(self.output_label)

        # Scroll area for displaying components
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_area_widget)
        self.scroll_area.setMinimumHeight(100)  # Set minimum height
        self.scroll_area.setMaximumHeight(200)  # Set maximum height
        self.layout.addWidget(self.scroll_area)

        self.refresh_machine_list()

    def refresh_machine_list(self):
        # Clear and update the machine combo box with valid machine names
        self.machine_combo.clear()
        valid_machine_names = machine_components.keys()  # Assuming machine_components is imported
        self.machine_combo.addItems(valid_machine_names)

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

        # Check if the scroll_area_widget already has a layout
        if self.scroll_area_widget.layout() is not None:
            # Clear the existing layout
            for i in reversed(range(self.scroll_area_widget.layout().count())):
                widget_to_remove = self.scroll_area_widget.layout().itemAt(i).widget()
                self.scroll_area_widget.layout().removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)
        else:
            # If no layout exists, create a new one
            self.scroll_layout = QVBoxLayout(self.scroll_area_widget)
            self.scroll_area_widget.setLayout(self.scroll_layout)

        # Add components to the layout
        for component in components:
            label = QLabel(component, self)
            self.scroll_area_widget.layout().addWidget(label)

        self.output_label.setText(f"Components in '{machine_name}' displayed.")

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
        if not self.simulation_running:
            self.simulation_running = True
            self.manager.run_simulation(machine_name, 10)
            self.timer.start(1000)  # Update sensor data every second
            self.output_label.setText(f"Simulation started for machine '{machine_name}'.")
        else:
            self.output_label.setText("Simulation already running.")

    def stop_simulation(self):
        if self.simulation_running:
            self.simulation_running = False
            self.timer.stop()
            self.output_label.setText("Simulation stopped.")
        else:
            self.output_label.setText("No simulation running.")
    
    def update_sensor_data(self):
        machine_name = self.machine_combo.currentText()
        sensor_data = self.manager.get_sensor_data(machine_name)
        if sensor_data:
            sensor_text = []
            for key, values in sensor_data.items():
                if values:  # Check if the list is not empty
                    sensor_text.append(f"{key.capitalize()}: {values[-1]}")
                else:
                    sensor_text.append(f"{key.capitalize()}: No data available")
            self.output_label.setText(f"Sensor Data for '{machine_name}':\n" + "\n".join(sensor_text))
        else:
            self.output_label.setText(f"No sensor data available for '{machine_name}'.")
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
            self.output_label.setText(f"Machine data loaded from {file_path}.")
        else:
            self.output_label.setText("No file selected for loading.")
            
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
    
if __name__ == "__main__":
    import sys
    from machine_library import machine_components  # Ensure machine_components is imported here
    app = QApplication(sys.argv)
    window = MechanicalSystemGUI()
    window.show()
    sys.exit(app.exec())