import PySimpleGUI as sg
import re

def extract_docstrings(file_path):
    """
    Extract docstrings from a Python script.

    Args:
        file_path (str): The path to the Python script.

    Returns:
        list: A list of docstrings found in the script.
    """
    docstrings = []
    with open(file_path, "r") as file:
        content = file.read()
        pattern = r'def\s+\w+\s*\((?:(?!\)).)*?\):\s*("""|\'\'\')(.*?)\1'
        matches = re.findall(pattern, content, re.DOTALL)
        docstrings.extend([match[1] for match in matches])
    return docstrings


def extract_function_names(file_path):
    """
    Extract function names from a Python script.

    Args:
        file_path (str): The path to the Python script.

    Returns:
        list: A list of function names found in the script.
    """
    function_names = []
    with open(file_path, "r") as file:
        content = file.read()
        pattern = r'def\s+(\w+)\s*\('
        matches = re.findall(pattern, content)
        function_names.extend(matches)
    return function_names


def extract_function_parameters(file_path):
    """
    Extract function parameters from a Python script.

    Args:
        file_path (str): The path to the Python script.

    Returns:
        list: A list of function parameters found in the script.
    """
    function_parameters = []
    with open(file_path, "r") as file:
        content = file.read()
        pattern = r'def\s+\w+\s*\((.*?)\):'
        matches = re.findall(pattern, content)
        for match in matches:
            parameters = match.split(',')
            parameters = [param.strip() for param in parameters]
            function_parameters.extend(parameters)
    return function_parameters


def main():
    layout = [
        [sg.Text("Select a Python script file:")],
        [sg.Input(key="-FILE-"), sg.FileBrowse()],
        [sg.Button("Extract Docstrings")],
        [sg.Button("Extract Function Names")],
        [sg.Button("Extract Function Parameters")],
        [sg.Multiline(key="-OUTPUT-", size=(50, 10))]
    ]

    window = sg.Window("Python Script Info Extractor", layout)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == "Extract Docstrings":
            file_path = values["-FILE-"]
            docstrings = extract_docstrings(file_path)
            window["-OUTPUT-"].update("\n".join(docstrings))

        if event == "Extract Function Names":
            file_path = values["-FILE-"]
            function_names = extract_function_names(file_path)
            window["-OUTPUT-"].update("\n".join(function_names))

        if event == "Extract Function Parameters":
            file_path = values["-FILE-"]
            function_parameters = extract_function_parameters(file_path)
            window["-OUTPUT-"].update("\n".join(function_parameters))

    window.close()
