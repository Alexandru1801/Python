from sys import argv
import magd_library

if len(argv) == 1:
    print("""
        User, use the following options:

        r <text filename> : load text file, add data into binary file (replacing a existing student when there is a match)
        s <student name> : show single student data
        d <part of the name> : delete student records if their name contain given pattern (minimum 3 characters)
        m : show list of students with their grades from high to low
        p <threshold>: calculate the number of students above the given threshold grade
        a : calculate the average of the grades for the whole class
        o : show students with above average grades
    """)
    exit()

if argv[1] == "r":
    if len(argv) < 3:
        raise ValueError("Error: filename misssing")
    filename = argv[2]
    magd_library.load_bin_file(filename)


elif argv[1] == "s":
    if len(argv) < 3:
        raise ValueError("Error: student name missing")
    student_name = " ".join(argv[2:])
    magd_library.search_name(student_name)


elif argv[1] == "d":
    if len(argv) < 3:
        raise ValueError("Error: part of name missing")
    part_of_name = argv[2]
    students_deleted = magd_library.delete_student(part_of_name)
    print("-" * 80)
    print("Students deleted:")
    for student in students_deleted:
        print(f"{student[0]} {student[1]} {student[2]} {student[3]}")
    print("-" * 80)


elif argv[1] == "m":
    if len(argv) != 2:
        raise ValueError("Error: option mode missing")
    students = magd_library.show_ordered_by_mark()
    print("-" * 80)
    print(f"{'Name':28} {'Mark':18} {'Email':22} {'Phone':12}")
    print("-" * 80)
    for student in students:
        print(f"{student[0]:30} {student[1]:12} {student[2]:26} {student[3]}")
    print("-" * 80)


elif argv[1] == "p":
    if len(argv) < 3:
        raise ValueError("Error: threshold missing")
    threshold = argv[2]
    student_counter = magd_library.students_above(threshold)
    print(f"The number of students that are above the threshold {threshold} are: {student_counter}")


elif argv[1] == "a":
    if len(argv) != 2:
        raise ValueError("Error: option mode missing")
    average = magd_library.calculate_average()
    print(f"The average of all the stundents is: {average}")


elif argv[1] == "o":
    if len(argv) != 2:
        raise ValueError("Error: option mode missing")
    students = magd_library.show_above_average()
    print("-" * 80)
    print(f"{'Name':28} {'Mark':18} {'Email':22} {'Phone':12}")
    print("-" * 80)
    for student in students:
        print(f"{student[0]:30} {student[1]:12} {student[2]:26} {student[3]}")
    print("-" * 80)
