# Library of component with Machine_component
from machine_component import MachineComponent
from market_library import market_library

def initialize_component_library():
    component_library = {
        # Gears
        "small_gear": MachineComponent("Small Gear"),
        "medium_gear": MachineComponent("Medium Gear"),
        "large_gear": MachineComponent("Large Gear"),
        
        # Bearings
        "small_bearing": MachineComponent("Small Bearing"),
        "medium_bearing": MachineComponent("Medium Bearing"),
        "large_bearing": MachineComponent("Large Bearing"),
        
        # Springs
        "small_spring": MachineComponent("Small Spring"),
        "medium_spring": MachineComponent("Medium Spring"),
        "large_spring": MachineComponent("Large Spring"),
        
        # Plates
        "thin_plate": MachineComponent("Thin Plate"),
        "medium_plate": MachineComponent("Medium Plate"),
        "thick_plate": MachineComponent("Thick Plate"),
        
        # Shafts
        "small_shaft": MachineComponent("Small Shaft"),
        "medium_shaft": MachineComponent("Medium Shaft"),
        "large_shaft": MachineComponent("Large Shaft"),
        
        # Bolts
        "small_bolt": MachineComponent("Small Bolt"),
        "medium_bolt": MachineComponent("Medium Bolt"),
        "large_bolt": MachineComponent("Large Bolt"),
        
        # Pulleys
        "small_pulley": MachineComponent("Small Pulley"),
        "medium_pulley": MachineComponent("Medium Pulley"),
        "large_pulley": MachineComponent("Large Pulley"),
        
        # Couplings
        "rigid_coupling": MachineComponent("Rigid Coupling"),
        "flexible_coupling": MachineComponent("Flexible Coupling"),
        
        # Motors (Electric and Hydraulic)
        "small_electric_motor": MachineComponent("Small Electric Motor"),
        "medium_electric_motor": MachineComponent("Medium Electric Motor"),
        "large_electric_motor": MachineComponent("Large Electric Motor"),
        "small_hydraulic_motor": MachineComponent("Small Hydraulic Motor"),
        "medium_hydraulic_motor": MachineComponent("Medium Hydraulic Motor"),
        "large_hydraulic_motor": MachineComponent("Large Hydraulic Motor"),
        
        # Belts
        "narrow_belt": MachineComponent("Narrow Belt"),
        "wide_belt": MachineComponent("Wide Belt"),
        
        # Screws
        "short_screw": MachineComponent("Short Screw"),
        "long_screw": MachineComponent("Long Screw"),
        
        # Washers
        "small_washer": MachineComponent("Small Washer"),
        "large_washer": MachineComponent("Large Washer"),
        
        # Nuts
        "small_nut": MachineComponent("Small Nut"),
        "large_nut": MachineComponent("Large Nut"),
        
        # Disks
        "thin_disk": MachineComponent("Thin Disk"),
        "thick_disk": MachineComponent("Thick Disk"),
        
        # Cylinders
        "short_cylinder": MachineComponent("Short Cylinder"),
        "long_cylinder": MachineComponent("Long Cylinder"),
        
        # Additional Components
        "pneumatic_cylinder": MachineComponent("Pneumatic Cylinder"),
        "hydraulic_pump": MachineComponent("Hydraulic Pump"),
        "electrical_generator": MachineComponent("Electrical Generator"),
        "heat_exchanger": MachineComponent("Heat Exchanger"),
        "compressor": MachineComponent("Compressor"),
        "valve": MachineComponent("Valve"),
        "fan": MachineComponent("Fan"),
        "conveyor_belt": MachineComponent("Conveyor Belt"),
        "sensor": MachineComponent("Sensor"),
        "actuator": MachineComponent("Actuator"),
        "gearbox": MachineComponent("Gearbox"),

        "bearing_block": MachineComponent("Bearing Block"),
        "spring_block": MachineComponent("Spring Block"),
        "plate_block": MachineComponent("Plate Block"),
        "shaft_block": MachineComponent("Shaft Block"),
        "bolt_block": MachineComponent("Bolt Block"),
        "pulley_block": MachineComponent("Pulley Block"),
        "coupling_block": MachineComponent("Coupling Block"),
        "motor_block": MachineComponent("Motor Block"),
        "belt_block": MachineComponent("Belt Block"),
        "screw_block": MachineComponent("Screw Block"),
        "washer_block": MachineComponent("Washer Block"),
        "nut_block": MachineComponent("Nut Block"),
        "disk_block": MachineComponent("Disk Block"),
        "cylinder_block": MachineComponent("Cylinder Block"),
        "pneumatic_cylinder_block": MachineComponent("Pneumatic Cylinder Block"),
        "hydraulic_pump_block": MachineComponent("Hydraulic Pump Block"),
        "electrical_generator_block": MachineComponent("Electrical Generator Block"),
        "heat_exchanger_block": MachineComponent("Heat Exchanger Block"),
        "compressor_block": MachineComponent("Compressor Block"),
        "valve_block": MachineComponent("Valve Block"),
        "fan_block": MachineComponent("Fan Block"),
        "conveyor_belt_block": MachineComponent("Conveyor Belt Block"),
        "sensor_block": MachineComponent("Sensor Block"),
        "actuator_block": MachineComponent("Actuator Block"),
        "gearbox_block": MachineComponent("Gearbox Block"),
        "seal": MachineComponent("Seal"),
        "gasket": MachineComponent("Gasket"),
        "electrical_wiring": MachineComponent("Electrical Wiring"),
        "connector": MachineComponent("Connector"),
        "lubrication_pump": MachineComponent("Lubrication Pump"),
        "lubrication_line": MachineComponent("Lubrication Line"),
        "cooling_fan": MachineComponent("Cooling Fan"),
        "temperature_sensor": MachineComponent("Temperature Sensor"),
        "pressure_sensor": MachineComponent("Pressure Sensor"),
        "plc_controller": MachineComponent("PLC Controller"),
        "hmi_display": MachineComponent("HMI Display"),
        "mounting_bracket": MachineComponent("Mounting Bracket"),
        "clamp": MachineComponent("Clamp"),
        "filter": MachineComponent("Filter"),
        "cooling_fin": MachineComponent("Cooling Fin"),
        "radiator": MachineComponent("Radiator"),
        }

    
    for component_name, component in component_library.items():
        component.cost = market_library["components"].get(component_name, 100)
        
    for component_name, component in component_library.items():
        component.mass = physical_parameter_component_library[component_name]["mass"]
        component.radius = physical_parameter_component_library[component_name]["radius"]
        component.length = physical_parameter_component_library[component_name]["length"]
        component.volume = physical_parameter_component_library[component_name]["volume"]

    return component_library

physical_parameter_component_library = {'small_gear': {'mass': 1, 'radius': 0.5, 'length': 1, 'volume': 0.1},
    'medium_gear': {'mass': 2, 'radius': 0.7, 'length': 1.5, 'volume': 0.2},
    'large_gear': {'mass': 3, 'radius': 1, 'length': 2, 'volume': 0.3},
    'small_bearing': {'mass': 0.5, 'radius': 0.3, 'length': 0.5, 'volume': 0.05},
    'medium_bearing': {'mass': 1, 'radius': 0.5, 'length': 1, 'volume': 0.1},
    'large_bearing': {'mass': 2, 'radius': 0.7, 'length': 1.5, 'volume': 0.2},
    'small_spring': {'mass': 0.2, 'radius': 0.2, 'length': 1, 'volume': 0.05},
    'medium_spring': {'mass': 0.5, 'radius': 0.3, 'length': 1.5, 'volume': 0.1},
    'large_spring': {'mass': 1, 'radius': 0.5, 'length': 2, 'volume': 0.15},
    'thin_plate': {'mass': 2, 'radius': 0.7, 'length': 0.5, 'volume': 0.5},
    'medium_plate': {'mass': 5, 'radius': 1, 'length': 1, 'volume': 1},
    'thick_plate': {'mass': 10, 'radius': 1.5, 'length': 1.5, 'volume': 2},
    'small_shaft': {'mass': 1, 'radius': 0.3, 'length': 1, 'volume': 0.2},
    'medium_shaft': {'mass': 2, 'radius': 0.5, 'length': 1.5, 'volume': 0.4},
    'large_shaft': {'mass': 3, 'radius': 0.7, 'length': 2, 'volume': 0.6},
    'small_bolt': {'mass': 0.1, 'radius': 0.05, 'length': 0.2, 'volume': 0.01},
    'medium_bolt': {'mass': 0.2, 'radius': 0.1, 'length': 0.3, 'volume': 0.02},
    'large_bolt': {'mass': 0.3, 'radius': 0.15, 'length': 0.4, 'volume': 0.03},
    'small_pulley': {'mass': 0.5, 'radius': 0.2, 'length': 0.5, 'volume': 0.1},
    'medium_pulley': {'mass': 1, 'radius': 0.3, 'length': 0.7, 'volume': 0.15},
    'large_pulley': {'mass': 2, 'radius': 0.5, 'length': 1, 'volume': 0.2},
    'rigid_coupling': {'mass': 1, 'radius': 0.5, 'length': 0.5, 'volume': 0.1},
    'flexible_coupling': {'mass': 1.5, 'radius': 0.7, 'length': 0.7,'volume': 0.15},
    'small_electric_motor': {'mass': 5, 'radius': 1, 'length': 1, 'volume': 1.5},
    'medium_electric_motor': {'mass': 10, 'radius': 1.5, 'length': 1.5, 'volume': 2.5},
    'large_electric_motor': {'mass': 15, 'radius': 2, 'length': 2, 'volume': 3.5},
    'small_hydraulic_motor': {'mass': 6, 'radius': 1, 'length': 1, 'volume': 1.6},
    'medium_hydraulic_motor': {'mass': 12,
    'radius': 1.5,
    'length': 1.5,
    'volume': 2.6},
    'large_hydraulic_motor': {'mass': 18,
    'radius': 2,
    'length': 2,
    'volume': 3.6},
    'narrow_belt': {'mass': 0.3, 'radius': 0.1, 'length': 1, 'volume': 0.05},
    'wide_belt': {'mass': 0.5, 'radius': 0.15, 'length': 1.5, 'volume': 0.1},
    'short_screw': {'mass': 0.05, 'radius': 0.02, 'length': 0.1, 'volume': 0.005},
    'long_screw': {'mass': 0.1, 'radius': 0.03, 'length': 0.2, 'volume': 0.01},
    'small_washer': {'mass': 0.01,
    'radius': 0.01,
    'length': 0.05,
    'volume': 0.001},
    'large_washer': {'mass': 0.02,
    'radius': 0.02,
    'length': 0.1,
    'volume': 0.002},
    'small_nut': {'mass': 0.01, 'radius': 0.01, 'length': 0.05, 'volume': 0.001},
    'large_nut': {'mass': 0.02, 'radius': 0.02, 'length': 0.1, 'volume': 0.002},
    'thin_disk': {'mass': 0.3, 'radius': 0.5, 'length': 0.05, 'volume': 0.1},
    'thick_disk': {'mass': 0.5, 'radius': 0.7, 'length': 0.1, 'volume': 0.2},
    'short_cylinder': {'mass': 0.5, 'radius': 0.5, 'length': 1, 'volume': 0.2},
    'long_cylinder': {'mass': 1, 'radius': 0.7, 'length': 1.5, 'volume': 0.4},
    'bearing_block': {'mass': 2, 'radius': 0.7, 'length': 1, 'volume': 0.5},
    'spring_block': {'mass': 1.5, 'radius': 0.5, 'length': 0.8, 'volume': 0.4},
    'plate_block': {'mass': 3, 'radius': 0.9, 'length': 1.2, 'volume': 0.6},
    'shaft_block': {'mass': 2.5, 'radius': 0.8, 'length': 1.5, 'volume': 0.7},
    'bolt_block': {'mass': 1, 'radius': 0.4, 'length': 0.7, 'volume': 0.2},
    "pulley_block": {"mass": 2.5, "radius": 0.8, "length": 1, "volume": 0.4},
    "coupling_block": {"mass": 1.8, "radius": 0.7, "length": 1.2, "volume": 0.3},
    "motor_block": {"mass": 10, "radius": 1.5, "length": 2, "volume": 1.2},
    "belt_block": {"mass": 0.7, "radius": 0.2, "length": 2, "volume": 0.1},
    "screw_block": {"mass": 1, "radius": 0.1, "length": 0.5, "volume": 0.05},
    "washer_block": {"mass": 0.3, "radius": 0.1, "length": 0.2, "volume": 0.02},
    "nut_block": {"mass": 0.2, "radius": 0.05, "length": 0.1, "volume": 0.01},
    "disk_block": {"mass": 1.5, "radius": 0.7, "length": 0.5, "volume": 0.25},
    "cylinder_block": {"mass": 3, "radius": 1, "length": 1.5, "volume": 0.75},
    "pneumatic_cylinder_block": {"mass": 4, "radius": 1.2, "length": 2, "volume": 0.9},
    "hydraulic_pump_block": {"mass": 8, "radius": 1.5, "length": 2, "volume": 1.2},
    "electrical_generator_block": {"mass": 15, "radius": 2.5, "length": 3, "volume": 2},
    "heat_exchanger_block": {"mass": 12, "radius": 1.8, "length": 2.5, "volume": 1.5},
    "compressor_block": {"mass": 10, "radius": 1.6, "length": 2.2, "volume": 1.3},
    "valve_block": {"mass": 5, "radius": 1, "length": 1.5, "volume": 0.75},
    "fan_block": {"mass": 3, "radius": 0.8, "length": 1, "volume": 0.4},
    "conveyor_belt_block": {"mass": 4.5, "radius": 1, "length": 3, "volume": 0.5},
    "sensor_block": {"mass": 0.5, "radius": 0.1, "length": 0.2, "volume": 0.05},
    "actuator_block": {"mass": 2, "radius": 0.5, "length": 1, "volume": 0.2},
    "gearbox_block": {"mass": 6, "radius": 1.2, "length": 1.8, "volume": 1},    
    'seal': {'mass': 0.05, 'radius': 0.03, 'length': 0.1, 'volume': 0.005},
    'gasket': {'mass': 0.1, 'radius': 0.05, 'length': 0.1, 'volume': 0.01},
    'electrical_wiring': {'mass': 0.5,
    'radius': 0.02,
    'length': 10,
    'volume': 0.1},
    'connector': {'mass': 0.05, 'radius': 0.02, 'length': 0.05, 'volume': 0.002},
    'lubrication_pump': {'mass': 3, 'radius': 0.5, 'length': 1, 'volume': 0.5},
    'lubrication_line': {'mass': 1, 'radius': 0.02, 'length': 5, 'volume': 0.2},
    'cooling_fan': {'mass': 2, 'radius': 0.5, 'length': 0.3, 'volume': 0.15},
    'temperature_sensor': {'mass': 0.1,
    'radius': 0.03,
    'length': 0.1,
    'volume': 0.01},
    'pressure_sensor': {'mass': 0.2,
    'radius': 0.05,
    'length': 0.15,
    'volume': 0.02},
    'plc_controller': {'mass': 1.5, 'radius': 0.4, 'length': 0.5, 'volume': 0.3},
    'hmi_display': {'mass': 0.8, 'radius': 0.2, 'length': 0.3, 'volume': 0.1},
    'mounting_bracket': {'mass': 0.5,
    'radius': 0.05,
    'length': 0.5,
    'volume': 0.05},
    'clamp': {'mass': 0.2, 'radius': 0.05, 'length': 0.1, 'volume': 0.01},
    'filter': {'mass': 0.7, 'radius': 0.1, 'length': 0.5, 'volume': 0.1},
    'cooling_fin': {'mass': 0.5, 'radius': 0.05, 'length': 0.2, 'volume': 0.02},
    'radiator': {'mass': 5, 'radius': 1, 'length': 0.5, 'volume': 1.5}}