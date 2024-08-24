from machine import Machine
from component_library import initialize_component_library
from machine_component import MachineComponent
machine_components = {
    "electric_motor": {
        "motor_block": 1,
        "gearbox_block": 1,
        "bearing_block": 2,
        "spring_block": 2,
        "shaft_block": 1,
        "bolt_block": 10,
        "pulley_block": 1,
        "coupling_block": 1,
        "belt_block": 1,
        "screw_block": 20,
        "washer_block": 20,
        "nut_block": 20,
        "disk_block": 1,
        "seal": 2,
        "gasket": 2,
        "electrical_wiring": 1,
        "connector": 4,
        "cooling_fan": 1,
        "temperature_sensor": 1,
        "pressure_sensor": 1,
        "mounting_bracket": 4,
        "clamp": 4
    },
    "hydraulic_pump": {
        "hydraulic_pump_block": 1,
        "coupling_block": 1,
        "shaft_block": 1,
        "bolt_block": 8,
        "screw_block": 12,
        "washer_block": 12,
        "nut_block": 12,
        "valve_block": 4,
        "cylinder_block": 2,
        "seal": 4,
        "gasket": 4,
        "lubrication_pump": 1,
        "lubrication_line": 4,
        "filter": 2,
        "pressure_sensor": 1,
        "plc_controller": 1,
        "mounting_bracket": 4,
        "clamp": 4
    },
    "heat_exchanger": {
        "heat_exchanger_block": 1,
        "plate_block": 10,
        "bolt_block": 10,
        "screw_block": 20,
        "washer_block": 20,
        "nut_block": 20,
        "gasket": 10,
        "seal": 4,
        "temperature_sensor": 2,
        "pressure_sensor": 1,
        "filter": 1,
        "mounting_bracket": 6,
        "clamp": 6
    },
    "compressor": {
        "compressor_block": 1,
        "valve_block": 4,
        "fan_block": 1,
        "shaft_block": 1,
        "bearing_block": 2,
        "coupling_block": 1,
        "bolt_block": 10,
        "screw_block": 20,
        "washer_block": 20,
        "nut_block": 20,
        "seal": 4,
        "gasket": 4,
        "lubrication_pump": 1,
        "lubrication_line": 4,
        "filter": 2,
        "cooling_fan": 1,
        "radiator": 1,
        "temperature_sensor": 2,
        "pressure_sensor": 1,
        "plc_controller": 1,
        "mounting_bracket": 6,
        "clamp": 6
    },
    "centrifugal_pump": {
        "impeller": 1,
        "pump_casing": 1,
        "shaft_block": 1,
        "bearing_block": 2,
        "seal": 2,
        "coupling_block": 1,
        "motor_block": 1,
        "gasket": 2,
        "bolt_block": 10,
        "pressure_sensor": 1,
        "flow_sensor": 1,
        "mounting_bracket": 4,
        "clamp": 4
    },
    "industrial_robot_arm": {
        "servo_motor": 6,
        "gearbox_block": 6,
        "control_unit": 1,
        "joint": 6,
        "bearing_block": 6,
        "electrical_wiring": 1,
        "connector": 12,
        "position_sensor": 6,
        "force_sensor": 1,
        "mounting_bracket": 6,
        "cooling_fan": 1,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "wind_turbine": {
        "rotor_blade": 3,
        "nacelle": 1,
        "gearbox_block": 1,
        "generator_block": 1,
        "tower": 1,
        "bearing_block": 3,
        "yaw_drive": 1,
        "control_system": 1,
        "wind_speed_sensor": 1,
        "position_sensor": 1,
        "temperature_sensor": 1,
        "cooling_fan": 2,
        "bolt_block": 30,
        "screw_block": 40,
        "washer_block": 40,
        "nut_block": 40
    },
    "steam_turbine": {
        "turbine_blade": 1,
        "rotor": 1,
        "stator": 1,
        "bearing_block": 2,
        "seal": 4,
        "gasket": 4,
        "lubrication_pump": 1,
        "cooling_system": 1,
        "generator_block": 1,
        "control_system": 1,
        "temperature_sensor": 2,
        "pressure_sensor": 2,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "industrial_conveyor_belt_system": {
        "conveyor_belt": 1,
        "roller": 10,
        "motor_block": 1,
        "gearbox_block": 1,
        "pulley_block": 2,
        "bearing_block": 4,
        "position_sensor": 2,
        "speed_sensor": 2,
        "mounting_bracket": 10,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "injection_molding_machine": {
        "injection_unit": 1,
        "mold": 1,
        "clamping_unit": 1,
        "hydraulic_system": 1,
        "motor_block": 1,
        "heater_band": 2,
        "control_system": 1,
        "temperature_sensor": 2,
        "pressure_sensor": 1,
        "cooling_system": 1,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "cnc_machine": {
        "spindle": 1,
        "cutting_tool": 5,
        "servo_motor": 3,
        "cnc_controller": 1,
        "ball_screw": 3,
        "bearing_block": 3,
        "cooling_system": 1,
        "position_sensor": 3,
        "force_sensor": 1,
        "electrical_wiring": 1,
        "connector": 6,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "air_compressor": {
        "compressor_pump": 1,
        "motor_block": 1,
        "air_tank": 1,
        "pressure_switch": 1,
        "safety_valve": 1,
        "cooling_fan": 1,
        "filter": 2,
        "control_panel": 1,
        "temperature_sensor": 1,
        "pressure_sensor": 1,
        "mounting_bracket": 4,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "solar_panel_system": {
        "solar_panel": 10,
        "inverter": 1,
        "mounting_system": 1,
        "electrical_wiring": 1,
        "connector": 8,
        "light_sensor": 1,
        "temperature_sensor": 1,
        "charge_controller": 1,
        "battery": 4,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    },
    "packaging_machine": {
        "conveyor_system": 1,
        "sealing_mechanism": 1,
        "cutting_tool": 1,
        "control_unit": 1,
        "position_sensor": 2,
        "temperature_sensor": 1,
        "actuator_block": 2,
        "bearing_block": 4,
        "lubrication_pump": 1,
        "mounting_bracket": 4,
        "bolt_block": 20,
        "screw_block": 30,
        "washer_block": 30,
        "nut_block": 30
    }
}


# ABC Analysis function
def abc_analysis_machine(machine_name, machine_components, market_library):
    # Get the market value of the machine
    total_cost = market_library["machines"][machine_name]
    
    # Get component costs from the market library, adjusted by quantity
    component_costs = {
        comp: market_library["components"][comp] * qty 
        for comp, qty in machine_components[machine_name].items()
    }

    # Initialize a set to track added components
    added_components = set()

    # Sort components by total cost in descending order
    sorted_components = sorted(component_costs.items(), key=lambda item: item[1], reverse=True)
    
    cumulative_cost = 0
    a_components = []
    b_components = []
    c_components = []

    for component, cost in sorted_components:
        # Logic gate: only add the component if it hasn't been added yet
        if component not in added_components:
            cumulative_cost += cost
            percentage = cumulative_cost / total_cost

            if percentage <= 0.7:
                a_components.append(component)
            elif percentage <= 0.9:
                b_components.append(component)
            else:
                c_components.append(component)
            
            # Mark this component as added
            added_components.add(component)
    
    return a_components, b_components, c_components

def initialize_machine_with_abc(machine_name, machine_components, market_library):
    # Perform ABC analysis
    a_components, b_components, _ = abc_analysis_machine(machine_name, machine_components, market_library)

    # Initialize the machine
    machine = Machine(machine_name)

    # Include both A and B category components
    for component in a_components + b_components:
        quantity = machine_components[machine_name][component]
        for _ in range(quantity):
            machine.add_component(MachineComponent(component))
    
    return machine
def initialize_machine_with_all_components(machine_name, machine_components, market_library):
    # Initialize the machine
    machine = Machine(machine_name)

    # Add all components from the machine_components dictionary
    for component, quantity in machine_components[machine_name].items():
        for _ in range(quantity):
            machine.add_component(MachineComponent(component))
    
    return machine

def initialize_full_machine_library(machine_components, market_library):
    machine_library = {
        "electric_motor": initialize_machine_with_all_components("electric_motor", machine_components, market_library),
        "hydraulic_pump": initialize_machine_with_all_components("hydraulic_pump", machine_components, market_library),
        "heat_exchanger": initialize_machine_with_all_components("heat_exchanger", machine_components, market_library),
        "compressor": initialize_machine_with_all_components("compressor", machine_components, market_library),
        "centrifugal_pump": initialize_machine_with_all_components("centrifugal_pump", machine_components, market_library),
        "industrial_robot_arm": initialize_machine_with_all_components("industrial_robot_arm", machine_components, market_library),
        "wind_turbine": initialize_machine_with_all_components("wind_turbine", machine_components, market_library),
        "steam_turbine": initialize_machine_with_all_components("steam_turbine", machine_components, market_library),
        "industrial_conveyor_belt_system": initialize_machine_with_all_components("industrial_conveyor_belt_system", machine_components, market_library),
        "injection_molding_machine": initialize_machine_with_all_components("injection_molding_machine", machine_components, market_library),
        "cnc_machine": initialize_machine_with_all_components("cnc_machine", machine_components, market_library),
        "air_compressor": initialize_machine_with_all_components("air_compressor", machine_components, market_library),
        "solar_panel_system": initialize_machine_with_all_components("solar_panel_system", machine_components, market_library),
        "packaging_machine": initialize_machine_with_all_components("packaging_machine", machine_components, market_library)
    }
    
    return machine_library

# Initialize machine library function
def initialize_abc_machine_library(market_library):
    # Initialize Electric Motor with A and B components
    electric_motor = initialize_machine_with_abc("electric_motor", machine_components, market_library)
    
    # Initialize other machines similarly
    hydraulic_pump = initialize_machine_with_abc("hydraulic_pump", machine_components, market_library)
    heat_exchanger = initialize_machine_with_abc("heat_exchanger", machine_components, market_library)
    compressor = initialize_machine_with_abc("compressor", machine_components, market_library)
    
    # Add the machines to the machine library
    machine_library = {
        "electric_motor": electric_motor,
        "hydraulic_pump": hydraulic_pump,
        "heat_exchanger": heat_exchanger,
        "compressor": compressor
    }

    return machine_library
