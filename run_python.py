import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        # Guardrail: must stay within working_directory
        if not abs_file_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        try:
            completed_process = subprocess.run(
                ["python", abs_file_path] + args,
                cwd=abs_working_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = []
            if completed_process.stdout:
                output.append(f'STDOUT:\n{completed_process.stdout}')
            if completed_process.stderr:
                output.append(f'STDERR:\n{completed_process.stderr}')
            if completed_process.returncode != 0:
                output.append(f'Process exited with code {completed_process.returncode}')
            if not output:
                return "No output produced."
            return '\n'.join(output)
        except Exception as e:
            return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"

