from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
 
root = Tk()
root.title("Итоговая таблица")
root.geometry("640x480")
 
#root.grid_rowconfigure(index=0, weight=1)
#root.grid_columnconfigure(index=0, weight=1)
#root.grid_columnconfigure(index=1, weight=1)
 
def replace_dots_with_commas(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if lines:
        last_line = lines[-1].replace('.', ',')
        lines[-1] = last_line

        with open(file_path, 'w') as file:
            file.writelines(lines)

def open_files():
    global file_paths
    filepaths = filedialog.askopenfilenames(filetype=(('txt file', '*.txt'), ('Any', '*')))
    if filepaths != "":
        pass
    file_paths = filepaths
    return file_paths

def get_first_value_before_tab(input_string):
    # Split the input string based on the tab character
    values = input_string.split('\t')

    # Check if there is at least one value before the tab
    if len(values) > 1:
        # Return the first value before the tab
        return values[0]
    else:
        # If there is no tab, return the original string
        return input_string

# Example usage
#input_string = "value1\tvalue2\tvalue3"
#result = get_first_value_before_tab(input_string)
#print(result)

def extract_first_line_value(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines:
            first_value = get_first_value_before_tab(lines[1])
            return first_value.strip()[:-7] if len(lines[0]) >= 7 else "xxx"
            #return lines[0].strip()[:-7] if len(lines[0]) >= 7 else ""
        else:
            return None

def extract_first_line_value1(file_path):
    return file_path[:-7]
    

def extract_second_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[1].strip()
        else:
            return None

def convert_to_number_except_first(value):
    parts = value.split()
    if parts:
        first_part = parts[0]
        rest_of_parts = [str(float(part)) if part.replace(".", "", 1).isdigit() else part for part in parts[1:][:-6]]
        return ' '.join([first_part] + rest_of_parts)
    return value

def merge_second_lines(input_file_paths, output_file_path):
    first_line_first_value = None
    sums = [0.0] * 5  # Initialize sums for the five values

    with open(output_file_path, 'w') as output_file:
        for file_path in input_file_paths:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines:
                    #first_line_first_value = lines[0].strip()[:-7] if len(lines[0]) >= 7 else ""
                    first_line_first_value = extract_first_line_value(file_path)

                second_line = extract_second_line(file_path)
                if second_line is not None:
                    converted_value = convert_to_number_except_first(second_line)
                    output_file.write(converted_value + '\n')

                    # Update sums for the second to the fifth values
                    values = [float(part) for part in converted_value.split()[1:]]
                    for i in range(min(5, len(values))):
                        sums[i] += values[i]

        # Write the summary line
        summary_line = f"{first_line_first_value}\t{sums[0]}\t{sums[1]}\t{sums[2]}\t{sums[3]}\n"
        output_file.write(summary_line)

open_files()

current_path = os.path.dirname(file_paths[0])
# Output file path
output_file_path = current_path + '/output.txt'

# Merge second lines into the output file and add the summary line
merge_second_lines(file_paths, output_file_path)

replace_dots_with_commas(output_file_path)

print(f"Second lines from {len(file_paths)} files merged into {output_file_path}.")
root.destroy()
#root.mainloop()