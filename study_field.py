# study_field.py
from enum import Enum

class StudyField(Enum):
    """
    Enumeration representing the official study fields at the Technical University of Moldova (TUM).
    Used to standardize faculty creation.
    """
    MECHANICAL_ENGINEERING = "Mechanical Engineering"
    SOFTWARE_ENGINEERING = "Software Engineering"
    FOOD_TECHNOLOGY = "Food Technology"
    URBANISM_ARCHITECTURE = "Urbanism and Architecture"
    VETERINARY_MEDICINE = "Veterinary Medicine"
