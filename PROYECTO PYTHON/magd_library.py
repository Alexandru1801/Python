import pickle

class StudentNotFoundError(Exception):
    pass

class MarkRangeError(Exception):
    pass

class NumberCharacterError(Exception):
    pass


def get_bin_filename():
    """Takes the name of the bin file who is stored in the .cfg file

    Output(str): the name of the binary file
    """
    try:
        config_file = open("students.cfg")
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file {config_file} is not found.")
    for line in config_file:
        line = line.split()
        if len(line) < 3:
            raise ValueError("The file must have the next struture file = <filename.bin>")
        else:
            bin_filename = line[2].strip()
    config_file.close()
    return bin_filename


def correct_the_file(text_data):
    """
    Takes the txt file with de students and correct the structure (delete blank spaces)

    text_file (str): the given text file to be corrected
    Output: the file corrected stored into a list
    """
    if text_data is None:
        raise ValueError("The file must not be empty")

    cleaned_lines = []
    for line in text_data:
        line = line.replace('\t', '').strip()
        if line:
            cleaned_lines.append(line)
    return cleaned_lines


def remove_suffix(name):
    """
    Takes the name of a student reapeted in a dictionaty who stores the data of all, and removes the _number 
    to can work with the name of that student.
    
    name(str): the name of the student
    """
    parts = name.split("_", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return name


def text_to_binary(text_data):
    """
    Takes the text file, and with the given name of the binary file, transform the text data in binary

    txt_file = the specified text file
    """
    bin_file = get_bin_filename()
    try:
        bin_file = open(bin_file, "wb")
        pickle.dump(text_data, bin_file)
        bin_file.close()
    except FileNotFoundError:
        print(f"The file {text_data} does not exist or is not found")
        raise


def binary_to_text(bin_filename):
    """
    Takes as parameter the binanry file and pass the information
    that contains to text to work with it

    bin_file(bin): the given binary file
    Output(list): in case of there is an error, give an empty list
    """
    try:
        return pickle.load(bin_filename)
    except (pickle.UnpicklingError, EOFError):
        print(f"Error: The file {bin_filename} did not have a valid format.")
        return []


def read_txt_content(text_filename):
    """
    Read the content in the given text_file, and store it into a list

    text_filename(file): the file with the given data
    Output(list): the data ready to work with it
    """
    text_file = open(text_filename, encoding="utf-8")
    text_data = text_file.readlines()
    text_file.close()
    text_data = correct_the_file(text_data)
    return text_data


def take_binary_content(binary_filename):
    """
    Takes the data into the binary file and store its in a dictionary with the following struture:
    key: name of student, and values: mark, mail and phone.

    binary_file(bytes): the given file to work with it
    Output(dit): the students stored into a dict, the keys are the names of each student
    and the values are the remaining data
    """
    binary_data = {}
    bin_content = binary_to_text(binary_filename)

    for record in bin_content:
        if record:
            if isinstance(record, str):
                fields = [x.strip() for x in record.split(",")]
            else:
                fields = [str(x).strip() for x in record]
            name = fields[0]
            binary_data[name] = fields[1:]
    return binary_data


def load_bin_file(filename):
    """
    Loads the data provided by the file and adds it into a binary file,
    update the data if is a match in the name and the mail or phone and add the new lines.

    filename(str): the text filename
    """
    text_content = read_txt_content(filename)
    bin_filename = get_bin_filename()

# CHECKS IF THE FILE IS EXISTING OR NOT
    try:
        bin_file = open(bin_filename, "rb")
        bin_info = take_binary_content(bin_file)
        bin_file.close()
        first_time = False
    except:
        first_time = True

    if first_time:
        bin_file = open(bin_filename, "wb")
        text_to_binary(text_content)
        print(f"Binary file created successfully")
        bin_file.close()
        return

# START UPDATING DE VALUES AND ADDING THE NEW ONES
    for line in text_content:
        fields = [x.strip() for x in line.split(",")]
        if len(fields) < 4:
            raise ValueError("The new lines must have Student name, mark, email and phone number")
        name = fields[0]
        mark = fields[1]
        email = fields[2]
        phone = fields[3]

        if name in bin_info:
            old_phone = bin_info[name][2]
            old_email = bin_info[name][1]

            if phone == old_phone or email == old_email:
                bin_info[name] = [mark, email, phone]
            else:
                i = 2
                new_name = f"{name}_{i}"
                while new_name in bin_info:
                    i += 1
                    new_name = f"{name}_{i}"
                bin_info[new_name] = [mark, email, phone]
        else:
            bin_info[name] = [mark, email, phone]

    final_data = []
    for key, data in bin_info.items():
        mark, email, phone = data
        final_data.append([remove_suffix(key), mark, email, phone])

    bin_f = open(bin_filename, "wb")
    text_to_binary(final_data)
    bin_f.close()

    print("Binary file updated successfully")


def search_name(student_name):
    """
    Search the given student name into de binary file and print it.

    student_name(str): the name of the student.
    """
    if not isinstance(student_name, str) or not student_name.strip():
        raise ValueError("You must give a valid name")
    
    for part in student_name.split():
        if not part.isalpha():
            raise ValueError("The name must contain only letters")

    bin_filename = get_bin_filename()

    bin_filename = open(bin_filename, "rb")
    bin_content = take_binary_content(bin_filename)
    bin_filename.close()

    pattern = student_name.lower()
    found = False

    for name, data in bin_content.items():
        if pattern in name.lower():
            found = True
            print("Student found:")
            print(f"  Name:  {name}")
            print(f"  Mark:  {data[0]}")
            print(f"  Email: {data[1]}")
            print(f"  Phone: {data[2]}\n")

    if not found:
        raise StudentNotFoundError(
            f"The student {student_name} is not in the list, try with another"
        )


def delete_student(part_of_name):
    """
    With a pattern of given letters delete all the students that have a mach in their names with that pattern

    part_of_name(str): pattern of letters, min 3 characters
    """

    if not isinstance(part_of_name, str) or not part_of_name.strip():
        raise ValueError("You must give a valid combination of characters upper than 3")

    if len(part_of_name) < 3:
        raise NumberCharacterError("You must write minimum 3 characters")

    bin_filename = get_bin_filename()
    bin_filename = open(bin_filename, "rb")
    bin_content = take_binary_content(bin_filename)
    bin_filename.close()

    students_deleted = [] # ONLY TO SHOW THE STUDENTS WHO HAVE BEEN DELETED
    remaining_students = []
    pattern = part_of_name.lower()
    for name, data in bin_content.items():
        if pattern in name.lower():
            students_deleted.append([name] + data)
        else:
            remaining_students.append([name] + data)

    if len(students_deleted) == 0:
        raise StudentNotFoundError(f"The is not a student with the following pattern: {part_of_name}, try again")

    bin_filename = text_to_binary(remaining_students)
    return students_deleted



def show_ordered_by_mark():
    """
    Orders the students by mark (higher to lower) and shows them all
    """
    bin_filename = get_bin_filename()

    bin_filename = open(bin_filename, "rb")
    bin_content = take_binary_content(bin_filename)
    bin_filename.close()

    desordered_list = []
    for key, value in bin_content.items():
        desordered_list.append([key] + value)

    n = len(desordered_list)
    for i in range(n):
        for j in range(n-1):
            if float(desordered_list[j][1]) < float(desordered_list[j+1][1]):
                desordered_list[j], desordered_list[j+1] = desordered_list[j+1], desordered_list[j]

    return desordered_list


def students_above(threshold):
    """
    Shows the students that are above a given threshold.
    
    threshold(int): the mark that the students need to superpass to be shown.
    """
    try:
        threshold = float(threshold)
    except ValueError:
        raise ValueError("You need to write numbers, please use the following syntax: <studen name>, <mark>, <mail>, <phone>")

    if threshold < 0 or threshold > 10:
        raise MarkRangeError("You need to select a value between 0 and 10 only")

    bin_filename = get_bin_filename()
    bin_filename = open(bin_filename, "rb")
    bin_content = take_binary_content(bin_filename)
    bin_filename.close()

    student_counter = 0
    for name, value in bin_content.items():
        mark = float(value[0])
        if mark > float(threshold):
            student_counter += 1

    return student_counter


def calculate_average():
    """
    Take the marks of all the students and calculate the average.
    """
    bin_filename = get_bin_filename()

    bin_filename = open(bin_filename, "rb")
    bin_info = take_binary_content(bin_filename)
    bin_filename.close()

    total = 0

    for key, value in bin_info.items():
        try:
            mark = float(value[0])
            total += mark
        except ValueError:
            ("The mark need to be a number, please use the following syntax: <studen name>, <mark>, <mail>, <phone>")

    avg = round(total / len(bin_info), 2)
    return avg


def show_above_average():
    """
    Using the average, show all the students that are above of the given mark.
    """
    average = calculate_average()
    students = []
    
    bin_filename = get_bin_filename()

    bin_filename = open(bin_filename, "rb")
    bin_info = take_binary_content(bin_filename)
    bin_filename.close()

    for key, value in bin_info.items():
        try:
            mark = float(value[0])
            if mark > average:
                students.append([key] + value)
        except ValueError:
            ("The mark need to be a number, please use the following syntax: <studen name>, <mark>, <mail>, <phone>")

    return students
