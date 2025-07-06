import os
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
            "write_file": types.Schema(
                type=types.Type.STRING, description="The content to write to the file"
            ),
        },
    ),
)
