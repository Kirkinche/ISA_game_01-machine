# src/quest.py

class Quest:
    def __init__(self, title, description, completed=False):
        self.title = title
        self.description = description
        self.completed = completed

    def complete_quest(self):
        self.completed = True
        print(f"Quest '{self.title}' completed!")
