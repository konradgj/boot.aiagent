import os


def get_files_info(working_directory, directory=None):
    if directory not in os.listdir(working_directory) and directory != ".":
        return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"

    path = os.path.join(working_directory, directory)
    if not os.path.isdir(path):
        return f"Error: '{directory}' is not a directory"

    info = []
    for item in os.listdir(path):
        ipath = os.path.join(path, item)
        fsize = os.path.getsize(ipath)
        is_dir = os.path.isdir(ipath)
        info.append(f"- {item}: file_size={fsize} bytes, is_dir={is_dir}")

    return "\n".join(info)


info = get_files_info("calculator", "pkg")
print(info)
