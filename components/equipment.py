from game.equipment_slots import EQUIPMENT_SLOTS
from game.game_message import Message
class Equipment:
    def __init__(self,main_hand=None, off_hand=None):
        self.main_hand = main_hand
        self.off_hand = off_hand

    @property
    def max_hp_bonus(self):
        bonus =0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus
        
        return bonus

    @property
    def power_bonus(self):
        bonus =0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus =0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        return bonus

    def toggle_equip(self, equipment_entity):
        results = []

        slot = equipment_entity.equippable.slot
       
        if slot == EQUIPMENT_SLOTS.MAIN_HAND:
            if self.main_hand == equipment_entity:
                self.main_hand = None
                results.append({"dequipped":equipment_entity})
            else:
                if self.main_hand:
                    results.append({"dequipped":self.main_hand})
                self.main_hand = equipment_entity
                results.append({"equipped":equipment_entity})
        elif slot == EQUIPMENT_SLOTS.OFF_HAND:
            if self.off_hand == equipment_entity:
                self.off_hand = None
                results.append({"dequipped":equipment_entity})
            else:
                if self.off_hand:
                    results.append({"dequipped":self.off_hand})
                self.off_hand = equipment_entity
                results.append({"equipped":equipment_entity})
        
        return results

    def toggle_equip_main_hand(self,equipment_entity):
        results = []
            
        if self.main_hand == equipment_entity:
            self.main_hand = None
            equipment_entity.equippable.equipped = False
            results.append({"dequipped":equipment_entity})
        else:
            if self.main_hand:
                self.main_hand.equippable.equipped = False
                results.append({"dequipped":self.main_hand})
               
            self.main_hand = equipment_entity
            self.main_hand.equippable.equipped = True
            results.append({"equipped":equipment_entity})
            
        return results
        
    def toggle_equip_off_hand(self, equipment_entity):
        results = []

        if self.off_hand == equipment_entity:
            self.off_hand = None
            equipment_entity.equippable.equipped = False
            equipment_entity.weapon.main = True
            results.append({"dequipped":equipment_entity})
        elif self.main_hand and self.main_hand.weapon.two_hand:
            self.toggle_equip_main_hand(self.main_hand)
        else:
            if self.off_hand:
                self.off_hand.equippable.equipped = False
                self.off_hand.weapon.main = True
                results.append({"dequipped":self.off_hand})
            self.off_hand = equipment_entity
            self.off_hand.equippable.equipped = True
            self.off_hand.weapon.main = False
            results.append({"equipped":equipment_entity})
    
        return results