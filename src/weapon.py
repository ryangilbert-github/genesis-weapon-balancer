import random

class Weapon:
    """
    Represents a candidate solution in the genetic algorithm.
    Contains the 'Genes' (Damage, Fire Rate, Mag Size).
    """
    def __init__(self, name="Prototype", damage=None, fire_rate=None, mag=None):
        self.name = name
        # Factory Pattern: If no stats provided, generate random 'Garbage' stats
        self.damage = damage if damage else random.randint(1, 100)
        self.fire_rate = fire_rate if fire_rate else random.uniform(0.1, 5.0)
        self.mag = mag if mag else random.randint(1, 50)

    def get_dps(self):
        """Calculate raw Damage Per Second (ignoring reload penalty)"""
        return self.damage * self.fire_rate

    def __repr__(self):
        return f"Weapon(Dmg={self.damage}, Rate={self.fire_rate:.2f}, Mag={self.mag})"