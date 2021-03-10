#Component for magic skllis or weapon skill where 
# Magic skill will be showed as icon on GUI.
# Then for example sword skill is a contener how good player can use that type of weapons.
class Skills:
    def __init__(self):
        self.skills = []
    
    def add_skill(self,skill_name:str,skill):
        self.skills.append(
            {"skill_name":skill_name,
             "skill":skill})    

    def use_skill(self,skill_name:str,target):
        for skill in self.skills:
            if skill['skill_name'] == skill_name:
                skill['skill'](self.owner, target)

    def check_for_skill(self):
        for skill in self.skills:
            if skill['skill_name'] == skill_name:
                return True
        return False