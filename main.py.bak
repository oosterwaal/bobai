import os
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
from google.genai import types

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt provided. Usage: python main.py <prompt>")
        sys.exit(1)
    user_prompt = sys.argv[1]
    verbose = False
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
        verbose = True
    from functions.get_files_info import schema_get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python import run_python_file
    from functions.write_file import write_file
    client = genai.Client(api_key=api_key)
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads the contents of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to read, relative to the working directory.",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The Python file to execute, relative to the working directory.",
                ),
                "args": types.Schema(
                    type=types.Type.ARRAY,
                    items=types.Schema(type=types.Type.STRING),
                    description="Optional arguments to pass to the Python file.",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites a file with the provided content, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]
    from functions.get_files_info import call_function
    max_iterations = 20
    for i in range(max_iterations):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )
            if verbose:
                print(f"Iteration {i+1}")
                print(f"Prompt tokens: {getattr(response.usage_metadata, 'prompt_token_count', None)}")
                print(f"Response tokens: {getattr(response.usage_metadata, 'candidates_token_count', None)}")
            if hasattr(response, "candidates") and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, "content"):
                        messages.append(candidate.content)
            if hasattr(response, "function_calls") and response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose=verbose)
                    messages.append(
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_function_response(
                                    name=function_call_part.name,
                                    response=function_call_result.parts[0].function_response.response
                                )
                            ]
                        )
                    )
                    if verbose and hasattr(function_call_result.parts[0], "function_response") and hasattr(function_call_result.parts[0].function_response, "response"):
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            elif hasattr(response, "text") and response.text:
                print(response.text)
                break
        except Exception as e:
            print(f"Error during iteration {i+1}: {e}")
            break
if __name__ == "__main__":
    main()
