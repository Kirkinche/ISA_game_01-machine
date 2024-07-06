# This an physical zone map module
import numpy as np
import os, sys, random
from noise import pnoise2
# Import the procedural map module

script_directory_src2 = os.path.dirname(os.path.abspath("E:/APIs/ProductionPipeApp/src/RPG_character_utils.py"))
script_directory_src3 = os.path.dirname(os.path.abspath("E:/APIs/ProductionPipeApp/src/object_utils.py"))
script_directory_src4 = os.path.dirname(os.path.abspath("E:/APIs/ProductionPipeApp/src/resource_utils.py"))
script_directory_src5 = os.path.dirname(os.path.abspath("E:/APIs/ProductionPipeApp/src/map_variable.py"))

sys.path.append(script_directory_src2)
sys.path.append(script_directory_src3)
sys.path.append(script_directory_src4)
sys.path.append(script_directory_src5)
import RPG_character_utils 
from object_utils import MapObject
from resource_utils import InorganicResource, OrganicResource
import map_variable
from procedural_map import Map

#loading the variable of the map generation tools
terrain_matrix = map_variable.terrain_matrix
terrain_cmap = map_variable.terrain_cmap

for terrain, color in terrain_cmap.items():
    terrain_cmap[terrain] = tuple(int(color[i:i+2], 16) / 255 for i in (1, 3, 5))

symbols = map_variable.symbols
TERRAIN_OBJECTS = map_variable.TERRAIN_OBJECTS
OBJECTS_FOOTPRINTS = map_variable.OBJECTS_FOOTPRINTS
RARITY_WEIGHTS = map_variable.RARITY_WEIGHTS
HUMAN_JOBS = map_variable.HUMAN_JOBS
PET_SPECIES = map_variable.PET_SPECIES 
WILDLIFE_SPECIES = map_variable.WILDLIFE_SPECIES
JOB_ATTRIBUTES = map_variable.JOB_ATTRIBUTES
PET_ATTRIBUTES = map_variable.PET_ATTRIBUTES
WILDLIFE_ATTRIBUTES = map_variable.WILDLIFE_ATTRIBUTES
TERRAIN_RESOURCES = map_variable.TERRAIN_RESOURCES
RESOURCE_ATTRIBUTES = map_variable.RESOURCE_ATTRIBUTES
elevation_ranges = map_variable.elevation_ranges
NPC_NAMES = map_variable.NPC_NAMES

class ZoneMap:
    def __init__(self, procedural_map, selected_terrain_type):
        # Initialize attributes based on the center point of the procedural map
        size = 5
        self.procedural_map = procedural_map  # Assuming this is the procedural map object
        self.selected_terrain_type = selected_terrain_type # This the type of terrain
        self.npcs ={} # Creating an empty dictionnary to store all the npc and their location
        self.objects ={} # Creating an empty dictionnary to store all the objects and their size, location and type
        self.resources ={} # Creating an empty dictionnary to store all the resources, location and type

        # Get the value of the center point (2, 2)
        center = int((size-1)/2)
        
        # Initialize zone maps for the center and its neighbors
        self.zone_maps = {}
        directions = ["Center", "North", "South", "West", "East", "Northwest", "Northeast", "Southwest", "Southeast"]
        offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction, offset in zip(directions, offsets):
            row, col = center + offset[0], center + offset[1]
            node_value = self.procedural_map.map[row][col]
            event, probability, indoor, weather, density, water_source, presence, resources = node_value
            print(f"{direction} value:", node_value)

            # Determine the physical size based on the indoor attribute
            if indoor:
                width = random.randint(5, 25)
                length = random.randint(5, 25)
            else:
                width = random.randint(25, 125)
                length = random.randint(25, 125)

            print(f"{direction} zone size: {width} x {length} = {width*length} m2")

            # Inside the loop, initializing the physical zone map
            self.zone_maps[direction] = {
                "width": width,
                "length": length,
                "map": [[(None, None, None, None) for _ in range(width)] for _ in range(length)],
                "event": event, 
                "probability": probability,
                "indoor": indoor,
                "terrain": None,
                "weather": weather,
                "density": density,
                "water source": water_source,
                "Npc_presence": presence,
                "resources": resources
            }
        # other initialization logic
            ...
    def to_dict(self):
        print(type(self.procedural_map))
        return {
            'class_name': 'ZoneMap',
            'procedural_map': self.procedural_map.to_dict(),
            'selected_terrain_type': list(self.selected_terrain_type),
            'npcs': [npc.to_dict() for npc in self.npcs],
            'resources': {direction: {group: [res.to_dict() for res in res_list] for group, res_list in group_dict.items()} for direction, group_dict in self.resources.items()},
            'objects': [obj.to_dict() for obj in self.objects],
            'zone_maps': {direction: {key: value if key != "map" else [[list(cell) for cell in row] for row in value] for key, value in zone.items()} for direction, zone in self.zone_maps.items()},
            # ... other attributes ...
        }

    @classmethod
    def from_dict(cls, dict_obj):
        procedural_map = Map.from_dict(dict_obj['procedural_map'])
        selected_terrain_type = tuple(dict_obj['selected_terrain_type'])

        npcs = [RPG_character_utils.RPGCharacter.from_dict(npc_dict) for npc_dict in dict_obj['npcs']]
        resources = {direction: {group: [InorganicResource.from_dict(res_dict) for res_dict in res_list] for group, res_list in group_dict.items()} for direction, group_dict in dict_obj['resources'].items()}
        objects = [MapObject.from_dict(obj_dict) for obj_dict in dict_obj['objects']]

        zone_maps = {direction: {key: value if key != "map" else [[tuple(cell) for cell in row] for row in value] for key, value in zone.items()} for direction, zone in dict_obj['zone_maps'].items()}

        # Initialize a new ZoneMap object and populate its attributes
        zone_map_obj = cls(procedural_map, selected_terrain_type)
        zone_map_obj.npcs = npcs
        zone_map_obj.resources = resources
        zone_map_obj.objects = objects
        zone_map_obj.zone_maps = zone_maps
        return zone_map_obj        
    
    def generate_elevation(self, elevation_ranges):
        outdoor_terrain, indoor_terrains = self.selected_terrain_type
        # Define the elevation variation range based on the selected outdoor terrain type
        elevation_ranges = elevation_ranges 
        # Iterate through each direction and populate the "map" with elevation values
        for direction, zone_map in self.zone_maps.items():
            # Extract the dimensions, map matrix, and indoor attribute
            width = zone_map["width"]
            length = zone_map["length"]
            map_matrix = zone_map["map"]
            indoor = zone_map["indoor"]
        
            # Set elevation variation range based on indoor/outdoor
            if indoor:
                elevation_min, elevation_max = 0, 0
                indoor_terrain_type = random.choice(indoor_terrains)
                self.zone_maps[direction]["terrain"] = indoor_terrain_type
            else:
                elevation_min, elevation_max = elevation_ranges.get(outdoor_terrain, (-5, 5))
                self.zone_maps[direction]["terrain"] = outdoor_terrain

            # Iterate through the matrix and generate elevation values
            for row in range(length):
                for col in range(width):
                    elevation = random.randint(elevation_min, elevation_max)
                    # Store the elevation value in the map matrix
                    map_matrix[row][col] = (elevation, None, None, None)  # Other attributes to be filled later

            # Update the zone map with the populated map matrix
            self.zone_maps[direction]["map"] = map_matrix

    def generate_NPC(self):
        # Counter for each type of NPC
        human_count, pet_count, wildlife_count = 0, 0, 0

        # NPC types based on indoor/outdoor
        indoor_NPC_types = ["human", "pet"]
        outdoor_NPC_types = ["human", "wildlife"]

        # Iterate through each direction and populate the "map" with NPCs
        for direction, zone_map in self.zone_maps.items():
            # Extract the dimensions, map matrix, indoor attribute, and NPC presence value
            width = zone_map["width"]
            length = zone_map["length"]
            map_matrix = zone_map["map"]
            indoor = zone_map["indoor"]
            NPC_presence = zone_map["Npc_presence"]

            # Determine the NPC types based on indoor/outdoor
            NPC_types = indoor_NPC_types if indoor else outdoor_NPC_types

            # Generate NPCs based on the NPC presence value
            for i in range(NPC_presence):
                # Randomly select an NPC type
                NPC_type = random.choice(NPC_types)
                # Randomly select a position for the NPC
                row, col = random.randint(2, length - 2), random.randint(2, width - 2)
                # Extract existing attributes at the selected position
                elevation, _, _, _ = map_matrix[row][col]
                position = (row, col)

                # Create an NPC instance based on the selected type
                if NPC_type == "human":
                    gender=random.choice(["male", "female"]) 
                    name=random.choice(NPC_NAMES[gender])
                    # Randomly select a job for the human NPC
                    job = random.choice(HUMAN_JOBS)
                    npc = RPG_character_utils.NPCCharacter(NPC_type, name, gender, job)
                    npc.direction = direction
                    npc.position = position
                    # Apply job-specific attributes
                    job_attributes = JOB_ATTRIBUTES[job]
                    npc.intelligence += job_attributes.get("intelligence", 0)
                    npc.dexterity += job_attributes.get("dexterity", 0)        
                    npc.wisdom += job_attributes.get("wisdom", 0)
                    npc.luck += job_attributes.get("luck", 0)
                    npc.charm += job_attributes.get("charm", 0)
                    npc.strength += job_attributes.get("strength", 0)
                    npc.constitution += job_attributes.get("constitution", 0)
                    human_count += 1
                # ... similar logic for pet and wildlife species ...
                # Inside the generation loop, after creating the NPC instance for pets and wildlife
                elif NPC_type == "pet":
                    species = random.choice(PET_SPECIES)
                    base_height = PET_ATTRIBUTES[species]["height"]
                    base_weight = PET_ATTRIBUTES[species]["weight"]
                    lower_bound_height = max(0, base_height - 5)
                    lower_bound_weight = max(0, base_weight - 5)
                    height = random.randint(lower_bound_height, int(base_height + 5))
                    weight = random.randint(lower_bound_weight, int(base_weight + 5))
                    npc = RPG_character_utils.NPCPet(NPC_type, pet_count, species, height, weight, direction, position)
                    pet_count += 1
                else: #NPC_type == "wildlife"
                    species = random.choice(WILDLIFE_SPECIES)
                    base_height = WILDLIFE_ATTRIBUTES[species]["height"]
                    base_weight = WILDLIFE_ATTRIBUTES[species]["weight"]
                    lower_bound_height = max(0, base_height - 10)
                    lower_bound_weight = max(0, base_weight - 10)
                    height = random.randint(lower_bound_height, int(base_height + 10))
                    weight = random.randint(lower_bound_weight, int(base_weight + 10))
                    npc = RPG_character_utils.NPCWildlife(NPC_type, wildlife_count, species, height, weight, direction, position)
                    wildlife_count += 1
                   
                # Store the NPC instance id in the map matrix
                map_matrix[row][col] = (elevation, npc.name, None, None)  # Other attributes to be filled later
                # Add the NPC and its location to the dictionary
                self.npcs[npc] = {
                    "id": npc.name,
                    "direction": direction,
                    "row": row,
                    "col": col
                }

            # Update the zone map with the populated map matrix
            self.zone_maps[direction]["map"] = map_matrix

    def is_empty_space(self, footprint, row, col, map_matrix, index):
        footprint = int(footprint)
        # Define the rows and columns of the map
        rows = len(map_matrix)
        cols = len(map_matrix[0])

        # Check if the current cell and the surrounding cells (based on the footprint) are all empty
        return all(
            map_matrix[r][c][index] is None
            for r in range(row, min(row + footprint, rows))
            for c in range(col, min(col + footprint, cols))
        )

    def place_object(self, row, col, map_object, map_matrix):
        # Determine the footprint of the object to know how many cells it occupies
        footprint = int(map_object.footprint)

        # Iterate through the cells within the footprint and place the object
        for r in range(row, min(row + footprint, len(map_matrix))):
            for c in range(col, min(col + footprint, len(map_matrix[0]))):
                elevation, npc, _, _ = map_matrix[r][c]  # Extract existing values
                map_matrix[r][c] = (elevation, npc, map_object.obj_type, None)  # Update with the object

        # You can also update the object's position attribute if needed
        map_object.position = (row, col)

    def generate_objects(self):
        # Iterate through each direction and populate the map with objects
        for direction, zone_map in self.zone_maps.items():
            map_matrix = zone_map["map"]
            indoor = zone_map["indoor"]
            width = zone_map["width"]
            length = zone_map["length"]

            # Retrieve the terrain objects for the current zone
            density = zone_map["density"]
            num_objects_A = int(0.1 * 0.1 * density * zone_map["width"] * zone_map["length"])
            if indoor:
                outdoor_terrain_type, _ = self.selected_terrain_type
                indoor_terrain_type = zone_map["terrain"]
                terrain_objects = TERRAIN_OBJECTS[outdoor_terrain_type][indoor_terrain_type]
                # Define the number of objects based on density
                num_objects_A = int(0.1 * 0.3 * density * zone_map["width"] * zone_map["length"])
                num_objects_B = int(0.3 * 0.3 * density * zone_map["width"] * zone_map["length"])
                num_objects_C = int(0.6 * 0.3 * density * zone_map["width"] * zone_map["length"])
            else:
                outdoor_terrain_type, _ = self.selected_terrain_type
                terrain_objects = TERRAIN_OBJECTS[outdoor_terrain_type]["outdoor"]
                # Define the number of objects based on density
                num_objects_A = int(0.1 * 0.05 * density * zone_map["width"] * zone_map["length"])
                num_objects_B = int(0.3 * 0.05 * density * zone_map["width"] * zone_map["length"])
                num_objects_C = int(0.6 * 0.05 * density * zone_map["width"] * zone_map["length"])
            print(f"the number of objects are: {num_objects_A}, {num_objects_B}, and {num_objects_C}")
            max_attempts = 1000
            # Iterate through object sizes
            for size, num_objects in zip(["big", "medium", "small"], [num_objects_A, num_objects_B, num_objects_C]):
                for _ in range(num_objects):
                    # Keep trying until a valid position is found
                    valid_position_found = False
                    attempts = 0  # Keep track of the number of attempts to avoid an infinite loop
                    while not valid_position_found and attempts < max_attempts :  # max_attempts can be a predefined constant
                        # Choose a random object from the specified size
                        obj_type = random.choice(terrain_objects[size])
                        try:
                            footprint = OBJECTS_FOOTPRINTS[size][obj_type]
                        except KeyError:
                            print(f"KeyError for size: {size}, obj_type: {obj_type}")
                            continue

                        # Check if the footprint is less than the length and width
                        if int(footprint) < length and int(footprint) < width:
                            row = random.randint(0, length - int(footprint))
                            col = random.randint(0, width - int(footprint))
                            # Check if the selected position is valid using is_empty_space
                            if self.is_empty_space(footprint, row, col, map_matrix, 2):
                                valid_position_found = True
                        attempts += 1

                    if valid_position_found:
                        # Continue with the rest of the code to place the object
                        position = (row, col)
                        name = obj_type
                        map_object = MapObject(size, obj_type, footprint, name, direction, position)
                        self.place_object(row, col, map_object, map_matrix)

                        # Add the object to the self.objects attribute
                        self.objects[map_object] = {
                            "type": obj_type,
                            "size": size,
                            "footprint": footprint,
                            "direction": direction,
                            "row": row,
                            "col": col
                        }

            # Update the zone map with the populated map matrix
            self.zone_maps[direction]["map"] = map_matrix
    
    def generate_resources(self):
        # Determine the terrain type
        terrain_type, _ = self.selected_terrain_type

        # Select the types of resources based on terrain
        terrain_resources = TERRAIN_RESOURCES[terrain_type]
        inorganic_resources = terrain_resources['inorganic_matter']
        organic_resources = terrain_resources['organic_matter']

        # Iterate over the zone_maps and generate resources for each one
        for direction, zone_map in self.zone_maps.items():
            # Retrieve the amount of inorganic and organic matter
            inorganic_amount = zone_map['resources']['inorganic_matter']
            organic_amount = zone_map['resources']['organic_matter']
            indoor = zone_map["indoor"] 

            # Calculate weights for inorganic resources based on rarity
            inorganic_weights = [RARITY_WEIGHTS[RESOURCE_ATTRIBUTES[res]['rarity']] for res in inorganic_resources]
            selected_inorganic_resources = random.choices(inorganic_resources, weights=inorganic_weights, k=inorganic_amount)
            number_of_inorganic_resources=len(selected_inorganic_resources)

            # Calculate weights for organic resources based on rarity
            organic_weights = [RARITY_WEIGHTS[RESOURCE_ATTRIBUTES[res]['rarity']] for res in organic_resources]
            selected_organic_resources = random.choices(organic_resources, weights=organic_weights, k=organic_amount)
            number_of_organic_resources=len(selected_organic_resources)
            number_or_different_resources = number_of_inorganic_resources + number_of_organic_resources
            print(f"there is {number_or_different_resources} types of resources")
            # Create Resource objects and place them on the map
            self.resources[direction] = {'inorganic_matter': [], 'organic_matter': []}
            for res_type, selected_resources in [('inorganic_matter', selected_inorganic_resources), ('organic_matter', selected_organic_resources)]:
                for res_name in selected_resources:
                    # Retrieve attributes from RESOURCE_ATTRIBUTES
                    attributes = RESOURCE_ATTRIBUTES[res_name]
                    rarity = attributes['rarity']
                    regeneration_rate = attributes.get('regeneration_rate', None) # Will be None for inorganic
                    value = attributes['value']
                    max_amount = attributes['max_amount'] # New attribute for maximum amount

                    # Determine the amount based on rarity
                    total_resource_amount = random.randint(1,(zone_map['resources'][res_type]))
                    amount = self.determine_amount(rarity,total_resource_amount, indoor)

                    # Ensure amount does not exceed max_amount
                    amount = min(amount, max_amount)

                    # Determine a random position on the map
                    row, col = self.determine_position(zone_map)
                    max_attempts = 100  # You can set a value based on your requirements
                    attempts = 0
                    while row is None and col is None and attempts < max_attempts:
                        row, col = self.determine_position(zone_map)
                        attempts += 1
                        
                    if row is None and col is None:
                        print(f"Failed to find a valid position for {res_name} in {direction}. Skipping.")
                        continue
                    position = (row, col)
                    if res_type == 'inorganic_matter':
                        resource = InorganicResource(res_type, res_name, amount, direction, position)
                    else: # 'organic_matter'
                        resource = OrganicResource(res_type, res_name, amount, direction, position, regeneration_rate)

                    elevation, npc, obj_type, _ = zone_map['map'][row][col] 
                    # Add the resource to the map matrix
                    zone_map['map'][row][col] = (elevation, npc, obj_type, res_name)  # Update with the object
                    # Add the resource object to the resources dictionary
                    self.resources[direction][res_type].append(resource)

        # The resources have been generated for all directions and center

    def determine_amount(self, rarity, total_resource_amount, indoor):
        # Define a logic to determine the amount based on rarity
        weight = RARITY_WEIGHTS[rarity]
        amount = total_resource_amount * weight
        # Reduce the amount by a factor of 5 if it's an indoor zone
        if indoor:
            amount /= 5
        return amount
    
    def determine_position(self, zone_map):
        rows = len(zone_map['map'])
        cols = len(zone_map['map'][0])
        
        max_attempts = 1000 # You can adjust this value
        attempts = 0

        while attempts < max_attempts:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)

            # Check if the selected position is empty using the is_empty_space method
            if self.is_empty_space(1, row, col, zone_map['map'],3):
               return row, col

            attempts += 1

        print(f"Warning: Could not find a valid position for the resource after {max_attempts} attempts.")
        return None, None
    
    def remove_resource(self, direction, res_type, resource):
        # Check if the direction and resource type exist
        if direction in self.resources and res_type in self.resources[direction]:
            try:
                # Remove the resource object from the list
                self.resources[direction][res_type].remove(resource)
                # Update the zone_map
                row, col = resource.position
                elevation, npc_id, object_type, _ = self.zone_maps[direction]["map"][row][col]
                self.zone_maps[direction]["map"][row][col] = (elevation, npc_id, object_type, None)
            except ValueError:
                print(f"Resource not found in {direction} for type {res_type}.")

    # Other methods for interaction, linking fields, saving/loading, etc.