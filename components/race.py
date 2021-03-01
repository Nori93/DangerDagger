import math

class Race:
    def __init__(self):
        self.strenght = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0

    @property
    def sav_th_strenght(self):
        return math.floor(((self.strenght - 10) / 2)) 

    @property
    def sav_th_dexterity(self):
        return math.floor(((self.dexterity - 10) / 2)) 
    
    @property
    def sav_th_constitution(self):
        return math.floor(((self.constitution - 10) / 2)) 
    
    @property
    def sav_th_wisdom(self):
        return math.floor(((self.wisdom - 10) / 2))

    @property
    def sav_th_charisma(self):
        return math.floor(((self.charisma - 10) / 2))
    
