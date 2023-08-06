-- -------------------------------------------------------------------------------------------------
-- Copyright (c) Lukas Vik. All rights reserved.
--
-- This file is part of the tsfpga project.
-- https://tsfpga.com
-- https://gitlab.com/tsfpga/tsfpga
-- -------------------------------------------------------------------------------------------------
-- Wrapper around VUnit BFM that uses convenient record types for the AXI signals.
-- -------------------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library axi;
use axi.axi_pkg.all;
use axi.axil_pkg.all;

library vunit_lib;
context vunit_lib.vc_context;


entity axil_read_slave is
  generic (
    axi_slave : axi_slave_t;
    data_width : integer
  );
  port (
    clk : in std_logic;
    --
    axil_read_m2s : in axil_read_m2s_t := axil_read_m2s_init;
    axil_read_s2m : out axil_read_s2m_t := axil_read_s2m_init
  );
end entity;

architecture a of axil_read_slave is

  constant len : std_logic_vector(axi_a_len_sz - 1 downto 0) := std_logic_vector(to_len(1));
  constant size : std_logic_vector(axi_a_size_sz - 1 downto 0) :=
    std_logic_vector(to_size(data_width));

  -- Using "open" not ok in GHDL: unconstrained port "rid" must be connected
  signal rid, aid : std_logic_vector(8 - 1 downto 0) := (others => '0');

  signal araddr : std_logic_vector(axil_read_m2s.ar.addr'range);

begin

  ------------------------------------------------------------------------------
  axi_read_slave_inst : entity vunit_lib.axi_read_slave
    generic map (
      axi_slave => axi_slave
    )
    port map (
      aclk => clk,

      arvalid => axil_read_m2s.ar.valid,
      arready => axil_read_s2m.ar.ready,
      arid => aid,
      araddr => araddr,
      arlen => len,
      arsize => size,
      arburst => axi_a_burst_fixed,

      rvalid => axil_read_s2m.r.valid,
      rready => axil_read_m2s.r.ready,
      rid => rid,
      rdata => axil_read_s2m.r.data(data_width - 1 downto 0),
      rresp => axil_read_s2m.r.resp,
      rlast => open
    );

  araddr <= std_logic_vector(axil_read_m2s.ar.addr);

end architecture;
