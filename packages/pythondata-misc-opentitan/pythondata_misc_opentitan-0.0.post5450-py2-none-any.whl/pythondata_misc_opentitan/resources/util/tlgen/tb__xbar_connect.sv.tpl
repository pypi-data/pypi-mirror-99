// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0
//
// tb__xbar_connect generated by `tlgen.py` tool

xbar_${xbar.name} dut();

% for clk in xbar.clocks:
`DRIVE_CLK(${clk})
% endfor

% for clk in xbar.clocks:
initial force dut.${clk} = ${clk};
% endfor

// TODO, all resets tie together
% for rst in xbar.resets:
initial force dut.${rst} = rst_n;
% endfor

// Host TileLink interface connections
% for node in xbar.hosts:
`CONNECT_TL_HOST_IF(${node.name.replace('.', '__')}, dut, ${node.clocks[0]}, rst_n)
% endfor

// Device TileLink interface connections
% for node in xbar.devices:
`CONNECT_TL_DEVICE_IF(${node.name.replace('.', '__')}, dut, ${node.clocks[0]}, rst_n)
% endfor
