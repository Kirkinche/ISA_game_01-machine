# Library of component with Machine_component
from machine_component import MachineComponent

def initialize_component_library():
    component_library = {
        "gears": {
            "small_gear": MachineComponent("Small Gear"),
            "medium_gear": MachineComponent("Medium Gear"),
            "large_gear": MachineComponent("Large Gear")
        },
        "bearings": {
            "small_bearing": MachineComponent("Small Bearing"),
            "medium_bearing": MachineComponent("Medium Bearing"),
            "large_bearing": MachineComponent("Large Bearing")
        },
        "springs": {
            "small_spring": MachineComponent("Small Spring"),
            "medium_spring": MachineComponent("Medium Spring"),
            "large_spring": MachineComponent("Large Spring")
        },
        "plates": {
            "thin_plate": MachineComponent("Thin Plate"),
            "medium_plate": MachineComponent("Medium Plate"),
            "thick_plate": MachineComponent("Thick Plate")
        },
        "shafts": {
            "small_shaft": MachineComponent("Small Shaft"),
            "medium_shaft": MachineComponent("Medium Shaft"),
            "large_shaft": MachineComponent("Large Shaft")
        },
        "bolts": {
            "small_bolt": MachineComponent("Small Bolt"),
            "medium_bolt": MachineComponent("Medium Bolt"),
            "large_bolt": MachineComponent("Large Bolt")
        },
        "pulleys": {
            "small_pulley": MachineComponent("Small Pulley"),
            "medium_pulley": MachineComponent("Medium Pulley"),
            "large_pulley": MachineComponent("Large Pulley")
        },
        "couplings": {
            "rigid_coupling": MachineComponent("Rigid Coupling"),
            "flexible_coupling": MachineComponent("Flexible Coupling")
        },
        "motors": {
            "small_electric_motor": MachineComponent("Small Electric Motor"),
            "medium_electric_motor": MachineComponent("Medium Electric Motor"),
            "large_electric_motor": MachineComponent("Large Electric Motor"),
            "small_hydraulic_motor": MachineComponent("Small Hydraulic Motor"),
            "medium_hydraulic_motor": MachineComponent("Medium Hydraulic Motor"),
            "large_hydraulic_motor": MachineComponent("Large Hydraulic Motor")
        },
        "belts": {
            "narrow_belt": MachineComponent("Narrow Belt"),
            "wide_belt": MachineComponent("Wide Belt")
        },
        "screws": {
            "short_screw": MachineComponent("Short Screw"),
            "long_screw": MachineComponent("Long Screw")
        },
        "washers": {
            "small_washer": MachineComponent("Small Washer"),
            "large_washer": MachineComponent("Large Washer")
        },
        "nuts": {
            "small_nut": MachineComponent("Small Nut"),
            "large_nut": MachineComponent("Large Nut")
        },
        "disks": {
            "thin_disk": MachineComponent("Thin Disk"),
            "thick_disk": MachineComponent("Thick Disk")
        },
        "cylinders": {
            "short_cylinder": MachineComponent("Short Cylinder"),
            "long_cylinder": MachineComponent("Long Cylinder")
        }
    }

    # Initializing attributes for components
    
    # Gears
    component_library["gears"]["small_gear"].mass = 0.5  # kg
    component_library["gears"]["small_gear"].material = "steel"
    component_library["gears"]["small_gear"].center_of_mass = (0, 0, 0.05)
    component_library["gears"]["small_gear"].surface_area = 0.01  # m^2
    component_library["gears"]["small_gear"].volume = 0.001  # m^3

    component_library["gears"]["medium_gear"].mass = 1.5  # kg
    component_library["gears"]["medium_gear"].material = "steel"
    component_library["gears"]["medium_gear"].center_of_mass = (0, 0, 0.07)
    component_library["gears"]["medium_gear"].surface_area = 0.015  # m^2
    component_library["gears"]["medium_gear"].volume = 0.0015  # m^3

    component_library["gears"]["large_gear"].mass = 3.0  # kg
    component_library["gears"]["large_gear"].material = "steel"
    component_library["gears"]["large_gear"].center_of_mass = (0, 0, 0.1)
    component_library["gears"]["large_gear"].surface_area = 0.02  # m^2
    component_library["gears"]["large_gear"].volume = 0.002  # m^3

    # Bearings
    component_library["bearings"]["small_bearing"].mass = 0.3  # kg
    component_library["bearings"]["small_bearing"].material = "titanium"
    component_library["bearings"]["small_bearing"].center_of_mass = (0, 0, 0.02)
    component_library["bearings"]["small_bearing"].surface_area = 0.005  # m^2
    component_library["bearings"]["small_bearing"].volume = 0.0005  # m^3

    component_library["bearings"]["medium_bearing"].mass = 0.6  # kg
    component_library["bearings"]["medium_bearing"].material = "titanium"
    component_library["bearings"]["medium_bearing"].center_of_mass = (0, 0, 0.04)
    component_library["bearings"]["medium_bearing"].surface_area = 0.01  # m^2
    component_library["bearings"]["medium_bearing"].volume = 0.001  # m^3

    component_library["bearings"]["large_bearing"].mass = 1.2  # kg
    component_library["bearings"]["large_bearing"].material = "titanium"
    component_library["bearings"]["large_bearing"].center_of_mass = (0, 0, 0.06)
    component_library["bearings"]["large_bearing"].surface_area = 0.015  # m^2
    component_library["bearings"]["large_bearing"].volume = 0.0015  # m^3

    # Springs
    component_library["springs"]["small_spring"].mass = 0.1  # kg
    component_library["springs"]["small_spring"].material = "steel"
    component_library["springs"]["small_spring"].center_of_mass = (0, 0, 0.02)
    component_library["springs"]["small_spring"].surface_area = 0.002  # m^2
    component_library["springs"]["small_spring"].volume = 0.0002  # m^3
    component_library["springs"]["small_spring"].stiffness = 5000  # N/m

    component_library["springs"]["medium_spring"].mass = 0.3  # kg
    component_library["springs"]["medium_spring"].material = "steel"
    component_library["springs"]["medium_spring"].center_of_mass = (0, 0, 0.03)
    component_library["springs"]["medium_spring"].surface_area = 0.003  # m^2
    component_library["springs"]["medium_spring"].volume = 0.0003  # m^3
    component_library["springs"]["medium_spring"].stiffness = 10000  # N/m

    component_library["springs"]["large_spring"].mass = 0.7  # kg
    component_library["springs"]["large_spring"].material = "steel"
    component_library["springs"]["large_spring"].center_of_mass = (0, 0, 0.04)
    component_library["springs"]["large_spring"].surface_area = 0.005  # m^2
    component_library["springs"]["large_spring"].volume = 0.0005  # m^3
    component_library["springs"]["large_spring"].stiffness = 20000  # N/m

    # Motors (Electric and Hydraulic)
    component_library["motors"]["small_electric_motor"].mass = 2.0  # kg
    component_library["motors"]["small_electric_motor"].material = "steel"
    component_library["motors"]["small_electric_motor"].center_of_mass = (0, 0, 0.1)
    component_library["motors"]["small_electric_motor"].surface_area = 0.02  # m^2
    component_library["motors"]["small_electric_motor"].volume = 0.002  # m^3

    component_library["motors"]["medium_electric_motor"].mass = 5.0  # kg
    component_library["motors"]["medium_electric_motor"].material = "steel"
    component_library["motors"]["medium_electric_motor"].center_of_mass = (0, 0, 0.15)
    component_library["motors"]["medium_electric_motor"].surface_area = 0.04  # m^2
    component_library["motors"]["medium_electric_motor"].volume = 0.004  # m^3

    component_library["motors"]["large_electric_motor"].mass = 10.0  # kg
    component_library["motors"]["large_electric_motor"].material = "steel"
    component_library["motors"]["large_electric_motor"].center_of_mass = (0, 0, 0.2)
    component_library["motors"]["large_electric_motor"].surface_area = 0.08  # m^2
    component_library["motors"]["large_electric_motor"].volume = 0.008  # m^3

    component_library["motors"]["small_hydraulic_motor"].mass = 3.0  # kg
    component_library["motors"]["small_hydraulic_motor"].material = "steel"
    component_library["motors"]["small_hydraulic_motor"].center_of_mass = (0, 0, 0.12)
    component_library["motors"]["small_hydraulic_motor"].surface_area = 0.03  # m^2
    component_library["motors"]["small_hydraulic_motor"].volume = 0.003  # m^3

    component_library["motors"]["medium_hydraulic_motor"].mass = 7.0  # kg
    component_library["motors"]["medium_hydraulic_motor"].material = "steel"
    component_library["motors"]["medium_hydraulic_motor"].center_of_mass = (0, 0, 0.17)
    component_library["motors"]["medium_hydraulic_motor"].surface_area = 0.05  # m^2
    component_library["motors"]["medium_hydraulic_motor"].volume = 0.005  # m^3

    component_library["motors"]["large_hydraulic_motor"].mass = 12.0  # kg
    component_library["motors"]["large_hydraulic_motor"].material = "steel"
    component_library["motors"]["large_hydraulic_motor"].center_of_mass = (0, 0, 0.22)
    component_library["motors"]["large_hydraulic_motor"].surface_area = 0.09  # m^2
    component_library["motors"]["large_hydraulic_motor"].volume = 0.009  # m^3

    component_library["belts"]["small_belt"].mass = 0.5  # kg
    component_library["belts"]["small_belt"].material = "steel"
    component_library["belts"]["small_belt"].center_of_mass = (0, 0, 0.05)
    component_library["belts"]["small_belt"].surface_area = 0.01  # m^2
    component_library["belts"]["small_belt"].volume = 0.001  # m^3

    component_library["belts"]["wide_belt"].mass = 1.0  # kg
    component_library["belts"]["wide_belt"].material = "steel"
    component_library["belts"]["wide_belt"].center_of_mass = (0, 0, 0.1)
    component_library["belts"]["wide_belt"].surface_area = 0.02  # m^2
    component_library["belts"]["wide_belt"].volume = 0.002  # m^3

    component_library["screws"]["short_screw"].mass = 0.1  # kg
    component_library["screws"]["short_screw"].material = "steel"
    component_library["screws"]["short_screw"].center_of_mass = (0, 0, 0.02)
    component_library["screws"]["short_screw"].surface_area = 0.002  # m^2
    component_library["screws"]["short_screw"].volume = 0.0002  # m^3

    component_library["screws"]["long_screw"].mass = 0.3  # kg
    component_library["screws"]["long_screw"].material = "steel"
    component_library["screws"]["long_screw"].center_of_mass = (0, 0, 0.04)
    component_library["screws"]["long_screw"].surface_area = 0.004  # m^2
    component_library["screws"]["long_screw"].volume = 0.0004  # m^3

    component_library["washers"]["small_washer"].mass = 0.5  # kg
    component_library["washers"]["small_washer"].material = "steel"
    component_library["washers"]["small_washer"].center_of_mass = (0, 0, 0.05)
    component_library["washers"]["small_washer"].surface_area = 0.01  # m^2
    component_library["washers"]["small_washer"].volume = 0.001  # m^3

    component_library["washers"]["large_washer"].mass = 1.0  # kg
    component_library["washers"]["large_washer"].material = "steel"
    component_library["washers"]["large_washer"].center_of_mass = (0, 0, 0.1)
    component_library["washers"]["large_washer"].surface_area = 0.02  # m^2
    component_library["washers"]["large_washer"].volume = 0.002  # m^3

    component_library["nuts"]["small_nut"].mass = 0.1  # kg
    component_library["nuts"]["small_nut"].material = "steel"
    component_library["nuts"]["small_nut"].center_of_mass = (0, 0, 0.02)
    component_library["nuts"]["small_nut"].surface_area = 0.002  # m^2
    component_library["nuts"]["small_nut"].volume = 0.0002  # m^3

    component_library["nuts"]["large_nut"].mass = 0.3  # kg
    component_library["nuts"]["large_nut"].material = "steel"
    component_library["nuts"]["large_nut"].center_of_mass = (0, 0, 0.04)
    component_library["nuts"]["large_nut"].surface_area = 0.004  # m^2
    component_library["nuts"]["large_nut"].volume = 0.0004  # m^3

    component_library["disks"]["thin_disk"].mass = 0.1  # kg
    component_library["disks"]["thin_disk"].material = "steel"
    component_library["disks"]["thin_disk"].center_of_mass = (0, 0, 0.02)
    component_library["disks"]["thin_disk"].surface_area = 0.002  # m^2
    component_library["disks"]["thin_disk"].volume = 0.0002  # m^3

    component_library["disks"]["thick_disk"].mass = 0.3  # kg
    component_library["disks"]["thick_disk"].material = "steel"
    component_library["disks"]["thick_disk"].center_of_mass = (0, 0, 0.04)
    component_library["disks"]["thick_disk"].surface_area = 0.004  # m^2
    component_library["disks"]["thick_disk"].volume = 0.0004  # m^3

    component_library["cylinders"]["short_cylinder"].mass = 0.1  # kg
    component_library["cylinders"]["short_cylinder"].material = "steel"
    component_library["cylinders"]["short_cylinder"].center_of_mass = (0, 0, 0.02)
    component_library["cylinders"]["short_cylinder"].surface_area = 0.002  # m^2
    component_library["cylinders"]["short_cylinder"].volume = 0.0002  # m^3

    component_library["cylinders"]["long_cylinder"].mass = 0.3  # kg
    component_library["cylinders"]["long_cylinder"].material = "steel"
    component_library["cylinders"]["long_cylinder"].center_of_mass = (0, 0, 0.04)
    component_library["cylinders"]["long_cylinder"].surface_area = 0.004  # m^2
    component_library["cylinders"]["long_cylinder"].volume = 0.0004  # m^3
       
    return component_library
