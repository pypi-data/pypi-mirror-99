# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

import hashlib
import datetime
import re
from shutil import copy2

from pathlib import Path

from tsfpga.git_utils import git_commands_are_available, get_git_commit
from tsfpga.svn_utils import svn_commands_are_available, get_svn_revision_information
from tsfpga.system_utils import create_directory, create_file, read_file
from . import __version__
from .constant import Constant
from .register import Register
from .register_array import RegisterArray
from .register_c_generator import RegisterCGenerator
from .register_cpp_generator import RegisterCppGenerator
from .register_html_generator import RegisterHtmlGenerator
from .register_vhdl_generator import RegisterVhdlGenerator


class RegisterList:

    """
    Used to handle the registers of a module. Also known as a register map.
    """

    def __init__(self, name, source_definition_file):
        """
        Arguments:
            name (str): The name of this register list. Typically the name of the module that uses
                it.
            source_definition_file (`pathlib.Path`): The TOML source file that defined this
                register list.
        """
        self.name = name
        self.source_definition_file = source_definition_file

        self.register_objects = []
        self.constants = []

    def append_register(self, name, mode, description=None, default_value=None):
        """
        Append a register to this list.

        Arguments:
            name (str): The name of the register.
            mode (str): A valid register mode.
            description (str): Textual register description.
            default_value (int): Default value for the register (signed).
        Return:
            :class:`.Register`: The register object that was created.
        """
        if self.register_objects:
            index = self.register_objects[-1].index + 1
        else:
            index = 0

        register = Register(name, index, mode, description, default_value)
        self.register_objects.append(register)

        return register

    def append_register_array(self, name, length):
        """
        Append a register array to this list.

        Arguments:
            name (str): The name of the register array.
            length (int): The number of times the register sequence shall be repeated.
        Return:
            :class:`.RegisterArray`: The register array object that was created.
        """
        if self.register_objects:
            base_index = self.register_objects[-1].index + 1
        else:
            base_index = 0
        register_array = RegisterArray(name, base_index, length)

        self.register_objects.append(register_array)
        return register_array

    def get_register(self, name):
        """
        Get a register from this list. Will only find single registers, not registers in a
        register array.

        Arguments:
            name (str): The name of the register.
        Return:
            :class:`.Register`: The register. ``None`` if no register matched.
        """
        for register_object in self.register_objects:
            if register_object.name == name:
                return register_object

        return None

    def add_constant(self, name, value, description=None):
        """
        Add a constant. Will be available in the generated packages and headers.

        Arguments:
            name (str): The name of the constant.
            length (int): The constant value (signed).
            description (str): Textual description for the constant.
        Return:
            :class:`.Constant`: The constant object that was created.
        """
        constant = Constant(name, value, description)
        self.constants.append(constant)
        return constant

    def get_constant(self, name):
        """
        Get a constant from this list.

        Arguments:
            name (str): The name of the constant.
        Return:
            :class:`.Constant`: The constant. ``None`` if no constant matched.
        """
        for constant in self.constants:
            if constant.name == name:
                return constant

        return None

    def create_vhdl_package(self, output_path):
        """
        Create a VHDL package file with register and field definitions.

        This function assumes that the ``output_path`` folder already exists. This assumption makes
        it slightly faster than the other functions that use ``create_file()``. Necessary since this
        one is often used in real time (before simulations, etc..) and not in one-off scenarios
        like the others (when making a release).

        In order to save time, there is a mechanism to only generate the VHDL file when necessary.
        A hash of this register list object will be written to the file along with all the register
        definitions. This hash will be inspected and compared, and the VHDL file will only be
        generated again if something has changed.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        vhd_file = output_path / (self.name + "_regs_pkg.vhd")

        self_hash = self._hash()
        if self._should_create_vhdl_package(vhd_file, self_hash):
            self._create_vhdl_package(vhd_file, self_hash)

    def _should_create_vhdl_package(self, vhd_file, self_hash):
        if not vhd_file.exists():
            return True
        if (self_hash, __version__) != self._find_hash_and_version_of_existing_vhdl_package(
            vhd_file
        ):
            return True
        return False

    @staticmethod
    def _find_hash_and_version_of_existing_vhdl_package(vhd_file):
        """
        Returns `None` if nothing found, otherwise the matching strings in a tuple.
        """
        regexp = re.compile(
            r"\n-- Register hash ([0-9a-f]+), generator version (\d+\.\d+\.\d+)\.\n"
        )
        existing_file_content = read_file(vhd_file)
        match = regexp.search(existing_file_content)
        if match is None:
            return None
        return match.group(1), match.group(2)

    def _create_vhdl_package(self, vhd_file, self_hash):
        print(f"Creating VHDL register package {vhd_file}")
        # Add a header line with the hash
        generated_info = self._generated_source_info() + [
            f"Register hash {self_hash}, generator version {__version__}."
        ]
        register_vhdl_generator = RegisterVhdlGenerator(self.name, generated_info)
        with vhd_file.open("w") as file_handle:
            file_handle.write(
                register_vhdl_generator.get_package(self.register_objects, self.constants)
            )

    def create_c_header(self, output_path):
        """
        Create a C header file with register and field definitions.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / (self.name + "_regs.h")
        register_c_generator = RegisterCGenerator(self.name, self._generated_source_info())
        create_file(
            output_file, register_c_generator.get_header(self.register_objects, self.constants)
        )

    def create_cpp_interface(self, output_path):
        """
        Create a C++ class interface header file, with register and field definitions. The
        interface header contains only virtual methods.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / ("i_" + self.name + ".h")
        register_cpp_generator = RegisterCppGenerator(self.name, self._generated_source_info())
        create_file(
            output_file, register_cpp_generator.get_interface(self.register_objects, self.constants)
        )

    def create_cpp_header(self, output_path):
        """
        Create a C++ class header file.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / (self.name + ".h")
        register_cpp_generator = RegisterCppGenerator(self.name, self._generated_source_info())
        create_file(output_file, register_cpp_generator.get_header(self.register_objects))

    def create_cpp_implementation(self, output_path):
        """
        Create a C++ class implementation file.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / (self.name + ".cpp")
        register_cpp_generator = RegisterCppGenerator(self.name, self._generated_source_info())
        create_file(output_file, register_cpp_generator.get_implementation(self.register_objects))

    def create_html_page(self, output_path):
        """
        Create a documentation HTML page with register and field information. Will include the
        tables created by :meth:`.create_html_register_table` and
        :meth:`.create_html_constant_table`.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        register_html_generator = RegisterHtmlGenerator(self.name, self._generated_source_info())

        output_file = output_path / (self.name + "_regs.html")
        create_file(
            output_file, register_html_generator.get_page(self.register_objects, self.constants)
        )

        output_file = output_path / "regs_style.css"
        if not output_file.exists():
            # Create the file only once. This mechanism could be made more smart, but at the moment
            # there is no use case. Perhaps there should be a separate stylesheet for each
            # HTML file?
            create_file(output_file, register_html_generator.get_page_style())

    def create_html_register_table(self, output_path):
        """
        Create documentation HTML table with register and field information.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / (self.name + "_register_table.html")
        register_html_generator = RegisterHtmlGenerator(self.name, self._generated_source_info())
        create_file(output_file, register_html_generator.get_register_table(self.register_objects))

    def create_html_constant_table(self, output_path):
        """
        Create documentation HTML table with constant information.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        output_file = output_path / (self.name + "_constant_table.html")
        register_html_generator = RegisterHtmlGenerator(self.name, self._generated_source_info())
        create_file(output_file, register_html_generator.get_constant_table(self.constants))

    def copy_source_definition(self, output_path):
        """
        Copy the TOML file that created this register list.

        Arguments:
            output_path (`pathlib.Path`): Result will be placed here.
        """
        create_directory(output_path, empty=False)
        copy2(self.source_definition_file, output_path)

    @staticmethod
    def _generated_info():
        """
        Return:
            list(str): Line(s) informing the user that a file is automatically generated.
        """
        return ["This file is automatically generated by tsfpga."]

    def _generated_source_info(self):
        """
        Return:
            list(str): Line(s) informing the user that a file is automatically generated, containing
            info about the source of the generated register information.
        """
        time_info = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        commit_info = ""
        if git_commands_are_available(directory=Path(".")):
            commit_info = f" at commit {get_git_commit(directory=Path('.'))}"
        elif svn_commands_are_available():
            commit_info = f" at revision {get_svn_revision_information()}"

        info = f"Generated {time_info} from file {self.source_definition_file.name}{commit_info}."

        return self._generated_info() + [info]

    def _hash(self):
        """
        Get a hash of this object representation. SHA1 is the fastest method according to e.g.
        http://atodorov.org/blog/2013/02/05/performance-test-md5-sha1-sha256-sha512/
        Result is a lowercase hexadecimal string.
        """
        return hashlib.sha1(repr(self).encode()).hexdigest()

    def __repr__(self):
        return f"""{self.__class__.__name__}(\
name={self.name},\
source_definition_file={repr(self.source_definition_file)},\
register_objects={','.join([repr(register_object) for register_object in self.register_objects])},\
constants={','.join([repr(constant) for constant in self.constants])},\
)"""
