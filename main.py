import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("API_KEY is NONE")

client = genai.Client(api_key = api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="This is your user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enables verbose output")
    args = parser.parse_args()
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    
    model = "gemini-2.5-flash"
    contents = messages
    response_obj = client.models.generate_content(model=model, contents = contents)
    if args.verbose == True:
        print(f"User prompt: {contents}\nPrompt tokens: {response_obj.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response_obj.usage_metadata.candidates_token_count}\nResponse:")
    print(f"{response_obj.text}")

if __name__ == "__main__":
    main()
