import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API_KEY is NONE")

client = genai.Client(api_key = api_key)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    print(f" - Calling function: {function_call_part.name}")
    
    functions = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if functions[function_call_part.name]:
        fn = functions[function_call_part.name]
        args = dict(function_call_part.args)
        args["working_directory"] = "./calculator"
        fn_result = {}
        fn_result["result"] = fn(**args)
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": fn_result},
                )
            ],
        )
    
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    

        

def main():
    available_functions = types.Tool(function_declarations=[schema_get_files_info,
            schema_get_file_content, schema_run_python_file, schema_write_file],)
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="This is your user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    
    model = "gemini-2.5-flash"
    contents = messages
    count = 0
    
    while count < 20:
        
        response_obj = client.models.generate_content(model=model, contents = contents,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
        
        for cand in response_obj.candidates:
            messages.append(cand)
        
        
        if not response_obj.function_calls:
            print("I PRINTED RESPONSE_OBJ.TEXT:")
            print(response_obj.text)
            break
        
        
        for call in response_obj.function_calls:
            
            #print(f"Calling function: {call.name}({call.args})")
            call_func_result = call_function(call)
            messages.append(call_func_result)
            
            if call_func_result.parts[0].function_response.response:
                
                if args.verbose:
                    print(f"-> {call_func_result.parts[0].function_response.response}")
            else:
                raise Exception("Something Went Wrong")
            
            
        count += 1
        
    

if __name__ == "__main__":
    main()
