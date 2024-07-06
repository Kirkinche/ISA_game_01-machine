
import random
import copy
# procedural_map.py

class Map:
    def __init__(self, size):
        self.size = size
        self.map = self.generate_map()

    def generate_map(self):
        return [[(random.choice(['plain', 'forest', 'mountain']), random.randint(1, 100), random.choice([True, False]), random.randint(0, 10), random.uniform(0, 0.5), random.choice(['none', 'river', 'lake', 'pond']), random.randint(0, 5), {'inorganic_matter': random.randint(0, 30),'organic_matter': random.randint(0, 20)}) for _ in range(self.size)] for _ in range(self.size)]

    def place_points_of_interest(self):
        points_of_interest = ['town', 'dungeon', 'treasure']
        for poi in points_of_interest:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            self.map[x][y] = (poi, *self.map[x][y][1:])
    
    def display_map(self):
        for row in self.map:
            print(" ".join([cell[0] for cell in row]))
    
    def to_dict(self):
        # Convert tuples to lists
        serialized_map = [[list(item) for item in row] for row in self.map]
        return {
            'class_name': 'Map',
            'map': serialized_map,
            'size': self.size
        }

    @classmethod
    def from_dict(cls, dict_obj):
        # Convert lists back to tuples
        deserialized_map = [[[tuple(item) for item in row] for row in layer] for layer in dict_obj.get('map', [])]
        size = dict_obj.get('size')
        return cls(deserialized_map, size)
    
    def __str__(self):
        return '\n'.join([' '.join([f"({cell[0]}, {cell[1]}, {cell[2]}, {cell[3]}, {cell[4]:.2f}, {cell[5]}, {cell[6]}, {cell[7]})" for cell in row]) for row in self.map])

    def move_north(self):
        self.map.pop(0)
        self.map.append([(random.choice('abcde'), random.randint(1, 100), random.choice([True, False]), random.randint(0, 10), random.uniform(0, 1), random.choice(['none', 'river', 'lake', 'pond']), random.randint(0, 5), {'inorganic_matter': random.randint(0, 50),'organic_matter': random.randint(0, 30)}) for _ in range(self.size)])

    def move_south(self):
        self.map.insert(0, [(random.choice('abcde'), random.randint(1, 100), random.choice([True, False]), random.randint(0, 10), random.uniform(0, 1), random.choice(['none', 'river', 'lake', 'pond']), random.randint(0, 5), {'inorganic_matter': random.randint(0, 50),'organic_matter': random.randint(0, 30)}) for _ in range(self.size)])
        self.map.pop()

    def move_east(self):
        for row in self.map:
            row.pop(0)
            row.append((random.choice('abcde'), random.randint(1, 100),random.choice([True, False]), random.randint(0, 10), random.uniform(0, 1), random.choice(['none', 'river', 'lake', 'pond']), random.randint(0, 5), {'inorganic_matter': random.randint(0, 50),'organic_matter': random.randint(0, 30)}))

    def move_west(self):
        for row in self.map:
            row.insert(0, (random.choice('abcde'), random.randint(1, 100), random.choice([True, False]), random.randint(0, 10), random.uniform(0, 1), random.choice(['none', 'river', 'lake', 'pond']), random.randint(0, 5), {'inorganic_matter': random.randint(0, 50),'organic_matter': random.randint(0, 30)}))
            row.pop()

    def get_point(self, row, col):
        return self.map[row][col]

    def set_point(self, row, col, value):
        # Ensure that the value is a tuple with 8 elements
        if len(value) != 8:
            raise ValueError("Value must be a tuple with 8 elements.")
        self.map[row][col] = value
    
    def update_indoor_grid(self, new_indoor_grid):
        for row in range(self.size):
            for col in range(self.size):
                event, probability, _, weather, density, water, npc, resources= self.map[row][col]
                indoor = new_indoor_grid[row][col]
                self.map[row][col] = (event, probability, indoor, weather, density, water, npc, resources)

    def make_weather_map(self):
        # Copy the existing weather map
        new_weather_map = copy.deepcopy(self.map)
        # Iterate through the rows and columns
        for n in range(self.size):
            for m in range(self.size):
                # Get the north and west weather values
                north_weather = self.map[n - 1][m][3] if n > 0 else 0
                west_weather = self.map[n][m - 1][3] if m > 0 else 0
                # Calculate the new weather value
                new_weather_value = int((random.randint(200, 1800) * (north_weather + west_weather)) / 2000)
                # Clamp the value to the range 0-10
                new_weather_value = min(max(new_weather_value, 0), 10)
                # Update the weather value in the copied map, keeping the other elements
                new_weather_map[n][m] = (self.map[n][m][0], self.map[n][m][1], self.map[n][m][2], new_weather_value, self.map[n][m][4], self.map[n][m][5], self.map[n][m][6], self.map[n][m][7])
        # Assign the new weather map to the original map
        self.map = new_weather_map

        
    def describe_point(self, row, col):
        point = self.map[row][col]
        weather_values = ["clear", "partly cloudy", "cloudy", "mist", "wind", "light rain", "heavy rain", "thunderstorm", "light snow", "heavy snow", "hurricane"]
        event_type, event_prob, indoor, weather, density, water_source, presence, resources = point
        description = f"Event Type: {event_type}\n"
        description += f"Probability of Event: {event_prob}%\n"
        description += "Location: Indoor\n" if indoor else "Location: Outdoor\n"
        description += f"Weather: {weather_values[weather]}\n"
        description += f"Density: {density * 100:.2f}% {'vegetation' if not indoor else 'objects'}\n"
        description += f"Water Source: {water_source}\n"
        description += f"Presence of NPC: {presence}\n"
        description += "Resources:\n"
        for resource, amount in resources.items():
            description += f"  {resource}: {amount}\n"

        print(f"The procedural map node {row}, {col} correspond to:\n {description}")
        return description
