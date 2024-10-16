class Enemy:
    def __init__(self, life, attack_damage):
        self.enemy_life = life
        self.attack_damage = attack_damage

    def take_damage(self, damage):
        self.enemy_life -= damage
        if self.enemy_life <= 0:
            self.enemy_life = 0
            print("Enemy defeated!")
        else:
            print(f"Enemy took {damage} damage, {self.enemy_life} life remaining.")

    def attack(self):
        print(f"Enemy attacks with {self.attack_damage} damage!")
