# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

from pathlib import Path

from tsfpga.hdl_file import HdlFile


def test_file_type():
    assert HdlFile(Path("file.vhd")).is_vhdl
    assert not HdlFile(Path("file.vhd")).is_verilog_source
    assert not HdlFile(Path("file.vhd")).is_verilog_header

    assert HdlFile(Path("file.vh")).is_verilog_header
    assert HdlFile(Path("file.v")).is_verilog_source


def test_can_cast_to_string_without_error():
    str(HdlFile(Path("file.vhd")))
