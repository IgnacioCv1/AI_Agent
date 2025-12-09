import os
from google.genai import types

def write_file(working_directory, directory, content):
  full_path = os.path.join(working_directory, directory)
  
  if not (full_path == working_directory or full_path.startswith(working_directory)):
    return f'Error: Cannot write to "{full_path}" as it is outside the permitted working directory'

  folder_path = os.path.dirname(full_path)
  if folder_path and not os.path.exists(folder_path):
    os.makedirs(folder_path)
  try:
      
    with open(full_path, 'w') as f:
      f.write(content)
      return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
  
  except PermissionError:
    return f'Error: Permission denied when writing "{full_path}"'
  
  except Exception as e:
    return f"Error: {e}"
  
  
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Create or overwrite a file in file path relative to working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory where we want to create or overwrite a file, relative to the working directory. If file path not provided create or overwrite files in the working directory itself",
            ),
            "content": types.Schema(
              type=types.Type.STRING,
              description="The content to be written into the newly created file over overwrite the existing one."
            ),
        },
    ),
)