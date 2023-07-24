from folderbrowser import get_browser
from directory_map import create_directory_map
from dependency_agg import find_third_party_imports
from abstract_utilities.read_write_utils import write_to_file,read_from_file
from abstract_utilities import*
import json
import openai
import requests
#!/usr/bin/env python3
import openai
from dotenv import load_dotenv
import os
import getpass

import os
import importlib
import inspect
import PySimpleGUI as sg
import os
import tkinter as tk
import shutil
from tkinter import filedialog
def find_empty_glob():
  for k in range(0,len(globals())):
    name = f'new{k}'
    if f'new{k}' in globals():
      return name

def get_nums_to_it(ls):
  name = find_empty_glob()
  for k in range(0,len(ls)):
    globals()[f'{name}_{k}'] = ls[k]
  return name
import json
def js_replace(js,ls):
  keys = list(js.values())
  for k in range(0,len(keys)):
    js[keys[k]] = ls[0]
    ls = ls[1:]
  return js
def imgTF(file_path):
    """
    Checks if a file is an image based on its file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    if not imghdr.what(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return False
        except (UnicodeDecodeError, IOError) as e:
            print(f"Error reading file: {file_path}. {e}")
            return False
    else:
        return True

def get_json_it(ls):
  return {key: None for key in str(ls)[1:-1].split(',')}
def read_file_if_not_image(file_path):
    """
    Read the contents of a file if it is not an image.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The contents of the file if it is not an image, else None.
    """
    if not imgTF(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return None


def create_directory_map(folder_path):
    directory_map = {}
    replica_folder_path = folder_path + "_replica"
    # Remove the replica folder if it exists, and create a new one
    if os.path.exists(replica_folder_path):
        shutil.rmtree(replica_folder_path)
    shutil.copytree(folder_path, replica_folder_path, ignore=shutil.ignore_patterns('*.*'))  # Copy the folder structure only, excluding all files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            replica_file_path = file_path.replace(folder_path, replica_folder_path)
            size = os.path.getsize(file_path)
            tokens = 0
            content = read_file_if_not_image(file_path)
            if content is not None:
                tokens = tokenize(content)
            # Create a blank file in the replica folder
            if not imgTF(file_path):
                with open(replica_file_path, "w", encoding="utf-8"):
                    pass
            directory_map[file_path] = {"size": size, "tokens": tokens, 'image': imgTF(file_path)}
    print(json.dumps(directory_map, indent=2))
    return directory_map
def create_directory_map(folder_path):
    """
    Create a directory map with file information and docstrings for Python files.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        dict: The directory map containing file information and docstrings.
    """
    directory_map = {}
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            size = os.path.getsize(file_path)
            is_image = is_image_file(file_path)
            docstrings = get_python_docstrings(file_path)
            directory_map[file_path] = {"size": size, "is_image": is_image, "docstrings": docstrings}
    return directory_map

def is_image_file(file_path):
    """
    Check if the given file path represents an image file.

    Args:
        file_path (str): The path to the file.

    Returns:
        bool: True if the file is an image, False otherwise.
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower() in image_extensions


def get_python_docstrings(file_path):
    """
    Get a list of docstrings from a Python file.

    Args:
        file_path (str): The path to the Python file.

    Returns:
        list: The list of docstrings found in the file.
    """
    docstrings = []
    with open(file_path, "r", encoding="utf-8") as file:
      try:
        code = compile(file.read(), file_path, "exec")
        module = type(os)("__main__")
        exec(code, module.__dict__)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) or inspect.isfunction(obj):
                docstring = inspect.getdoc(obj)
                inspect(docustring)
                if docstring:
                    docstrings.append(docstring)
      except:
        print(docstrings)
    return docstrings
def load_openai_key():
    """
    Loads the OpenAI API key for authentication.
    """
    openai.api_key = get_openai_key()

def get_env(path='/home/hmmm/envy_all.env', st='OPENAI_API_KEY'):
    """
    Retrieves the value of the specified environment variable.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable. Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The value of the environment variable.
    """
    load_dotenv(path)
    return os.getenv(st)

def get_openai_key(path='/home/hmmm/envy_all.env', st='OPENAI_API_KEY'):
    """
    Retrieves the OpenAI API key from the environment variables.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable containing the API key. Defaults to 'OPENAI_API_KEY'.

    Returns:
        str: The OpenAI API key.
    """
    key = get_env(path=path, st=st)
    openai.api_key = key

def getPass(path='/home/hmmm/envy_all.env', st='MY_PASSWORD'):
    """
    Retrieves the value of the specified environment variable.

    Args:
        path (str): The path to the environment file. Defaults to '/home/hmmm/envy_all.env'.
        st (str): The name of the environment variable. Defaults to 'MY_PASSWORD'.

    Returns:
        str: The value of the environment variable.
    """
    return get_env(path=path, st=st)
def getAPIkey():
    return get_openai_key()

def headers():
    return {'Content-Type': 'application/json', 'Authorization': f'Bearer {getAPIkey()}'}

# Example function for sending text for OpenAI review
def send_for_review(prompt):
    api_endpoint = 'https://api.openai.com/v1/engines/davinci-codex/completions'
    data = {
        'prompt': prompt,
        'max_tokens': 100,
    }
    response = requests.post(api_endpoint, json=data, headers=headers())
    return response.json()

# Example usage
prompt = "This is the text to be reviewed. Please review it thoroughly."
review_response = send_for_review(prompt)
print(review_response)
def create_startup_file(path: str, requires: str = None, readme: str = None, short_description: str = None,email: str = None, author: str = None, entity: str = None):
    module_name = path.split('/')[-1]
    keys = ['requires', 'readme', 'short_description', 'email', 'author', 'entity']
    values = [requires, readme, short_description, email, author, entity]
    if str(requires) == 'set()':
      requires = ''
    data = {key: value for key, value in zip(keys, values)}
    
    input(data)

    return f"""from setuptools import setup, find_packages

    setup(name='{module_name}',
      version='0.0.1',
      author='{author}',
      author_email='{email}',
      description='{module_name} is a collection of utility modules providing a variety of functions.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      url='https://github.com/{entity}/{module_name}',
      packages=find_packages(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.11',
      ],
      python_requires='>=3.11',
      install_requires=
      {list(requires)}
      ,
      entry_points={{
          'console_scripts': [
              '{module_name}={module_name}.main:main',
          ],
      }}
    )
     """
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
    # You can import and use other modules or functions of abstract_utilities here.
    script_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(script_path)

    filtered_modules = get_filtered_files(directory_path)

if __name__ == "__main__":
    # Get the absolute directory path of the current script file
    main()"""
# Example usage
def get_stringers(content,k,ls):
  if not content[k] in ls:
      if content[-3:] in ['"""',"'''"]:
        for c in range(0,len(['"""',"'''"])):
          if ls[-3:] == ['"""',"'''"][c]:
            piece = ['"""',"'''"][c]
        ls.append(content[k:].split(piece)[0])
        return ls
  return ''
def eat_right(obj,content):
  while content[-1] != obj:
    content = content[:-1]
  return content[1:]
def if_commented(content):
  ls = ['',' ','\t','\n','"',"'"]
  for k in range(0,len(content)):
    
    lsN[content[:-len(eat_right(':',content).split('(')[-1][:-1])+2]]={'inputs':eat_right(':',content).split('(')[-1][:-1],'docstring':get_stringers(content,k,ls)}
path = get_browser()
lis = os.listdir(path)
for k in range(0,len(lis)):
    
  if lis[k].split('.')[-1]=='py':
     content = read_from_file(os.path.join(path,lis[k]))
     content = content.split('def')
     for c in range(0,len(content)):
       content[c]
                              
input(get_python_docstrings())
path = get_browser()
requires = find_third_party_imports(os.path.join(path,path.split('/')[-1]))
readme = os.path.join(path,'README.md')
short_description = """The "abstract_security" module is a powerful collection of utility modules designed to enhance your Python projects with advanced security functionalities. It provides a wide range of functions to aid in tasks such as data comparison, list manipulation, JSON handling, string manipulation, mathematical computations, and time operations. Developed by putkoff and released under the MIT License, this module is currently in its alpha development stage. It is intended for developers who prioritize security in their applications and require a reliable and efficient solution. For detailed information on how to install and utilize this module, please refer to the documentation."""
email = "partners@abstractendeavors.com"
author = "putkoff"
entity = "abstract_endeavors"
write_to_file(contents=create_directory_map(path),filepath=os.path.join(path,'directory_map.txt'))
write_to_file(contents=gather_header_docs(os.path.join(path,path.split('/')[-1])),filepath=os.path.join(path,'docusigns.txt'))
startup_file_content = create_startup_file(path, requires, readme, short_description, email, author, entity)
write_to_file(contents=startup_file_content,filepath=os.path.join(path,'startup.py'))
write_to_file(contents='',filepath=os.path.join(path,'__init__.py'))
write_to_file(contents=create_main(path.split('/')[-1]),filepath=os.path.join(os.path.join(path,path.split('/')[-1]),'main.py'))
write_to_file(contents='',filepath=os.path.join(os.path.join(path,path.split('/')[-1]),'__init__.py'))
