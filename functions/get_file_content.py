import os
from functions.config import MAX_FILE_LENGTH

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # Guardrail: must stay within working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        if len(content) > MAX_FILE_LENGTH:
            content = content[:MAX_FILE_LENGTH] + f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'

