import os
import shutil
import re
import json
import importlib.util
from tkinter import filedialog
import tkinter as tk
import PySimpleGUI as sg
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from dependency_agg import find_third_party_imports
from abstract_utilities.read_write_utils import write_to_file, read_from_file, read_or_write
from gui_template import get_gui_fun,while_basic
from folderbrowser import get_browser
import os
import shutil
from abstract_utilities.read_write_utils import read_or_write
from nltk.tokenize import word_tokenize
def read_with_different_encodings(file_path):
    """Attempt to read a file with different encodings."""
    encodings = ['utf-8', 'latin-1', 'utf-16', 'cp1252', 'ascii']  # List of encodings to try
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read()
                return content
        except UnicodeDecodeError:
            continue
    raise Exception(f'Failed to read file {file_path} with any encoding in the list.')

def create_directory_map(path, prefix=""):
    dir_map = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                dir_map.append(prefix + entry.name + "/")
                dir_map.extend(create_directory_map(os.path.join(path, entry.name), prefix + "  "))
            elif is_file(entry):
                dir_map.append(prefix + entry.name)
    for line in dir_map:
        print(line)
    return dir_map
def create_directory_map(folder_path):
    directory_map = {}
    replica_folder_path = folder_path + "_replica"
    # Remove the replica folder if it exists, and create a new one
    if os.path.exists(replica_folder_path):
        shutil.rmtree(replica_folder_path)
   
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            tokens = 0
            print(file_path)
            content =read_with_different_encodings(file_path)
            if content != None:
                tokens = len(word_tokenize(content))
            # Create a blank file in the replica folder
            directory_map[file_path] = {"size": size, "tokens": tokens}
    print(json.dumps(directory_map, indent=2))
    return directory_map

def get_file_info(root,file):
        file_path = os.path.join(root, file)
        size = os.path.getsize(file_path)
        tokens = 0
        print(file_path)
        content =read_with_different_encodings(file_path)
        if content != None:
            tokens = len(word_tokenize(content))
        # Create a blank file in the replica folder
        return {"name":file,"path":file_path,"size": size, "tokens": tokens}
def extract_summary(file_path):
    """
    Extract a summary of the Python script.

    Args:
        file_path (str): The path to the Python script.

    Returns:
        str: The summary of the script.
    """
    with open(file_path, "r") as file:
        content = file.read()
        sentences = sent_tokenize(content)
        summary = " ".join(sentences[:3])  # Extract the first three sentences as the summary
    return summary


def extract_info(file_path, pattern):
    """
    Extract information from a Python script using a specified pattern.

    Args:
        file_path (str): The path to the Python script.
        pattern (str): The regular expression pattern for extraction.

    Returns:
        list: A list of matched information found in the script.
    """
    info = []
    with open(file_path, "r") as file:
        content = file.read()
        matches = re.findall(pattern, content, re.DOTALL)
        info.extend(matches)
    return info

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_relative_path(path, base_path):
    """
    Get the relative path of a file or directory from a base directory.

    Args:
        path (str): The path to the file or directory.
        base_path (str): The base directory path.

    Returns:
        str: The relative path of the file or directory.
    """
    return os.path.relpath(path, base_path)

def get_files_in_directory(directory):
    """
    Get the list of files in a directory.

    Args:
        directory (str): The path to the directory.

    Returns:
        list: A list of file names.
    """
    files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            files.append(file)
    return files

def get_filtered_files(directory):
    excluded_files = ['__pycache__', 'main.py', '__init__.py']
    excluded_directories = ['__pycache__']
    modules = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item not in excluded_files:
            if item_path.endswith('.py'):
                modules.append(import_module_from_file(item_path))
        elif os.path.isdir(item_path) and item not in excluded_directories:
            modules.extend(get_filtered_files(item_path))
    return modules

def create_main(module_name):
    return f"""import os
import importlib.util

excluded_files = ['__pycache__', 'main.py', '__init__.py']
excluded_directories = ['__pycache__']

def import_module_from_file(file_path):
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def get_filtered_files(directory):
    modules = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) and item not in excluded_files:
            if item_path.endswith('.py'):
                modules.append(import_module_from_file(item_path))
        elif os.path.isdir(item_path) and item not in excluded_directories:
            modules.extend(get_filtered_files(item_path))
    return modules


def main():
    print("Hello, this is {module_name}.")
    # You can import and use other modules or functions of {module_name} here.
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)

    filtered_modules = get_filtered_files(directory_path)

if __name__ == "__main__":
    # Get the absolute directory path of the current script file
    main()"""

def create_directory_map_gui():
    folder_path = sg.popup_get_folder("Select folder to create directory map")
    if folder_path:
        directory_map = create_directory_map(folder_path)
        output_file = sg.popup_get_file("Save directory map as", save_as=True, default_extension=".txt")
        write_to_file(output_file,json.dumps(directory_map, indent=2))
        sg.popup(f"Directory map created successfully!\n\nOutput file: {output_file}")

def directory_map_GUI():
    # Get the parent directory from the user
    parent_dir = get_browser(text='please select your projects parent directory')
    if parent_dir is None:
        return

    # Get the subdirectories in the parent directory
    subdirs = [name for name in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, name))]

    # Ask the user to select directories
    layout = [[sg.Text('select projects for directory analysis'),sg.Listbox(values=subdirs, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(50, len(subdirs))), sg.Button('OK')]]
    window = sg.Window('directory analysis', layout)
    selected_dirs = None
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            selected_dirs = values[0]
            break
    window.close()
    if not selected_dirs:
        return 
    # Ask the user where to create the data directory
    data_dir_parent = get_browser(text=f'location of data directory for {selected_dirs}')
    if data_dir_parent is None:
        return
        
    # Create the data directory and the selected directories inside it
    data_dir = os.path.join(data_dir_parent, 'data_directory')
    os.makedirs(data_dir, exist_ok=True)

    for dir in selected_dirs:
        path = os.path.join(data_dir, dir)
        os.makedirs(path, exist_ok=True)
        write_to_file(os.path.join(path,'directory_map.json'),json.dumps({'original_directory':os.path.join(parent_dir,dir),'directory_map':create_directory_map(os.path.join(parent_dir,dir))}))
    sg.popup('Folders successfully created!')
    return data_dir_parent

def find_third_party_imports_gui():
    folder_path = get_browser('Folder')
    if folder_path:
        imports = find_third_party_imports(folder_path)
        output_file = os.path.join(folder_path, "third_party_imports.txt")
        write_to_file("\n".join(imports), output_file)
        sg.popup(f"Third-party imports found successfully!\n\nOutput file: {output_file}")

def create_startup_file_gui():
    folder_path = get_browser('Folder')

    if folder_path:
        module_name = folder_path.split('/')[-1]
        requires = find_third_party_imports(os.path.join(folder_path, module_name))
        readme = os.path.join(folder_path, "README.md")
        short_description = "The startup file has been created successfully!"
        email = "example@example.com"
        author = "Your Name"
        entity = "Your Entity"
        startup_file_content = create_startup_file(folder_path, requires, readme, short_description, email, author, entity)
        output_file = os.path.join(folder_path, "startup.py")
        write_to_file(startup_file_content, output_file)
        sg.popup(f"Startup file created successfully!\n\nOutput file: {output_file}")

def create_project_structure(directory):
    """
    Create a basic project structure in the given directory.

    Args:
        directory (str): The path to the directory.
    """
    subdirectories = ["src", "tests", "docs", "data"]
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(directory, subdirectory)
        os.makedirs(subdirectory_path, exist_ok=True)
    main_file = os.path.join(directory, "src", "main.py")
    if not os.path.exists(main_file):
        with open(main_file, "w") as file:
            file.write("# Entry point of the project")

def create_module_structure(directory, module_name):
    """
    Create a basic module structure in the given directory.

    Args:
        directory (str): The path to the directory.
        module_name (str): The name of the module.
    """
    module_directory = os.path.join(directory, module_name)
    os.makedirs(module_directory, exist_ok=True)
    module_file = os.path.join(module_directory, f"{module_name}.py")
    if not os.path.exists(module_file):
        with open(module_file, "w") as file:
            file.write(f"# {module_name} module")

def abstract_utilities_layout():
    return [[sg.Button("Create Directory Map", key="-DIRECTORY_MAP-")],
            [sg.Button("Find Third-Party Imports", key="-THIRD_PARTY_IMPORTS-")],
            [sg.Button("Create Startup File", key="-STARTUP_FILE-")],
            [sg.Button("Exit")]]

def return_script_info_extractor_layout():
    patterns = {
        "Summary": None,  # Placeholder for summary extraction
        "Docstrings": r'def\s+\w+\s*\((?:(?!\)).)*?\):\s*("""|\'\'\')(.*?)\1',
        "Function Names": r'def\s+(\w+)\s*\(',
        "Function Parameters": r'def\s+\w+\s*\((.*?)\):'
    }
    return [[sg.Text("Select a Python script file:")],
            [sg.Input(key="-FILE-"), sg.FileBrowse()],
            [sg.Text("Select the information to extract:")],
            [sg.Combo(list(patterns.keys()), key="-PATTERN-")],
            [sg.Button("Extract Information")],
            [sg.Multiline(key="-OUTPUT-", size=(50, 10))]]

def return_project_manager_layout():
    return [
        [sg.Text("Select a directory:")],
        [sg.Input(key="-FOLDER-", enable_events=True), sg.FolderBrowse()],
        [sg.Tree(data=sg.TreeData(), headings=["name","path","size","tokens"], auto_size_columns=True, num_rows=20, key="-TREE-", expand_x= True,expand_y= True)],
        [sg.Button("Create Directory Map", key="-DIRECTORY_MAP-"),
         sg.Button("Find Third-Party Imports", key="-THIRD_PARTY_IMPORTS-"),
         sg.Button("Create Project", key="-CREATE_PROJECT-"),
         sg.Button("Create Module", key="-CREATE_MODULE-")],
        [sg.Multiline(key="-OUTPUT-", size=(50, 10), disabled=True, auto_size_text=True, expand_x= True,expand_y= True)]]

sg.theme("DefaultNoMoreNagging")
window = sg.Window("Abstract Utilities", return_project_manager_layout(),resizable= True, auto_size_text=True)
if 'parent' not in globals():
      globals()['parent'] = directory_map_GUI()
while True:
    event, values = window.read()
    
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    if event == "-DIRECTORY_MAP-":
        create_directory_map_gui()

    if event == "-THIRD_PARTY_IMPORTS-":
        find_third_party_imports_gui()

    if event == "-STARTUP_FILE-":
        create_startup_file_gui()

    if event == "Extract Information":
        file_path = values["-FILE-"]
        if values["-PATTERN-"] != '':
            pattern = patterns[values["-PATTERN-"]]
            if values["-PATTERN-"] == "Summary":
                summary = extract_summary(file_path)
                window["-OUTPUT-"].update(summary)
            elif values["-PATTERN-"] == "Docstrings":
                info = extract_info(file_path, pattern)
                # Convert tuple-based info to strings
                info = [str(item) for item in info]
                window["-OUTPUT-"].update("\n".join(info))
            else:
                info = extract_info(file_path, pattern)
                window["-OUTPUT-"].update("\n".join(info))

    if event == "-FOLDER-":
        folder_path = values["-FOLDER-"]
        files = get_files_in_directory(folder_path)
        tree_data = sg.TreeData()
        for file in files:
            relative_path = get_relative_path(os.path.join(folder_path, file), folder_path)
            info_js=get_file_info(folder_path,file)
            tree_data.Insert("","project_1", "project_1", [info_js["name"],info_js["path"],info_js["size"],info_js[ "tokens"]])
        window["-TREE-"].Update(tree_data)

    if event == "-CREATE_PROJECT-":
        if folder_path:
            create_project_structure(folder_path)
            window["-OUTPUT-"].update("Project structure created successfully!")
        else:
            window["-OUTPUT-"].update("Please select a directory first!")

    if event == "-CREATE_MODULE-":
        if folder_path:
            module_name = sg.popup_get_text("Enter the name of the module:")
            if module_name:
                create_module_structure(folder_path, module_name)
                window["-OUTPUT-"].update("Module structure created successfully!")
            else:
                window["-OUTPUT-"].update("Module name cannot be empty!")
        else:
            window["-OUTPUT-"].update("Please select a directory first!")

window.close()
