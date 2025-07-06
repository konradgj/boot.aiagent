import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    abs_working = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working, file_path))
    if not target_file.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f"Error: '{file_path}' is not a Python file."
    try:
        commands = ["python", target_file]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = []
    output.append(f"STDOUT: {result.stdout}")
    output.append(f"STRERR: {result.stderr}")
    if result.returncode != 0:
        output.append(f"Process exited with code {result.returncode}")
    return "\n".join(output) if output else "No output produced."
