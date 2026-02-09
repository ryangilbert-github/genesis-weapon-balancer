class Monster:
    """
    Represents an enemy entity in the game world.
    Acts as the 'Constraint' for the optimization problem.
    """
    def __init__(self, name, health, ideal_ttk):
        self.name = name
        self.health = health
        self.ideal_ttk = ideal_ttk  # The Game Design Target (e.g., Bosses should take 30s)

    def __repr__(self):
        return f"Monster(Name={self.name}, HP={self.health}, Target_TTK={self.ideal_ttk}s)"