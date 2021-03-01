from random import randint
from enum import Enum
class Dice:
    class TYPE(Enum):
        K_4 = 4
        K_6 = 6
        K_8 = 8
        K_10 = 10
        K_12 = 12
        K_20 = 20

    def __init__(self, type: Dice.TYPE):
        self.type = type

    @property
    def roll(self):
        return randint( 1, self.type.value )