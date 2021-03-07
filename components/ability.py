import math

class Ability:
    def __init__(
        self,
        strenght:int,
        dexterity:int,
        constitution:int,
        intelligence:int,
        wisdom:int,
        charisma:int
        ):
        self.strenght = strenght
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    @property
    def modifaier_strenght(self):
        return math.floor(((self.strenght - 10) / 2)) 

    @property
    def modifaier_dexterity(self):
        return math.floor(((self.dexterity - 10) / 2)) 
    
    @property
    def modifaier_constitution(self):
        return math.floor(((self.constitution - 10) / 2)) 
    
    @property
    def modifaier_intelligence(self):
        return math.floor(((self.intelligence - 10) / 2)) 
    
    @property
    def modifaier_wisdom(self):
        return math.floor(((self.wisdom - 10) / 2))

    @property
    def modifaier_charisma(self):
        return math.floor(((self.charisma - 10) / 2))
    
