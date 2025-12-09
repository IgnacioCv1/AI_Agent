import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
  full_path = os.path.realpath(os.path.join(working_directory, file_path))
  working_directory = os.path.realpath(working_directory)
  
  if not(full_path == working_directory or full_path.startswith(working_directory + os.sep)):
    return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
  
  if not(os.path.exists(full_path)):
    return f'Error: File "{file_path}" not found.'
  
  if not full_path.endswith(".py"):
    return f'Error: "{file_path}" is not a Python file.'
  
  try:
    result = subprocess.run(["python3", full_path] + args, capture_output=True, text=True, timeout=30)
    stdout = result.stdout
    stderr = result.stderr 
    if result.returncode != 0:
      return f"Process exited with code {result.returncode}"
    
    if stdout == "" and stderr == "":
      return f"No output produced"
    
    return f"STDOUT: {stdout} STDERR: {stderr}"
  except Exception as e:
    return f"Error: executing Python file: {e}"
  
  
  


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="executes a python script constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to the python script, relative to the working directory. If not provided, files in the working directory itself.",
            ),
            "args": types.Schema(
              type=types.Type.ARRAY,
              items=types.Schema(type=types.Type.STRING),
              description=(
                "List of command-line arguments to pass to the Python file. "
                "Each element must be a string."
              )
            ),
        },
    ),
)