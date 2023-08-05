// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0

class dcd_common_vseq extends dcd_base_vseq;
  `uvm_object_utils(dcd_common_vseq)

  constraint num_trans_c {
    num_trans inside {[1:2]};
  }
  `uvm_object_new

  virtual task body();
    run_common_vseq_wrapper(num_trans);
  endtask : body

endclass
