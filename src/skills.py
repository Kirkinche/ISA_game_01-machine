# src/skills.py

skills = {
    "combat": {
        "Power Strike": {
            "attribute": "strength",
            "description": "Deal extra damage based on strength.",
            "effect": lambda strength: strength * 2
        },
        "Quick Attack": {
            "attribute": "dexterity",
            "description": "Increased chance to hit.",
            "effect": lambda dexterity: dexterity * 1.5
        },
        "Magic Bolt": {
            "attribute": "intelligence",
            "description": "Ranged magic attack.",
            "effect": lambda intelligence: intelligence * 2
        }
    },
    "trading": {
        "Bartering": {
            "attribute": "charisma",
            "description": "Negotiate better prices.",
            "effect": lambda charisma: charisma * 1.2
        },
        "Market Analysis": {
            "attribute": "intelligence",
            "description": "Predict market trends and find rare items.",
            "effect": lambda intelligence: intelligence * 1.5
        }
    },
    "social": {
        "Charming": {
            "attribute": "charisma",
            "description": "Influence NPCs for better deals or information.",
            "effect": lambda charisma: charisma * 1.2
        },
        "Intimidation": {
            "attribute": "strength",
            "description": "Force NPCs to comply or provide information.",
            "effect": lambda strength: strength * 1.2
        },
        "Persuasion": {
            "attribute": "wisdom",
            "description": "Convince NPCs to join your cause.",
            "effect": lambda wisdom: wisdom * 1.2
        }
    },
    "crafting": {
        "Crafting": {
            "attribute": ["dexterity", "intelligence"],
            "description": "Create items with gathered resources.",
            "effect": lambda dexterity, intelligence: (dexterity + intelligence) / 2
        },
        "Building": {
            "attribute": ["strength", "constitution"],
            "description": "Construct buildings or defenses.",
            "effect": lambda strength, constitution: (strength + constitution) / 2
        },
        "Alchemy": {
            "attribute": ["intelligence", "wisdom"],
            "description": "Brew potions and elixirs.",
            "effect": lambda intelligence, wisdom: (intelligence + wisdom) / 2
        }
    },
    "exploration": {
        "Foraging": {
            "attribute": "wisdom",
            "description": "Find herbs and food in the wild.",
            "effect": lambda wisdom: wisdom * 1.2
        },
        "Scouting": {
            "attribute": "dexterity",
            "description": "Explore new areas and avoid danger.",
            "effect": lambda dexterity: dexterity * 1.2
        },
        "Fishing": {
            "attribute": ["dexterity", "wisdom"],
            "description": "Catch fish for food or trade.",
            "effect": lambda dexterity, wisdom: (dexterity + wisdom) / 2
        }
    },
    "magic": {
        "Spellcasting": {
            "attribute": "intelligence",
            "description": "Use spells for combat and utility.",
            "effect": lambda intelligence: intelligence * 2
        },
        "Enchanting": {
            "attribute": ["intelligence", "wisdom"],
            "description": "Imbue items with magical properties.",
            "effect": lambda intelligence, wisdom: (intelligence + wisdom) / 2
        },
        "Potion Brewing": {
            "attribute": ["intelligence", "wisdom"],
            "description": "Create potions with various effects.",
            "effect": lambda intelligence, wisdom: (intelligence + wisdom) / 2
        }
    },
    "leadership": {
        "Commanding": {
            "attribute": "charisma",
            "description": "Lead party members in combat or missions.",
            "effect": lambda charisma: charisma * 1.5
        },
        "Strategizing": {
            "attribute": "intelligence",
            "description": "Plan and execute complex strategies.",
            "effect": lambda intelligence: intelligence * 1.5
        }
    },
    "resource_management": {
        "Mining": {
            "attribute": "strength",
            "description": "Extract minerals and gems.",
            "effect": lambda strength: strength * 1.2
        },
        "Logging": {
            "attribute": "strength",
            "description": "Harvest wood.",
            "effect": lambda strength: strength * 1.2
        },
        "Farming": {
            "attribute": "wisdom",
            "description": "Grow crops and raise animals.",
            "effect": lambda wisdom: wisdom * 1.2
        }
    },
    "entertainment": {
        "Performing": {
            "attribute": "charisma",
            "description": "Entertain NPCs and gain their favor.",
            "effect": lambda charisma: charisma * 1.2
        },
        "Gambling": {
            "attribute": ["luck", "charisma"],
            "description": "Win money or items through games of chance.",
            "effect": lambda luck, charisma: (luck + charisma) / 2
        }
    }
}
