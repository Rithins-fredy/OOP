# system_manager.py
from typing import Dict, Optional, Any 
from faculty import Faculty
from study_field import StudyField


class StudentManagementSystem:
    """
    The central hub for the University, managing all Faculty objects.
    """

    def __init__(self):
        """Stores all faculties: {abbreviation: Faculty object}"""
        self._faculties: Dict[str, Faculty] = {}

    # --- General Operations ---

    def create_faculty(self, name: str, abbreviation: str, study_field_str: str) -> bool:
        abbreviation = abbreviation.upper() 
        
        if abbreviation in self._faculties:
            print(f"Error: Faculty with abbreviation '{abbreviation}' already exists.")
            return False

        try:
            # Convert the string input (e.g., 'SOFTWARE_ENGINEERING') to the Enum member
            study_field = StudyField[study_field_str.upper()]
        except KeyError:
            # This is robust input validation for the study field
            print(f"Error: Invalid study field '{study_field_str}'. Available: {', '.join([f.name for f in StudyField])}")
            return False

        new_faculty = Faculty(name, abbreviation, study_field)
        self._faculties[abbreviation] = new_faculty
        print(f"Success: Faculty '{name}' ({abbreviation}) created under field '{study_field.value}'.")
        return True

    def find_faculty_by_student_email(self, email: str) -> Optional[Faculty]:
        """Searches all faculties for a student by email."""
        for faculty in self._faculties.values():
            if faculty.find_student_by_email(email):
                return faculty
        return None

    def display_university_faculties(self):
        """Displays the name, abbreviation, and field of all faculties."""
        if not self._faculties:
            print("No faculties have been created yet.")
            return

        print("\n--- University Faculties ---")
        # THIS LOOP IS THE KEY AREA. If it crashes, the print is interrupted.
        for faculty in self._faculties.values():
            print(f" * {faculty}")
        print("----------------------------")

    def display_faculties_by_field(self, study_field_str: str):
        try:
            target_field = StudyField[study_field_str.upper()]
        except KeyError:
            print(f"Error: Invalid study field '{study_field_str}'.")
            return

        matching_faculties = [f for f in self._faculties.values() if f.study_field == target_field]

        if not matching_faculties:
            print(f"No faculties found under the field: {target_field.value}.")
            return

        print(f"\n--- Faculties under {target_field.value} ---")
        for faculty in matching_faculties:
            print(f" * {faculty.name} ({faculty.abbreviation})")
        print("----------------------------------")
        
    def get_faculty(self, abbreviation: str) -> Optional[Faculty]:
        return self._faculties.get(abbreviation.upper())
