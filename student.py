# student.py
from datetime import date
from typing import Optional, Dict, Any # <-- ADDED typing imports

class Student:
    """
    Represents a student in the TUM system.
    """

    def __init__(self, first_name: str, last_name: str, email: str, 
                 enrollment_date: date, date_of_birth: date):
        """Initializes a new Student object."""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email  
        self.enrollment_date = enrollment_date
        self.date_of_birth = date_of_birth
        self.is_graduated = False 

    def __str__(self):
        """Provides a clean string representation for display."""
        status = "Graduated" if self.is_graduated else "Enrolled"
        return (f"Student: {self.first_name} {self.last_name} | Email: {self.email} | "
                f"DOB: {self.date_of_birth.strftime('%d/%m/%Y')} | Status: {status}")
    
    # ... (other methods are optional for base grade)
    def graduate(self):
        self.is_graduated = True

    def is_enrolled(self) -> bool:
        return not self.is_graduated
    
    # Placeholder methods for Grade 9, included here for completeness but not used in Grade 8
    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("to_dict not implemented for Grade 8")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        raise NotImplementedError("from_dict not implemented for Grade 8")
