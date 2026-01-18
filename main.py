# main.py
import sys
from datetime import date
from typing import Optional # <-- ADDED typing import
from system_manager import StudentManagementSystem
from student import Student
from study_field import StudyField

# --- Utility Functions for Input Handling (parse_date_input) ---
# ... (contents are the same as before) ...
def parse_date_input(date_str: str) -> Optional[date]:
    try:
        day, month, year = map(int, date_str.split('/'))
        return date(year, month, day)
    except ValueError:
        print("Error: Date must be in a valid DD/MM/YYYY format (e.g., 01/04/2002).")
        return None
# --- Menu Functions (print_menus) ---
# ... (contents are the same as before) ...
def print_main_menu():
    print("\n=============================================")
    print("Welcome to TUM's Student Management System!")
    print("=============================================")
    print("What do you want to do?")
    print(" g - General operations")
    print(" f - Faculty operations")
    print(" q - Quit Program")
    print("=============================================")

def print_general_operations_menu():
    print("\n--- General Operations ---")
    print(" nf/<name>/<abbr>/<field> - Create new faculty")
    print(" ss/<email>               - Search student and show faculty")
    print(" df                       - Display all faculties")
    print(" of/<field>               - Display faculties of a field")
    print(" b - Back to main menu")
    print(" q - Quit Program")
    print(f"Available Fields: {', '.join([f.name for f in StudyField])}")

def print_faculty_operations_menu():
    print("\n--- Faculty Operations ---")
    print(" ns/<abbr>/<fname>/<lname>/<email>/<date(DD/MM/YYYY)> - Enroll new student") 
    print(" gs/<abbr>/<email>                                     - Graduate student")
    print(" ds/<abbr>                                             - Display enrolled students")
    print(" dg/<abbr>                                             - Display graduated students")
    print(" bf/<abbr>/<email>                                     - Check if student belongs to faculty")
    print(" b - Back to main menu")
    print(" q - Quit Program")
    
# --- Core Logic Handlers (handle_operations) ---
# ... (contents are the same as before) ...
def handle_general_operation(system: StudentManagementSystem, command: str):
    parts = command.split('/')
    op_code = parts[0]
    
    if op_code == 'nf':
        if len(parts) == 4:
            system.create_faculty(parts[1], parts[2], parts[3])
        else:
            print("Error: 'nf' requires 3 arguments: <name>/<abbr>/<field>.")
    elif op_code == 'ss':
        if len(parts) == 2:
            email = parts[1]
            faculty = system.find_faculty_by_student_email(email)
            if faculty:
                print(f"Success: Student '{email}' belongs to faculty: {faculty.name} ({faculty.abbreviation}).")
            else:
                print(f"Result: Student '{email}' was not found in any faculty.")
        else:
            print("Error: 'ss' requires 1 argument: <email>.")
    elif op_code == 'df':
        if len(parts) == 1:
            system.display_university_faculties()
        else:
            print("Error: 'df' takes no arguments.")
    elif op_code == 'of':
        if len(parts) == 2:
            system.display_faculties_by_field(parts[1])
        else:
            print("Error: 'of' requires 1 argument: <field>.")
    else:
        print(f"Error: Operation '{op_code}' is not a valid General operation.")
        
def handle_faculty_operation(system: StudentManagementSystem, command: str):
    parts = command.split('/')
    op_code = parts[0]
    
    if len(parts) > 1:
        abbr = parts[1].upper()
        faculty = system.get_faculty(abbr)

        if not faculty and op_code != 'ns':
            print(f"Error: Faculty with abbreviation '{abbr}' not found.")
            return
    else:
        if op_code in ['ns', 'gs', 'ds', 'dg', 'bf']:
            print(f"Error: '{op_code}' requires an argument.")
            return

    if op_code == 'ns':
        if len(parts) == 6:
            if not faculty:
                print(f"Error: Faculty with abbreviation '{abbr}' not found. Cannot enroll student.")
                return

            first_name, last_name, email = parts[2], parts[3], parts[4]
            date_str = parts[5]
            
            dob = parse_date_input(date_str)
            enrollment_date = date.today()
            
            if dob:
                if system.find_faculty_by_student_email(email):
                    print(f"Error: Student with email '{email}' is already enrolled in another faculty.")
                    return

                new_student = Student(first_name, last_name, email, enrollment_date, dob)
                if faculty.enroll_student(new_student):
                    print(f"Success: Student '{first_name} {last_name}' enrolled in {abbr}.")
        else:
            print("Error: 'ns' requires 5 arguments: <abbr>/<fname>/<lname>/<email>/<date(DD/MM/YYYY)>.")

    elif op_code == 'gs':
        if len(parts) == 3:
            email = parts[2]
            graduated_student = faculty.graduate_student(email)
            if graduated_student:
                print(f"Success: Student '{email}' graduated from {abbr}.")
            else:
                print(f"Error: Cannot graduate student. Student with email '{email}' not found or already graduated in {abbr}.")
        else:
            print("Error: 'gs' requires 2 arguments: <abbr>/<email>.")
            
    elif op_code == 'ds':
        if len(parts) == 2:
            faculty.display_enrolled_students()
        else:
            print("Error: 'ds' takes 1 argument: <abbr>.")
            
    elif op_code == 'dg':
        if len(parts) == 2:
            faculty.display_graduates()
        else:
            print("Error: 'dg' takes 1 argument: <abbr>.")
            
    elif op_code == 'bf':
        if len(parts) == 3:
            email = parts[2]
            student = faculty.find_student_by_email(email)
            
            if student:
                print(f"Yes: Student '{email}' belongs to faculty {abbr}. Status: {'Enrolled' if student.is_enrolled() else 'Graduated'}")
            else:
                print(f"No: Student '{email}' does NOT belong to faculty {abbr}.")
        else:
            print("Error: 'bf' requires 2 arguments: <abbr>/<email>.")

    else:
        print(f"Error: Operation '{op_code}' is not a valid Faculty operation.")

# --- Main Program Execution ---

def run_cli():
    """
    The main program loop for the Student Management System.
    """
    system = StudentManagementSystem()
    current_state = 'main'
    
    # Pre-populate some data for easier testing 
    print("Initializing system with some example data...")
    system.create_faculty("Faculty of Computers, Informatics, and Microelectronics", "FCIM", "SOFTWARE_ENGINEERING")
    system.create_faculty("Faculty of Food Technology", "FTC", "FOOD_TECHNOLOGY")
    
    fcim = system.get_faculty("FCIM")
    
    # Enroll a test student 
    test_student_1_dob = parse_date_input("1/4/2002")
    test_student_1_enroll = date.today() 
    if test_student_1_dob and fcim: 
        test_student_1 = Student("Ionel", "Gavrev", "i.gavrev@isa.utm.md", test_student_1_enroll, test_student_1_dob)
        if fcim.enroll_student(test_student_1):
            print("Example student enrolled successfully.")


    while True:
        try:
            if current_state == 'main':
                print_main_menu()
            elif current_state == 'general':
                print_general_operations_menu()
            elif current_state == 'faculty':
                print_faculty_operations_menu()

            user_input = input("your input> ").strip()

            if not user_input:
                continue

            op_char = user_input[0].lower()
            
            if op_char == 'q':
                print("Quitting Program. Goodbye!")
                break
            
            if op_char == 'b' and current_state != 'main':
                current_state = 'main'
                continue
            elif op_char == 'b' and current_state == 'main':
                print("You are already at the main menu.")
                continue

            # State transition logic
            if current_state == 'main':
                if op_char == 'g':
                    current_state = 'general'
                elif op_char == 'f':
                    current_state = 'faculty'
                else:
                    print("Error: Invalid main menu selection. Use 'g', 'f', or 'q'.")
            
            # Command execution logic
            elif current_state == 'general':
                handle_general_operation(system, user_input)

            elif current_state == 'faculty':
                handle_faculty_operation(system, user_input)

        except KeyboardInterrupt:
            print("\nProgram interrupted. Quitting Program. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected internal error occurred: {e}. Please try again.")

if __name__ == "__main__":
    run_cli()
