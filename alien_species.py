class AlienSpecies:
    """
    Represents an individual alien species in the classification system.
    """
    def __init__(self, id, name, features):
        self.id = id
        self.name = name
        self.features = features
        self.classified_universe = None

    def __str__(self):
        universe_status = self.classified_universe if self.classified_universe else "Unclassified"
        return (
            f"--- Alien Species: {self.name} (ID: {self.id}) ---\n"
            f"  Features: {', '.join(self.features)}\n"
            f"  Classification: {universe_status}\n"
        )
