-- -------------------------------------------------------------------------------------------------
-- Copyright (c) Lukas Vik. All rights reserved.
--
-- This file is part of the tsfpga project.
-- https://tsfpga.com
-- https://gitlab.com/tsfpga/tsfpga
-- -------------------------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library math;
use math.math_pkg.all;

library axi;
use axi.axil_pkg.all;

library vunit_lib;
context vunit_lib.vunit_context;
context vunit_lib.vc_context;


entity axil_master is
  generic (
    bus_handle : bus_master_t
  );
  port (
    clk : in std_logic;

    axil_m2s : out axil_m2s_t := axil_m2s_init;
    axil_s2m : in axil_s2m_t := axil_s2m_init
  );
end entity;

architecture a of axil_master is

  signal rdata, wdata : std_logic_vector(data_length(bus_handle) - 1 downto 0);
  signal wstrb : std_logic_vector(byte_enable_length(bus_handle) - 1 downto 0);

  signal araddr, awaddr : std_logic_vector(address_length(bus_handle) - 1 downto 0);

begin

  ------------------------------------------------------------------------------
  axil_m2s.read.ar.addr(araddr'range) <= unsigned(araddr);
  rdata <= axil_s2m.read.r.data(rdata'range);

  axil_m2s.write.aw.addr(awaddr'range) <= unsigned(awaddr);
  axil_m2s.write.w.data(wdata'range) <= wdata;
  axil_m2s.write.w.strb(wstrb'range) <= wstrb;


  ------------------------------------------------------------------------------
  axi_lite_master_inst : entity vunit_lib.axi_lite_master
  generic map (
    bus_handle => bus_handle
  )
  port map (
    aclk => clk,

    arready => axil_s2m.read.ar.ready,
    arvalid => axil_m2s.read.ar.valid,
    araddr => araddr,

    rready => axil_m2s.read.r.ready,
    rvalid => axil_s2m.read.r.valid,
    rdata => rdata,
    rresp => axil_s2m.read.r.resp,

    awready => axil_s2m.write.aw.ready,
    awvalid => axil_m2s.write.aw.valid,
    awaddr => awaddr,

    wready => axil_s2m.write.w.ready,
    wvalid => axil_m2s.write.w.valid,
    wdata => wdata,
    wstrb => wstrb,

    bready => axil_m2s.write.b.ready,
    bvalid => axil_s2m.write.b.valid,
    bresp => axil_s2m.write.b.resp
  );

end architecture;
