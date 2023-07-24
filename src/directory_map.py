import os
import shutil
from abstract_utilities.read_write_utils import read_or_write

def create_directory_map(folder_path):
    directory_map = {}
    replica_folder_path = folder_path + "_replica"
    # Remove the replica folder if it exists, and create a new one
    if os.path.exists(replica_folder_path):
        shutil.rmtree(replica_folder_path)
    shutil.copytree(folder_path, replica_folder_path, ignore=shutil.ignore_patterns('*.*')) # Copy the folder structure only, excluding all files
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            replica_file_path = file_path.replace(folder_path, replica_folder_path)
            size = os.path.getsize(file_path)
            tokens = 0
            content = read_or_write(path=file_path)
            if content != None:
                tokens = tokenize(content)
            # Create a blank file in the replica folder
            if not imgTF(file_path):
                with open(replica_file_path, "w", encoding="utf-8") as f:
                    pass
            directory_map[file_path] = {"size": size, "tokens": tokens, 'image': imgTF(file_path)}
    print(json.dumps(directory_map, indent=2))
    return directory_map
