# This is a basic program that allows the user to input, remove, view and search for student records.
# These records are saved to a JSON file, which the program can read from in future sessions to retain any previous input.

# Privacy Note: This program only stores names, subjects, and grades. Data is saved locally and should never be shared externally.

import json # Required library in order to save and load student records in and from a JSON file

should_i_loop = True # Controls whether the main loop keeps running

# Menu text displayed to the user
menu_options = """
1. Add Student Record
2. Remove Student Record
3. View Record List
4. Search For Existing Record
5. Exit"""

def load_records():
    global records
    try:
        # Tries to open the JSON file and to load existing records
        with open("student_records.json", "r") as f:
            content = f.read().strip()
            if content:
                records = json.loads(content) # Loads records if file has content
            else:
                # Starts with empty list if file is blank
                records = []
    except FileNotFoundError:
        # If file doesn't exist, it will initialize with empty list
        records = []

def main_menu():
    global should_i_loop
    while should_i_loop is True:
        try:
            # Displays menu options to the user
            print("====")
            print("Student Record Safekeeping")
            print(menu_options)
            print("=====\n")

            user_choice = int(input("Select an option (1-5): "))

            # User choice determines which functions will run
            if user_choice == 1:
                add_student_record()
            elif user_choice == 2:
                remove_student_record()
            elif user_choice == 3:
                view_record_list()
            elif user_choice == 4:
                search_student_record()
            elif user_choice == 5:
                print("Exiting program..", "\n")
                break
            else:
                print("Invalid input. Please select from numbers 1 to 5.")
                continue
        except (ValueError, MemoryError):
            # Handles non-numeric input or memory issues (too many numbers, etc)
            print("Invalid input. Please only use numbers between 1 to 5.")
            continue

def add_student_record():
    global records
    try:
        # Collects student details from user - name, subject and grade

        # Prompts user to input student name. Checks to ensure student name is purely alphabetic
        student_name = input("Input student's name: ").title()
        if student_name.isalpha() == False:
            print("Student name must only contain alphabetic characters. Please try again.")
            return

        # Prompts user to input field of study. Checks to ensure field of study is only alphabetic
        student_subject = input("Input student's subject of study: ").title()
        if student_subject.isalpha() == False:
            print("Subject must only contain alphabetic characters. Please try again.")
            return

        # Prompts user for student grade. Checks that grade is between 0 and 100 before accepting
        student_grade = int(input("Input student's final grade: "))
        if student_grade < 0 or student_grade > 100:
            print("Grade must be between 0 and 100. Please try again.")
            return

        # Stores previously inputted details in a dictionary, which will then be sent to a JSON file to enable saving
        student_record = {
            "name": student_name,
            "subject": student_subject,
            "grade": student_grade
        }

        # Adds the newly created student record to the list
        records.append(student_record)

        # Saves updated list with new student record back to JSON file
        with open("student_records.json", "w") as f:
            json.dump(records, f, indent=4)

        print("Student record added successfully!")
        return
    except (ValueError, MemoryError):
        # Handles invalid grade input or memory issues (too many numbers, etc)
        print("Invalid input. Either your grade input was invalid, or there was a memory error (too many numbers). Please try again.")
        return

def remove_student_record(): 
    global records
    target_student_name = input("Enter the student's name to remove: ").title()
    if target_student_name.isalpha() == False:
        print("Student name must only contain alphabetic characters. Please try again.")
        return

    # Find all records matching the given name (case-insensitive)
    matches = []
    for record in records:
        if record['name'].title() == target_student_name:
            matches.append(record)

    if len(matches) == 0:
        print("No records found for that student.")
        return

    elif len(matches) == 1:
        # If only one match, the program will remove it directly without any further complication on the end of the user
        records.remove(matches[0])
        
        with open("student_records.json", "w") as f:
            json.dump(records, f, indent=4)
        print("Record removed successfully!")
    else:
        # If there are multiple matches for the same name, this will allow the user to choose which one they wish to delete
        print("More than one student has that name:")
        for num, record in enumerate(matches, 1):
            print(f"{num}. Subject: {record['subject']} | Grade: {record['grade']}")
        try:
            user_mult_name_choice = int(input("Enter the number of the record you wish to remove: "))
            if 1 <= user_mult_name_choice <= len(matches):
                records.remove(matches[user_mult_name_choice - 1])
                with open("student_records.json", "w") as f:
                    json.dump(records, f, indent=4)
                print("Record removed successfully!")
            else:
                print("Invalid choice. Please only enter numbers within the list.")
        except ValueError:
            print("Please enter a valid number.")

def view_record_list():
    global records

    if len(records) == 0:
        print("No student records found.")
        return

    # Displays all saved student records in an ordered number list
    print("\n==== Student Records ====")
    for num, record in enumerate(records, start=1):
        print(f"{num}. Name: {record['name']}.")
        print(f"{num}. Subject: {record['subject']}.") 
        print(f"{num}. Grade: {record['grade']}.") 
    print("=====\n")

def search_student_record():
    global records

    target_student_name = input("Enter the student's name to search: ").lower()

    if target_student_name.isalpha() == False:
        print("Subject must only contain alphabetic characters. Please try again.")
        return

    student_name_matches = []

    for record in records:
        if record['name'].lower() == target_student_name:
            student_name_matches.append(record)

    if len(student_name_matches) == 0:
        print("No records found for that student.")
        return

    print(f"\nFound {len(student_name_matches)} existing records for '{target_student_name.title()}':")

    # Loops through each record that matches the inputted name, formats, and prints them accordingly
    for num, record in enumerate(student_name_matches, 1):
        print("====")
        print(f"{num}. Name: {record['name']}.")
        print(f"{num}. Subject: {record['subject']}.") 
        print(f"{num}. Grade: {record['grade']}.") 

if __name__ == '__main__':
    # Loads existing records before starting the menu loop
    load_records()
    main_menu()

