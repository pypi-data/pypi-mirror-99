# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

import pytest

import tsfpga
from tsfpga.git_utils import find_git_files
from tsfpga.system_utils import create_file


def open_file_with_encoding(file):
    print(file)
    with file.open(encoding="ascii") as file_handle:
        file_handle.read()


def test_all_checked_in_files_are_properly_encoded():
    """
    To avoid problems with different editors and different file encodings, all checked in files
    should contain only ASCII characters.

    Avoid one of the documentation files that uses wonky characters to illustrate a directory tree.
    """
    for file in files_to_test(
        exclude_directories=[tsfpga.TSFPGA_DOC / "sphinx" / "module_structure.rst"]
    ):
        open_file_with_encoding(file)


def check_file_ends_with_newline(file):
    test_ok = True
    with file.open() as file_handle:
        file_data = file_handle.read()
        if len(file_data) != 0:
            if file_data[-1] != "\n":
                print(f"File {file} didn't end with newline")
                test_ok = False
    return test_ok


def test_all_checked_in_files_end_with_newline():
    """
    All checked in non-empty files should end with a UNIX style line break (\n).
    Otherwise UNIX doesn't consider them actual text files.
    """
    test_ok = True
    for file in files_to_test():
        test_ok &= check_file_ends_with_newline(file)
    assert test_ok


def check_file_for_tab_character(file):
    test_ok = True
    with file.open() as file_handle:
        for idx, line in enumerate(file_handle.readlines()):
            if "\t" in line:
                test_ok = False
                print(f"TAB charatcher (\\t) on line {idx + 1} in {file}")
    return test_ok


def test_no_checked_in_files_contain_tabs():
    """
    To avoid problems with files looking different in different editors, no checked in files may
    contain TAB characters.
    """
    test_ok = True
    for file in files_to_test():
        test_ok &= check_file_for_tab_character(file)
    assert test_ok


def check_file_for_carriage_return(file):
    test_ok = True
    with file.open(newline="") as file_handle:
        if "\r" in file_handle.read():
            test_ok = False
            print(f"Windows style line breaks (\\r\\n aka CR/LF) in {file}")
    return test_ok


def test_no_checked_in_files_contain_carriage_return():
    """
    All checked in files should use UNIX style line breaks (\n not \r\n).
    Some Linux editors and tools will display or interpret the \r as something other than a line
    break.
    """
    test_ok = True
    for file in files_to_test():
        test_ok &= check_file_for_carriage_return(file)
    assert test_ok


def check_file_for_trailing_whitespace(file):
    test_ok = True
    with file.open() as file_handle:
        for idx, line in enumerate(file_handle.readlines()):
            if " \n" in line:
                test_ok = False
                print(f"Trailing whitespace on line {idx + 1} in {file}")
    return test_ok


def test_no_checked_in_files_contain_trailing_whitespace():
    """
    Trailing whitespace is not allowed. Some motivation here:
    https://softwareengineering.stackexchange.com/questions/121555/
    """
    test_ok = True
    for file in files_to_test():
        test_ok &= check_file_for_trailing_whitespace(file)
    assert test_ok


def files_to_test(exclude_directories=None):
    # Do not test binary image files
    return find_git_files(
        directory=tsfpga.REPO_ROOT,
        exclude_directories=exclude_directories,
        file_endings_avoid="png",
    )


def test_open_file_with_encoding_should_raise_exception_on_bad_file(tmp_path):
    """
    Sanity check that the function we use actually triggers on bad files.
    """
    file = tmp_path / "temp_file_for_test.txt"
    with file.open("w", encoding="utf-8") as file_handle:
        # Swedish word for island = non-ASCII character
        data = "\N{LATIN CAPITAL LETTER O WITH DIAERESIS}"
        file_handle.write(data)

    with pytest.raises(UnicodeDecodeError):
        open_file_with_encoding(file)


def test_check_file_for_tab_character_should_fail_on_bad_file(tmp_path):
    """
    Sanity check that the function we use actually triggers on bad files.
    """
    data = "Apa\thest"
    file = create_file(tmp_path / "temp_file_for_test.txt", data)
    assert not check_file_for_tab_character(file)


def test_check_file_for_carriage_return_should_fail_on_bad_file(tmp_path):
    """
    Sanity check that the function we use actually triggers on bad files.
    """
    file = tmp_path / "temp_file_for_test.txt"
    data = b"Apa\r\nhest"
    with file.open("wb") as file_handle:
        file_handle.write(data)
    assert not check_file_for_carriage_return(file)


def test_check_file_for_trailing_whitespace(tmp_path):
    """
    Sanity check that the function we use actually triggers on bad files.
    """
    data = "Apa \nhest    \nzebra"
    file = create_file(tmp_path / "temp_file_for_test.txt", data)
    assert not check_file_for_trailing_whitespace(file)
