# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

from tsfpga.module import BaseModule
from tsfpga.vivado.project import VivadoNetlistProject
from tsfpga.vivado.size_checker import EqualTo, Ffs, Ramb18, Ramb36, TotalLuts
from examples.tsfpga_example_env import get_tsfpga_modules


class Module(BaseModule):
    def setup_vunit(self, vunit_proj, **kwargs):
        for test in (
            vunit_proj.library(self.library_name).test_bench("tb_asynchronous_fifo").get_tests()
        ):
            for read_clock_is_faster in [True, False]:
                original_generics = dict(read_clock_is_faster=read_clock_is_faster)

                for generics in self.generate_common_fifo_test_generics(
                    test.name, original_generics
                ):
                    self.add_vunit_config(test, generics=generics)

        for test in vunit_proj.library(self.library_name).test_bench("tb_fifo").get_tests():
            for generics in self.generate_common_fifo_test_generics(test.name):
                self.add_vunit_config(test, generics=generics)

    @staticmethod
    def generate_common_fifo_test_generics(test_name, original_generics=None):
        generics = original_generics if original_generics is not None else dict()

        if "write_faster_than_read" in test_name:
            generics.update(read_stall_probability_percent=90)
            generics.update(enable_last=True)

        if "read_faster_than_write" in test_name:
            generics.update(write_stall_probability_percent=90)

        if "packet_mode" in test_name:
            generics.update(enable_last=True, enable_packet_mode=True)

        if "drop_packet" in test_name:
            generics.update(enable_last=True, enable_packet_mode=True, enable_drop_packet=True)

        if "init_state" in test_name or "almost" in test_name:
            # Note that
            #   almost_full_level = depth, or
            #   almost_empty_level = 0
            # result in alternative ways of calculating almost full/empty.
            depth = 32

            for almost_full_level, almost_empty_level in [(depth, depth // 2), (depth // 2, 0)]:
                generics.update(
                    depth=depth,
                    almost_full_level=almost_full_level,
                    almost_empty_level=almost_empty_level,
                )

                yield generics

        elif (
            "drop_packet_mode_read_level_should_be_zero" in test_name
            or "drop_packet_in_same_cycle_as_write_last_should_drop_the_packet" in test_name
        ):
            # Do not need to test these in many configurations
            generics.update(depth=16)
            yield generics

        else:
            # For most test, generate configuration with two different depths
            for depth in [16, 512]:
                generics.update(depth=depth)

                yield generics

    def setup_formal(self, formal_proj, **kwargs):
        depth = 4
        base_generics = dict(
            width=3,
            depth=depth,
            enable_last=True,
        )

        for (almost_full_level, almost_empty_level) in [(depth - 1, 0), (depth, 1)]:
            generics = dict(
                base_generics,
                almost_full_level=almost_full_level,
                almost_empty_level=almost_empty_level,
            )
            formal_proj.add_config(
                top="fifo",
                generics=generics,
                engine_command="smtbmc",
                solver_command="z3",
                mode="prove",
            )

    def get_build_projects(self):
        projects = []
        modules = get_tsfpga_modules()
        part = "xc7z020clg400-1"

        self._setup_fifo_build_projects(projects, modules, part)
        self._setup_asynchronous_fifo_build_projects(projects, modules, part)

        return projects

    def _setup_fifo_build_projects(self, projects, modules, part):
        generics = dict(use_asynchronous_fifo=False, width=32, depth=1024)

        # Use a wrapper as top level, which only routes the "barebone" ports, resulting in
        # a minimal FIFO.
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("fifo_minimal", generics),
                modules=modules,
                part=part,
                top="fifo_netlist_build_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(14)),
                    Ffs(EqualTo(24)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # A FIFO with level counter port and non-default almost_full_level, which
        # increases resource utilization.
        generics.update(almost_full_level=800)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("fifo", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(26)),
                    Ffs(EqualTo(35)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling last should not increase resource utilization
        generics.update(enable_last=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("fifo_with_last", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(26)),
                    Ffs(EqualTo(35)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling packet mode increases resource utilization a bit, since an extra counter
        # and some further logic is introduced.
        generics.update(enable_packet_mode=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("fifo_with_packet_mode", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(41)),
                    Ffs(EqualTo(46)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling drop packet support increases utilization further, since an extra counter
        # and some further logic is introduced.
        generics.update(enable_drop_packet=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("fifo_with_drop_packet_support", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(47)),
                    Ffs(EqualTo(57)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

    def _setup_asynchronous_fifo_build_projects(self, projects, modules, part):
        generics = dict(use_asynchronous_fifo=True, width=32, depth=1024)

        # Use a wrapper as top level, which only routes the "barebone" ports, resulting in
        # a minimal FIFO.
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("asynchronous_fifo_minimal", generics),
                modules=modules,
                part=part,
                top="fifo_netlist_build_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(44)),
                    Ffs(EqualTo(90)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # A FIFO with level counter ports and non-default almost_full_level, which
        # increases resource utilization.
        generics.update(almost_full_level=800)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("asynchronous_fifo", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(67)),
                    Ffs(EqualTo(112)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling last should not increase resource utilization
        generics.update(enable_last=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("asynchronous_fifo_with_last", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(67)),
                    Ffs(EqualTo(112)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling packet mode increases resource utilization quite a lot since another
        # resync_counter is added.
        generics.update(enable_packet_mode=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("asynchronous_fifo_with_packet_mode", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(86)),
                    Ffs(EqualTo(167)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )

        # Enabling drop_packet support actually decreases utilization. Some logic is added for
        # handling the drop_packet functionality, but one resync_counter instance is saved since
        # the read_level value is not used.
        generics.update(enable_drop_packet=True)
        projects.append(
            VivadoNetlistProject(
                name=self.test_case_name("asynchronous_fifo_with_drop_packet_support", generics),
                modules=modules,
                part=part,
                top="fifo_wrapper",
                generics=generics,
                result_size_checkers=[
                    TotalLuts(EqualTo(66)),
                    Ffs(EqualTo(134)),
                    Ramb36(EqualTo(1)),
                    Ramb18(EqualTo(0)),
                ],
            )
        )
