// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0
//
// xbar_env_pkg__params generated by `tlgen.py` tool

<%
  name_len = max([len(x.name) for x in xbar.devices])
%>\

// List of Xbar device memory map
tl_device_t xbar_devices[$] = '{
% for device in xbar.devices:
    '{"${device.esc_name()}", '{
    % for addr in device.addr_range:
        '{32'h${"%08x" % addr[0]}, 32'h${"%08x" % addr[1]}}${"," if not loop.last else ""}
    % endfor
  % if loop.last:
}}};
  % else:
    }},
  % endif
% endfor

  // List of Xbar hosts
tl_host_t xbar_hosts[$] = '{
% for host in xbar.hosts:
    '{"${host.name}", ${loop.index}, '{
  % for device in xbar.get_devices_from_host(host):
        "${device.esc_name()}"${'}}' if loop.last else ','}
  % endfor
  % if loop.last:
};
  % else:
    ,
  % endif
% endfor
