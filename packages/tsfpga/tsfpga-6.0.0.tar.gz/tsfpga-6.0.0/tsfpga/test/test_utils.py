# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

from tsfpga.system_utils import read_file


def file_contains_string(file, string):
    return string in read_file(file)


def file_equals(file, string):
    return string == read_file(file)
