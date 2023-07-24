import os
import importlib
import inspect
import PySimpleGUI as sg
import os
import tkinter as tk
from tkinter import filedialog
def gather_header_docs(folder_path):
    header_docs = ""
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".py"):
            module_name = file_name[:-3]  # Remove the file extension
            try:
                module = __import__(module_name)
            except ImportError:
                continue  # Skip modules that cannot be imported

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, "__doc__"):
                    docstring = inspect.getdoc(obj)
                    if docstring:
                        header_docs += f"{name}:\n{docstring}\n\n"

    return header_docs

def main():
    # Initialize tkinter
    root = tk.Tk()
    root.withdraw()

    # Open directory selection dialog
    start_path = filedialog.askdirectory(title="Select starting directory")
    header_docs = gather_header_docs(folder_path)
    print(header_docs)

if __name__ == "__main__":
    main()
