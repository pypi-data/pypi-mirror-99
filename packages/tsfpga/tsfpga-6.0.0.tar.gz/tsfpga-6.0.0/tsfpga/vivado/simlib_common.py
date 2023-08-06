# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

from pathlib import Path
import platform
from shutil import which, make_archive
import zipfile

from tsfpga.system_utils import create_file, delete


class VivadoSimlibCommon:

    """
    Class for handling Vivado simlib used for simulation. Keeps track of when a
    (re)compile is needed.
    """

    _libraries = None
    _vivado_path = None
    _output_path = None

    def compile_if_needed(self):
        """
        Compile if needed (if :meth:`compile_is_needed <.compile_is_needed>` condition is not
        fulfilled).
        """
        if self.compile_is_needed:
            self.compile()
            return True
        return False

    @property
    def compile_is_needed(self):
        """
        If there is compiled simlib available that matches

         * Operating system
         * Vivado version
         * Simulator version

        then there should not be a recompile.

        .. note::
            Child implementations might add further conditions.

        Return:
            True if compiled simlib is not available. False otherwise.
        """
        if self._done_token.exists():
            return False
        return True

    def compile(self):
        """
        Compile simlib.
        """
        delete(self._done_token)
        print(f"Compiling Vivado simlib in {self._output_path}")

        self._compile()

        create_file(self._done_token, "Done!")

    def _compile(self):
        """
        Compile simlib.
        """
        raise NotImplementedError()

    def add_to_vunit_project(self):
        """
        Add the compiled simlib to your VUnit project.
        """
        self._add_to_vunit_project()

    def _add_to_vunit_project(self):
        raise NotImplementedError()

    @property
    def artifact_name(self):
        """
        str: The name of the folder where simlib is or will be compiled.
        Follows a format ``vivado-simlib-WW.XX.YY.ZZ`` suitable for storage and versioning
        in Artifactory.
        """
        return self._output_path.name

    def to_archive(self):
        """
        Compress compiled simlib to an archive.

        Return:
            `pathlib.Path`: Path to the archive.
        """
        make_archive(self._output_path, "zip", self._output_path)
        archive = self._output_path.parent / (self._output_path.name + ".zip")
        return archive

    def from_archive(self, archive):
        """
        Unpack compiled simlib from an existing archive.

        Arguments:
            archive (`pathlib.Path`): Path to a zip archive with previously compiled simlib.
        """
        with zipfile.ZipFile(archive, "r") as zip_handle:
            zip_handle.extractall(self._output_path)

    def _get_version_tag(self):
        tag = "vivado-simlib-"
        tag += self._get_operating_system_tag()
        tag += "." + self._get_vivado_version_tag()
        tag += "." + self._get_simulator_tag()
        return tag

    def _get_operating_system_tag(self):
        """
        Return e.g. "linux".
        """
        return self._format_version(platform.system())

    def _get_vivado_version_tag(self):
        """
        Return e.g. "vivado_2019_2".
        """
        vivado_path = self._vivado_path
        if vivado_path == "vivado":
            vivado_path = which(vivado_path)
            assert vivado_path is not None, "Could not find vivado location"
        vivado_version = Path(vivado_path).parent.parent.name
        return self._format_version("vivado_" + vivado_version)

    def _get_simulator_tag(self):
        raise NotImplementedError()

    @staticmethod
    def _format_version(version):
        """
        Format version string to something suitable fort artifactory versioning.
        """
        return version.replace(".", "_").replace("-", "_").lower()

    @property
    def _done_token(self):
        """
        Path to "done" token file.
        """
        return self._output_path / "done.txt"
