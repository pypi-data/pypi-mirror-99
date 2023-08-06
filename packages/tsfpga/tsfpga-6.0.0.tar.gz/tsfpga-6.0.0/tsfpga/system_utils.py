# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

import importlib.util
import os
from platform import system
from shutil import rmtree
import subprocess


def create_file(file, contents=None):
    create_directory(file.parent, empty=False)

    contents = "" if contents is None else contents
    with file.open("w") as file_handle:
        file_handle.write(contents)

    return file


def read_file(file):
    with file.open() as file_handle:
        return file_handle.read()


def read_last_lines_of_file(file, num_lines):
    """
    Read a number of lines from the end of a file, without buffering the whole file.
    Similar to unix ``tail`` command.

    Arguments:
        file (`pathlib.Path`): The file that shall be read.
        num_lines (int): The number of lines to read.

    Return:
        str: The last lines of the file.
    """
    result_lines = []
    blocks_to_read = 0

    with open(file) as file_handle:
        while len(result_lines) < num_lines:
            # Since we do not know the line lengths, there is some guessing involved. Keep reading
            # larger and larger blocks until we have all the lines that are requested.
            blocks_to_read += 1

            try:
                # Read a block from the end
                file_handle.seek(-blocks_to_read * 4096, os.SEEK_END)
            except IOError:
                # Tried to read more data than what is available. Read whatever we have and return
                # to user.
                file_handle.seek(0)
                result_lines = file_handle.readlines()
                break

            result_lines = file_handle.readlines()

    result = "".join(result_lines[-num_lines:])
    return result


def delete(path):
    if path.exists():
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()
    return path


def create_directory(directory, empty=True):
    if empty:
        delete(directory)
    elif directory.exists():
        return directory

    directory.mkdir(parents=True)
    return directory


def run_command(cmd, cwd=None):
    if not isinstance(cmd, list):
        raise ValueError("Must be called with a list, not a string")

    subprocess.check_call(cmd, cwd=cwd)


def load_python_module(file):
    python_module_name = file.stem

    spec = importlib.util.spec_from_file_location(python_module_name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def system_is_windows():
    return system() == "Windows"
