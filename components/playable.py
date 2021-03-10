import tcod as libtcod
from components.weapon import Weapon
from game_message import Message
from color import *
from random import randint
class Playable:
    def __init__(self, hp, ac,xp):
        self.max_hp = hp
        self.hp = hp
        self.armor_class = ac
        self.xp = xp      
        
    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({"dead": self.owner, "xp":self.xp})

        return results

    def heal(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []

        if self.owner.equipment.main_hand != None:
            m_weapon:Weapon=self.owner.equipment.main_hand.weapon
            atk_bonus = self.get_atk_bonus(m_weapon)
            roll = randint(1,20)
            results.append({"message":
                            Message("{} attack roll {}+{} vs {} AC of {}.".format(
                                self.owner.name,atk_bonus,roll,
                                target.playable.armor_class,target.name))})
            if atk_bonus + roll >= target.playable.armor_class:
                damage = 0
                for i in range(0, m_weapon.dmg_quantity):
                    d_roll = randint(1,m_weapon.weapon_dmg)
                    modifier = self.get_modifier_bonus(m_weapon)
                    damage += d_roll + modifier
                if damage > 0:
                    results.append({
                    "message":Message("{} attacks {} for {} hit points.".format(
                        self.owner.name.capitalize(), target.name, damage),WHITE)})
                    results.extend(target.playable.take_damage(damage))
                else:
                    results.append({"message":
                    Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})
            else:
                results.append({"message":
                Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})

        if self.owner.equipment.off_hand != None:
            o_weapon:Weapon=self.owner.equipment.off_hand.weapon
            atk_bonus = self.get_atk_bonus(o_weapon)
            roll = randint(1,20)
            results.append({"message":
                            Message("{} attack roll {}+{} vs {} AC of {}.".format(
                                self.owner.name,atk_bonus,roll,
                                target.playable.armor_class,target.name))})
            if atk_bonus + roll >= target.playable.armor_class:
                damage = 0
                for i in range(0, m_weapon.dmg_quantity):
                    d_roll = randint(1,m_weapon.weapon_dmg)
                    '''
                    TODO DULA WILDING  3 types ;/
                    '''
                    #modifier = sefl.get_modifier_bonus(m_weapon)
                    modifier = 0
                    damage += d_roll + modifier
                if damage > 0:
                    results.append({
                    "message":Message("{} attacks {} for {} hit points.".format(
                        self.owner.name.capitalize(), target.name, damage),WHITE)})
                    results.extend(target.Playable.take_damage(damage))
                else:
                    results.append({"message":
                    Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})
            else:
                results.append({"message":
                Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})
        
        if self.owner.equipment.main_hand == None and self.owner.equipment.off_hand == None:
            atk_bonus = self.owner.ability.modifaier_strenght
            roll = randint(1,20)
            results.append({"message":
                            Message("{} attack roll {}+{} vs {} AC of {}.".format(
                                self.owner.name,atk_bonus,roll,
                                target.playable.armor_class,target.name))})
            if atk_bonus + roll >= target.playable.armor_class:
                '''
                Instead of using a weapon to make a melee weapon attack, you can use an unarmed strike:
                a punch, kick, head--butt, or similar forceful blow (none of which count as weapons). 
                On a hit, an unarmed strike deals bludgeoning damage equal to 1 + your Strength modifier.
                You are proficient with your unarmed strikes.
                '''  
                damage = 1 + self.owner.ability.modifaier_strenght
                if damage > 0 :
                    results.append({
                    "message":Message("{} attacks {} for {} hit points.".format(
                        self.owner.name.capitalize(), target.name, damage),WHITE)})
                    results.extend(target.playable.take_damage(damage))
                else:
                    results.append({"message":
                    Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})
            else:
                results.append({"message":
                Message("{} attacks {} but does no damage.".format(self.owner.name.capitalize(), target.name),WHITE)})

        return results

    def get_atk_bonus(self,weapon:Weapon):        
        modifier_bonus = self.get_modifier_bonus(weapon)
        '''
        proficiency bonus
        Only addet when u can wield this type of weapon
        '''
        proficiency_bonus = 0
        if self.owner.preficiencies.is_proficient_weapon(weapon):
            proficiency_bonus = self.owner.level.proficiency_bonus
        return modifier_bonus + proficiency_bonus

    def get_modifier_bonus(self,weapon:Weapon):
        '''
            Weapons with finesse can use dexterity modifaier as bonus to hit roll
            That why we take higher modifaier ...
            No on chose lower modifaier XD
        '''
        if weapon.finesse:
           return max(self.owner.ability.modifaier_strenght, self.owner.ability.modifaier_dexterity)
        else:
           return self.owner.ability.modifaier_strenght
            