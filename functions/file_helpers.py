import os
import subprocess
from google.genai import types

max_chars = 10000


def get_files_info(working_directory, directory=None):
    abs_working = os.path.abspath(working_directory)
    target_dir = abs_working
    if directory:
        target_dir = os.path.abspath(os.path.join(abs_working, directory))
    if not target_dir.startswith(abs_working):
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
    if not os.path.isdir(target_dir):
        return f"Error: '{directory}' is not a directory"

    try:
        info = []
        for item in os.listdir(target_dir):
            ipath = os.path.join(target_dir, item)
            fsize = os.path.getsize(ipath)
            is_dir = os.path.isdir(ipath)
            info.append(f"- {item}: file_size={fsize} bytes, is_dir={is_dir}")

        return "\n".join(info)
    except Exception as e:
        return f"Error listing files: {e}"


def get_file_content(working_directory, file_path):
    abs_working = os.path.abspath(working_directory)
    target_file = abs_working
    if file_path:
        target_file = os.path.abspath(os.path.join(abs_working, file_path))
    if not target_file.startswith(abs_working):
        return f"Error: Cannot read '{file_path}' as it is outside the permitted working directory"
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_file, "r") as f:
            file_content = f.read(max_chars)
            if os.path.getsize(target_file) > max_chars:
                file_content += (
                    f"[...File '{file_path}' truncated at {max_chars} characters]"
                )
        return file_content
    except Exception as e:
        return f"Error reading files: {e}"


def write_file(working_directory, file_path, content):
    abs_working = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(abs_working, file_path))
    if not target_file.startswith(abs_working):
        return f"Error: Cannot write to '{file_path}' as it is outside the permitted working directory"

    if not os.path.exists(target_file):
        try:
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
        )
    except Exception as e:
        return f"Error: writine to file: {e}"


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


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Returns the contents of the file, contrained to max {max_chars} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to the given file_path",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING, description="The content to write to the file"
            ),
        },
        required=["file_path", "content"],
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the python file at the given file_path with optional agruments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
