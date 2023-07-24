import os
import re
import importlib
from folderbrowser import get_browser

def find_third_party_imports(start_path:str=None):
    if start_path == None:
        start_path = get_browser()
    python_files = [f for f in os.listdir(start_path) if f.endswith('.py')]
    third_party_imports = set()

    for file in python_files:
        with open(os.path.join(start_path, file), 'r') as f:
            lines = f.readlines()
            for line in lines:
                import_match = re.match(r'^import (\S+)', line)  # Match "import <module>"
                from_import_match = re.match(r'^from (\S+)', line)  # Match "from <module>"
                if import_match:
                    module = import_match.group(1)
                    if is_third_party(module):
                        third_party_imports.add(module)
                if from_import_match:
                    module = from_import_match.group(1)
                    if is_third_party(module):
                        third_party_imports.add(module)

    return third_party_imports

def is_third_party(module):
    try:
        spec = importlib.util.find_spec(module)
        return spec is not None and 'site-packages' in spec.origin
    except Exception:
        return False

