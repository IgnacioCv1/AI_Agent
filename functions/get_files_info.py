import os

def get_files_info(working_directory, directory="."):
  full_path = os.path.join(working_directory, directory)
  full_path = os.path.realpath(full_path)
  working_directory = os.path.realpath(working_directory)
  
  #print(f"DEBUG: working_directory={os.path.realpath(working_directory)}")
  #print(f"DEBUG: full_path={os.path.realpath(os.path.join(working_directory, directory))}")
  
  if not (full_path == working_directory or full_path.startswith(working_directory + os.sep)):
    return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
  
  if not os.path.isdir(full_path):
    return f'Error: "{directory}" is not a directory'
  
  inside_full_path = os.listdir(full_path)
  return_string = ""
  
  for item in inside_full_path:
    if item == "__pycache__" or item.startswith("."):
                continue
              
    item_path = os.path.join(full_path, item)
    return_string += f'- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n'
  
  return return_string