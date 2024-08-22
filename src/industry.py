#this module create the industry object  with its attributes and methods, for industrial simulations.

from machine import Machine

class Industry:
    def __init__(self, name):
        self.name = name
        self.machines = [Machine(name)]

    def add_machine(self, machine):
        self.machines.append(machine)

    def remove_machine(self, machine):
        self.machines.remove(machine)
    
    def simulate(self, time_units):
        for machine in self.machines:
            machine.simulate(time_units)

    def estimate_environmental_impact(self):
        impact = 0
        for machine in self.machines:
            impact += machine.estimate_environmental_impact()
        return impact
    
    def estimate_maintenance_cost(self, time_units):
        cost = 0
        for machine in self.machines:
            cost += machine.calculate_operating_cost(time_units)
        return cost
    
    def estimate_production_output(self, time_units):
        output = 0
        for machine in self.machines:
            output += machine.calculate_power_consumption(time_units)
        return output

    def optimize_production(self, time_units, target_output):
        # This is a placeholder for a more complex optimization algorithm
        # In a real-world scenario, this could involve adjusting machine speeds, scheduling, etc.
        for machine in self.machines:
            machine.speed = target_output / machine.calculate_power_consumption(time_units)
