from math import sqrt
import random

class RPGCharacter:
    def __init__(self, race, name, gender, job):
        self.race = race
        self.name = name
        self.gender = gender
        self.job = job
        self.height = random.randint(150, 200)       
        weight_height_factor = random.randint(350, 620) / 1000
        self.weight = int(weight_height_factor * self.height)
        self.intelligence = self.roll_dice()
        self.dexterity = self.roll_dice()
        self.wisdom = self.roll_dice()
        self.luck = self.roll_dice()
        self.charm = self.roll_dice()
        self.strength = self.roll_dice()
        self.constitution = self.roll_dice()
        self.current_health = self.roll_dice() * 10  # Example health calculation
        self.max_health = self.current_health
        self.direction = None # the location of the map in the zone, e.g., north, south, east, west, northeast, etc.
        self.position = None # A tuple representing the (row, col) position within a zone map
        self.orientation = "north" # A string indicating the orientation of the character,  north, south, east, west, northeast, etc.; or change to an angle rotation?
        self.inventory = []
        self.level = 1
        self.affection = [] # Condition, deseases, blessing, magical effects affecting the character
        self.life = 100
        self.points = 0
        self.money = 5
        self.status = [] # Action or action state of the character, such as "attacking", "defending", "travelling", etc.
    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

    def __str__(self):
        return f"Character(name={self.name}, job={self.job}, gender={self.gender}, height={self.height}, weight={self.weight}, intelligence={self.intelligence}, wisdom={self.wisdom}, \n luck={self.luck}, charm={self.charm}, strength={self.strength}, constitution={self.constitution}),\n direction={self.direction}, position={self.position}, life={self.life}, level={self.level}, \n inventory={self.inventory} "
    
    def to_dict(self):
        return {
            'class_name': 'RPGCharacter',
            'race': self.race,
            'name': self.name,
            'gender': self.gender,
            'job': self.job,
            'height': self.height,
            'weight': self.weight,
            'intelligence': self.intelligence,
            'dexterity': self.dexterity,
            'wisdom': self.wisdom,
            'luck': self.luck,
            'charm': self.charm,
            'strength': self.strength,
            'constitution': self.constitution,
            'direction': self.direction,
            'position': self.position,
            'orientation': self.orientation,
            'inventory': self.inventory,
            'level': self.level,
            'affection': self.affection,
            'life': self.life,
            'points': self.points,
            'money': self.money,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, dict_obj):
        # Create an instance of RPGCharacter
        instance = cls(
            dict_obj.get('race'),
            dict_obj.get('name'),
            dict_obj.get('gender'),
            dict_obj.get('job')
        )
        # Populate the other attributes
        instance.height = dict_obj.get('height')
        instance.weight = dict_obj.get('weight')
        instance.intelligence = dict_obj.get('intelligence')
        instance.dexterity = dict_obj.get('dexterity')
        instance.wisdom = dict_obj.get('wisdom')
        instance.luck = dict_obj.get('luck')
        instance.charm = dict_obj.get('charm')
        instance.strength = dict_obj.get('strength')
        instance.constitution = dict_obj.get('constitution')
        instance.direction = dict_obj.get('direction')
        instance.position = dict_obj.get('position')
        instance.orientation = dict_obj.get('orientation')
        instance.inventory = dict_obj.get('inventory')
        instance.level = dict_obj.get('level')
        instance.affection = dict_obj.get('affection')
        instance.life = dict_obj.get('life')
        instance.points = dict_obj.get('points')
        instance.money = dict_obj.get('money')
        instance.status = dict_obj.get('status')
        return instance

class NPCCharacter(RPGCharacter):
    def __init__(self, race, name, gender, job):
        super().__init__(race, name, gender, job)    
        self.memory = {'place_to_go':(0,0)}

    def to_dict(self):
        parent_dict = super().to_dict()  # Get the parent class's dictionary
        parent_dict['class_name'] = 'NPCCharacter'  # Update the class_name
        return parent_dict

    @classmethod
    def from_dict(cls, dict_obj):
        parent_obj = super().from_dict(dict_obj)  # Initialize parent object attributes
        parent_obj.__class__ = cls  # Change the class to NPCCharacter
        return parent_obj
    
    def npc_description(self):
        print(self)

    def move(self, direction, zone_map):
        width_map = zone_map.zone_maps[self.direction]["width"]
        length_map = zone_map.zone_maps[self.direction]["length"]
        row, col = self.position
        if direction == "North":
            self.position= (row - 1, col)
        elif direction == "South":
            self.position= (row + 1, col)
        elif direction == "East":
            self.position= (row, col -1)
        elif direction == "West":
            self.position= (row, col + 1)
        if row < 0 or row > (length_map-1) or col < 0 or col > (width_map-1): 
            self.life = 0
            print("Fall of the map")
            print(f"{self.name} has {self.life} life and is now dead")
    
    def look_for_resources(self, zone_map):
        #TODO #search for a resource in the map
        self.resource_positions = []
        for res_typ in zone_map.resources[self.direction]:
            for resource in zone_map.resources[self.direction][res_typ]:
                self.resource_positions.append(resource.position)
        if len(self.resource_positions) > 0:
            print(self.resource_positions)     
            closest_position = None 
            closest_distance = float('inf')
            
            for point in self.resource_positions:
                distance = sqrt((self.position[0] - point[0])**2 + (self.position[1] - point[1])**2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_position = point
            print(f"the closest resource is at: {closest_position}")
            return closest_position
        

    def make_path_to(self, target_position):
        #TODO #make a path of directions for getting to the position in a map
        row_npc, col_npc = self.position
        direction =""
        row, col = target_position
        posible_directions = []
        if row < (row_npc):
            posible_directions.append("North")
        elif row == (row_npc):
            pass
        else:
            posible_directions.append("South")
        if col < (col_npc):
            posible_directions.append("West")
        elif col == (col_npc):
            pass
        else:
            posible_directions.append("East")
        if len(posible_directions)>0:
            direction=random.choice(posible_directions)
        return direction
    
    def go_to(self, path_in_map):
        #TODO #successively reach to a position
        pass

    def look_on_map_in_situ(self, zone_map):
        x_npc, y_npc = self.position
        direction = self.direction
        print(f"Direction: {direction}, x_npc: {x_npc}, y_npc: {y_npc}")
        print(f"Map Dimensions: {len(zone_map.zone_maps[direction]['map'])} x {len(zone_map.zone_maps[direction]['map'][0])}")
        tuple_in_map = zone_map.zone_maps[direction]["map"][x_npc-1][y_npc-1]
        return tuple_in_map

    def gather_resource(self, direction, position, zone_map):
        #TODO #collect resources on a map of zone_map
        x, y = position
        position_matrix = x-1, y-1
        tuple_in_map = zone_map.zone_maps[direction]["map"][x-1][y-1]
        elevation, npc_id, object_type, resource_type = tuple_in_map
        print(tuple_in_map)
        if resource_type is not None:
            for res_typ in zone_map.resources[direction]:
                for resource in zone_map.resources[direction][res_typ]:
                    print(f"{resource.position} compare to {position_matrix}")
                    if resource.position == position_matrix:
                        self.inventory.append(resource)
                        # Remove the resource from the zone_map
                        zone_map.remove_resource(direction, res_typ, resource)
                        print(f"{self.name} added resources to is inventory: {self.inventory}")
                        print("collected all resources in situ")

    def persue_goal(self, zone_map):
        job = self.job
        
        goals = {"Farmer": "look_for_resources", "Merchant": "look_for_npcs", "Guard": "look_for_objects"}
        HUMAN_JOBS:["Farmer", "Merchant", "Guard", "Healer", "Blacksmith", "Carpenter", "Miner", "Hunter", "Mage", "Warrior"]
       
    
    def take_turn(self, zone_map):
        # Implement NPC behavior here
        print(f"{self.name} has {self.life} point of live and will play")
        if self.life > 0:
            print(f"{self.name} starting to play at position {self.position}")
            # For example, choose a random direction to move
            tuple_in_situ=self.look_on_map_in_situ(zone_map) 
            elevation, npc_id, object_type, resource_type =tuple_in_situ
            if resource_type is None:
                closest_position = self.look_for_resources(zone_map)
                if self.memory['place_to_go'] == self.position:
                    self.memory['place_to_go'] = closest_position
                    direction = self.make_path_to(closest_position)
                    self.move(direction, zone_map)
                elif self.memory['place_to_go'] == closest_position:
                    direction = self.make_path_to(closest_position)
                    self.move(direction, zone_map)
                else:
                    closest_position = self.memory['place_to_go']
                    print(closest_position)
                    direction = self.make_path_to(closest_position)
                    self.move(direction, zone_map)
            else:
                print("npc is at a resource position")
                self.gather_resource(self.direction, self.position, zone_map)
        else:
            print(f"{self.name} is dead and cannot act.")
        


class NPCPet:
    def __init__(self, race, name, species, height, weight, direction, position):
        self.race = race
        self.name = f"Pet_name_{name}"
        self.species = species
        self.height = height
        self.weight = weight
        self.level = 1
        self.direction = direction # the location of the map in the zone, e.g., north, south, east, west, northeast, etc.
        self.position = position  # A tuple representing the (row, col) position within a zone map
        self.life = 100
        self.memory = {}

    def to_dict(self):
        return {
            'class_name': 'NPCPet',
            'race': self.race,
            'name': self.name,
            'species': self.species,
            'height': self.height,
            'weight': self.weight,
            'level': self.level,
            'direction': self.direction,
            'position': self.position,
            'life': self.life
        }

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj['race'],
            dict_obj['name'],
            dict_obj['species'],
            dict_obj['height'],
            dict_obj['weight'],
            dict_obj['level'],
            dict_obj['direction'],
            tuple(dict_obj['position']),  # Convert list back to tuple
            dict_obj['life'],
        )

    def __str__(self):
        return f"NPCPet(name={self.name}, species={self.species}, weight={self.weight})"
    
    def move(self, direction):
        row, col = self.position
        if direction == "North":
            self.position= (row - 1, col)
        elif direction == "South":
            self.position= (row + 1, col)
        elif direction == "East":
            self.position= (row, col -1)
        elif direction == "West":
            self.position= (row, col + 1)
        print(f"{self.name} is {self.race} and at {self.position}")
        if row < 0 or col < 0: 
            self.live = 0
            print(self.live)
            print("Fall of the map")

    def take_turn(self, zone_map):
        # Implement NPC behavior here
        if self.life > 0:
            # For example, choose a random direction to move
            direction = random.choice(['North', 'South', 'East', 'West'])
            self.move(direction)
        else:
            print(f"{self.name} is dead and cannot act.")

class NPCWildlife:
    def __init__(self, race, name, species, height, weight, direction, position):
        self.race = race
        self.name = "Anon"
        self.species = species
        self.height = height
        self.weight = weight
        self.level = 1
        self.direction = direction # the location of the map in the zone, e.g., north, south, east, west, northeast, etc.
        self.position = position  # A tuple representing the (row, col) position within a zone map
        self.life = 100
        self.memory = {}

    def to_dict(self):
        return {
            'class_name': 'NPCWildlife',
            'race': self.race,
            'name': self.name,
            'species': self.species,
            'height': self.height,
            'weight': self.weight,
            'level': self.level,
            'direction': self.direction,
            'position': self.position,
            'life': self.life
        }

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj['race'],
            dict_obj['name'],
            dict_obj['species'],
            dict_obj['height'],
            dict_obj['weight'],
            dict_obj['level'],
            dict_obj['direction'],
            tuple(dict_obj['position']),  # Convert list back to tuple
            dict_obj['life'],
        )
    
    def __str__(self):
        return f"NPCWildlife(name={self.name}, species={self.species}, weight={self.weight})"

    def move(self, direction):
        row, col = self.position
        if direction == "North":
            self.position= (row - 1, col)
        elif direction == "South":
            self.position= (row + 1, col)
        elif direction == "East":
            self.position= (row, col -1)
        elif direction == "West":
            self.position= (row, col + 1)
        print(self)
        print(self.position)
        if row < 0 or col < 0: 
            self.live = 0
            print(self.live)
            print("Fall of the map")

    def take_turn(self, zone_map):
        # Implement NPC behavior here
        if self.life > 0:
            # For example, choose a random direction to move
            direction = random.choice(['North', 'South', 'East', 'West'])
            self.move(direction)
        else:
            print(f"{self.name} is dead and cannot act.")