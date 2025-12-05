import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
  
    
  full_path = os.path.join(working_directory, file_path)
  
  if not (full_path == working_directory or full_path.startswith(working_directory + os.sep)):
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
  
  if not os.path.isfile(full_path):
    return f'Error: File not found or is not a regular file: "{file_path}"'
  
  try:
      
    with open(full_path, 'r') as f:
      file_content = f.read(MAX_CHARS)
      remainder = f.read(1)
      if remainder:
        file_content += f'[...File "{full_path}" truncated at 10000 characters]'
      return file_content
    
  except FileNotFoundError:
    return f'Error: File not found or is not a regular file: "{file_path}"'
  except PermissionError:
    return f'Error: Permission denied when reading "{file_path}"'
  except IsADirectoryError:
    return f'Error: File not found or is not a regular file: "{file_path}"'
  except Exception as e:
    return f"Error: {e}"