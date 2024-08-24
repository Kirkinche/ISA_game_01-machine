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
            }

    
    for component_name, component in component_library.items():
        component.cost = market_library["components"].get(component_name, 100)  # Assign cost and set a default

    return component_library
