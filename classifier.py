from alien_species import AlienSpecies

class Classifier:
    """
    Applies classification rules to assign an AlienSpecies to a universe.
    """
    CLASSIFICATION_RULES = {
        "solar power": "Kryptonian Universe",
        "icy breath": "Arcturian Universe",
        "three legs": "Zorpian Universe",
        # You can add more rules here based on your data!
    }

    def classify_species(self, alien: AlienSpecies):
        """
        Iterates through the alien's features and applies the classification rules.
        """
        for feature in alien.features:
            if feature in self.CLASSIFICATION_RULES:
                alien.classified_universe = self.CLASSIFICATION_RULES[feature]
                return f"Classified {alien.name} as {alien.classified_universe}"
        
        # Default classification
        alien.classified_universe = "Unknown Universe"
        return f"Could not classify {alien.name}, assigned to {alien.classified_universe}"
