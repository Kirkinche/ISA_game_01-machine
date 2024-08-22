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
