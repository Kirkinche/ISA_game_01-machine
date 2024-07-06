# tests/test_character.py

import unittest
from src.character import create_character

class TestCharacter(unittest.TestCase):
    def test_create_character(self):
        character = create_character("Hero")
        self.assertEqual(character.name, "Hero")
        self.assertEqual(character.strength, 10)
        self.assertEqual(character.agility, 10)
        self.assertEqual(character.intelligence, 10)

if __name__ == "__main__":
    unittest.main()
