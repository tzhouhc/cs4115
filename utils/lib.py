import os


def is_executable_file(file_path):
    """Check if a file is executable."""
    if os.path.isfile(file_path):
        # Check for executable permission; use `os.access` for portability
        return os.access(file_path, os.X_OK)
    return False


def find_binaries_on_path():
    """Find all binaries available on the PATH."""
    # Retrieve and split the PATH environment variable
    path_env_var = os.environ.get('PATH', '')
    path_dirs = path_env_var.split(os.pathsep)

    # To store the collected binaries
    binaries = set()

    # Iterate through each directory in the PATH
    for directory in path_dirs:
        try:
            # List all entries in the directory
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_file() and is_executable_file(entry.path):
                        # Add the executable file's name to the set
                        binaries.add(entry.name)
        except (FileNotFoundError, PermissionError):
            # Path might contain non-existing directories
            # Ignore them and continue
            continue

    return binaries


# Get the list of binary names
PATH_BINS: set[str] = find_binaries_on_path()
