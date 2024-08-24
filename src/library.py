#library for all modules, market_library
from market_library import market_library

# Material library with physical properties
material_lib = {
    "steel": {
        "density": 7850,            # kg/m^3
        "resistance": 200e9,        # Pa
        "wear": 1e-8,               # m^3/m
        "friction": 0.6,            # friction coeficient dimensionless
        "thermal_expansion": 1.2e-5,    # 1/K
        "fatigue_limit": 250e6  # Pa
        },
    "copper": {"density": 8960, "resistance": 167.8e9, "wear": 2e-9, "friction": 0.4, "thermal_expansion": 1.7e-5, "fatigue_limit": 120e6},
    "bronze": {"density": 8800, "resistance": 100e9, "wear": 3e-9, "friction": 0.5, "thermal_expansion": 1.5e-5, "fatigue_limit": 100e6},
    "aluminium": {"density": 2700, "resistance": 69e9, "wear": 4e-9, "friction": 0.6, "thermal_expansion": 2.3e-5, "fatigue_limit": 100e6},
    "titanium": {"density": 4500, "resistance": 110e9, "wear": 5e-9, "friction": 0.5, "thermal_expansion": 2.0e-5, "fatigue_limit": 150e6},
    "carbon_fiber": {"density": 1800, "resistance": 200e9, "wear": 6e-9, "friction": 0.4, "thermal_expansion": 1.0e-5, "fatigue_limit": 200e6},
    "glass": {"density": 2500, "resistance": 70e9, "wear": 7e-9, "friction": 0.9, "thermal_expansion": 1.5e-5, "fatigue_limit": 150e6},
    "rubber": {"density": 1200, "resistance": 100e6, "wear": 8e-9, "friction": 1.0, "thermal_expansion": 1.2e-5, "fatigue_limit": 100e6},
    "plastic": {"density": 1000, "resistance": 3e9, "wear": 9e-9, "friction": 0.8, "thermal_expansion": 1.0e-5, "fatigue_limit": 50e6},
    "wood": {"density": 700, "resistance": 1e9, "wear": 10e-9, "friction": 0.7, "thermal_expansion": 1.1e-5, "fatigue_limit": 30e6},
    "concrete": {"density": 2400, "resistance": 20e9, "wear": 11e-9, "friction": 0.6, "thermal_expansion": 1.3e-5, "fatigue_limit": 50e6},
    "granite": {"density": 2700, "resistance": 100e9, "wear": 12e-9, "friction": 0.6, "thermal_expansion": 1.4e-5, "fatigue_limit": 70e6},
    "marble": {"density": 2500, "resistance": 70e9, "wear": 13e-9, "friction": 0.6, "thermal_expansion": 1.5e-5, "fatigue_limit": 100e6},
    "nickel": {"density": 8900, "resistance": 200e9, "wear": 14e-9, "friction": 0.5, "thermal_expansion": 1.3e-5, "fatigue_limit": 200e6},
    "stainless_steel": {"density": 7850, "resistance": 200e9, "wear": 15e-9, "friction": 0.4, "thermal_expansion": 1.2e-5, "fatigue_limit": 250e6},
    "tungsten": {"density": 19300, "resistance": 410e9, "wear": 16e-9, "friction": 0.5, "thermal_expansion": 4.5e-5, "fatigue_limit": 300e6},
    "silver": {"density": 10700, "resistance": 83e9, "wear": 17e-9, "friction": 0.5, "thermal_expansion": 1.8e-5, "fatigue_limit": 150e6},
    "gold": {"density": 19300, "resistance": 79e9, "wear": 18e-9, "friction": 0.5, "thermal_expansion": 1.4e-5, "fatigue_limit": 200e6},
    "polyurethane": {"density": 1200, "resistance": 50e6, "wear": 19e-9, "friction": 0.9, "thermal_expansion": 1.2e-5, "fatigue_limit": 100e6},
    "polycarbonate": {"density": 1200, "resistance": 150e6, "wear": 20e-9, "friction": 0.8, "thermal_expansion": 1.0e-5, "fatigue_limit": 150e6},
    "kevlar": {"density": 1440, "resistance": 3.4e9, "wear": 21e-9, "friction": 0.7, "thermal_expansion": 1.1e-5, "fatigue_limit": 200e6},
    "graphite": {"density": 2260, "resistance": 10e9, "wear": 22e-9, "friction": 0.3, "thermal_expansion": 7.0e-5, "fatigue_limit": 50e6},
    "diamond": {"density": 3500, "resistance": 1.2e12, "wear": 23e-9, "friction": 0.2, "thermal_expansion": 1.0e-5, "fatigue_limit": 1000e6},
    "graphene": {"density": 770, "resistance": 1.0e11, "wear": 24e-9, "friction": 0.1, "thermal_expansion": 0.7e-5, "fatigue_limit": 2000e6}
}

