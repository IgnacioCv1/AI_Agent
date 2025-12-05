import os

def write_file(working_directory, directory, content):
  full_path = os.path.join(working_directory, directory)
  
  if not (full_path == working_directory or full_path.startswith(working_directory)):
    return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'

  if not os.path.exists(full_path):
    os.makedirs(directory)
  try:
      
    with open(full_path, 'w') as f:
      f.write(content)
      return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
  
  except PermissionError:
    return f'Error: Permission denied when writing "{full_path}"'
  
  except Exception as e:
    return f"Error: {e}"