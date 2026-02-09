import numpy as np
import random
from .weapon import Weapon


# ==========================================
# 1. THE PHYSICS (The Discriminator)
# ==========================================
def calculate_ttk(weapon, monster):
    """
    Runs a discrete-event simulation: Weapon vs Monster.
    Returns: Time To Kill (seconds).
    """
    shots_to_kill = np.ceil(monster.health / weapon.damage)

    # Reload Logic: If mag size is too small, add penalty time
    reloads = 0
    if shots_to_kill > weapon.mag:
        reloads = np.floor((shots_to_kill - 1) / weapon.mag)

    # Physics Formula:
    # (Shots - 1) because the first bullet is fired at t=0
    shooting_time = (shots_to_kill - 1) / weapon.fire_rate
    total_time = shooting_time + (reloads * 2.0)  # Assume 2.0s reload animation

    return total_time


def fitness_score(weapon, monster):
    """
    Calculates the 'Error Score'.
    0.0 = Perfect Solution.
    """
    actual_ttk = calculate_ttk(weapon, monster)
    error = abs(monster.ideal_ttk - actual_ttk)
    return error


# ==========================================
# 2. THE EVOLUTION (The Generator)
# ==========================================
def mutate(weapon, mutation_rate=0.1):
    """
    Randomly modifies genes based on mutation_rate.
    Returns a NEW Weapon instance (Immutability).
    """
    new_dmg = weapon.damage
    new_rate = weapon.fire_rate
    new_mag = weapon.mag

    # Mutation: Damage +/- 10
    if random.random() < mutation_rate:
        new_dmg = max(1, weapon.damage + random.randint(-10, 10))

    # Mutation: Fire Rate +/- 0.5
    if random.random() < mutation_rate:
        new_rate = max(0.1, weapon.fire_rate + random.uniform(-0.5, 0.5))

    # Mutation: Mag Size +/- 5
    if random.random() < mutation_rate:
        new_mag = max(1, weapon.mag + random.randint(-5, 5))

    return Weapon(weapon.name, new_dmg, new_rate, new_mag)


def crossover(parent1, parent2):
    """
    Mixes genes from two parents to create a child.
    """
    # 50/50 chance for each gene
    child_dmg = parent1.damage if random.random() > 0.5 else parent2.damage
    child_rate = parent1.fire_rate if random.random() > 0.5 else parent2.fire_rate

    # Average the mag size for stability
    child_mag = int((parent1.mag + parent2.mag) / 2)

    return Weapon(parent1.name, child_dmg, child_rate, child_mag)