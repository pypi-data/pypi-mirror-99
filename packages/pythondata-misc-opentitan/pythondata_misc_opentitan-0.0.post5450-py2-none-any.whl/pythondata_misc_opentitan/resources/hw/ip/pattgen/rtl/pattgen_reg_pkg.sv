// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0
//
// Register Package auto-generated by `reggen` containing data structure

package pattgen_reg_pkg;

  // Param list
  parameter int NumRegsData = 2;

  // Address widths within the block
  parameter int BlockAw = 6;

  ////////////////////////////
  // Typedefs for registers //
  ////////////////////////////

  typedef struct packed {
    struct packed {
      logic        q;
    } done_ch0;
    struct packed {
      logic        q;
    } done_ch1;
  } pattgen_reg2hw_intr_state_reg_t;

  typedef struct packed {
    struct packed {
      logic        q;
    } done_ch0;
    struct packed {
      logic        q;
    } done_ch1;
  } pattgen_reg2hw_intr_enable_reg_t;

  typedef struct packed {
    struct packed {
      logic        q;
      logic        qe;
    } done_ch0;
    struct packed {
      logic        q;
      logic        qe;
    } done_ch1;
  } pattgen_reg2hw_intr_test_reg_t;

  typedef struct packed {
    struct packed {
      logic        q;
    } enable_ch0;
    struct packed {
      logic        q;
    } enable_ch1;
    struct packed {
      logic        q;
    } polarity_ch0;
    struct packed {
      logic        q;
    } polarity_ch1;
  } pattgen_reg2hw_ctrl_reg_t;

  typedef struct packed {
    logic [31:0] q;
  } pattgen_reg2hw_prediv_ch0_reg_t;

  typedef struct packed {
    logic [31:0] q;
  } pattgen_reg2hw_prediv_ch1_reg_t;

  typedef struct packed {
    logic [31:0] q;
  } pattgen_reg2hw_data_ch0_mreg_t;

  typedef struct packed {
    logic [31:0] q;
  } pattgen_reg2hw_data_ch1_mreg_t;

  typedef struct packed {
    struct packed {
      logic [5:0]  q;
    } len_ch0;
    struct packed {
      logic [9:0] q;
    } reps_ch0;
    struct packed {
      logic [5:0]  q;
    } len_ch1;
    struct packed {
      logic [9:0] q;
    } reps_ch1;
  } pattgen_reg2hw_size_reg_t;

  typedef struct packed {
    struct packed {
      logic        d;
      logic        de;
    } done_ch0;
    struct packed {
      logic        d;
      logic        de;
    } done_ch1;
  } pattgen_hw2reg_intr_state_reg_t;

  // Register -> HW type
  typedef struct packed {
    pattgen_reg2hw_intr_state_reg_t intr_state; // [235:234]
    pattgen_reg2hw_intr_enable_reg_t intr_enable; // [233:232]
    pattgen_reg2hw_intr_test_reg_t intr_test; // [231:228]
    pattgen_reg2hw_ctrl_reg_t ctrl; // [227:224]
    pattgen_reg2hw_prediv_ch0_reg_t prediv_ch0; // [223:192]
    pattgen_reg2hw_prediv_ch1_reg_t prediv_ch1; // [191:160]
    pattgen_reg2hw_data_ch0_mreg_t [1:0] data_ch0; // [159:96]
    pattgen_reg2hw_data_ch1_mreg_t [1:0] data_ch1; // [95:32]
    pattgen_reg2hw_size_reg_t size; // [31:0]
  } pattgen_reg2hw_t;

  // HW -> register type
  typedef struct packed {
    pattgen_hw2reg_intr_state_reg_t intr_state; // [3:0]
  } pattgen_hw2reg_t;

  // Register offsets
  parameter logic [BlockAw-1:0] PATTGEN_INTR_STATE_OFFSET = 6'h 0;
  parameter logic [BlockAw-1:0] PATTGEN_INTR_ENABLE_OFFSET = 6'h 4;
  parameter logic [BlockAw-1:0] PATTGEN_INTR_TEST_OFFSET = 6'h 8;
  parameter logic [BlockAw-1:0] PATTGEN_CTRL_OFFSET = 6'h c;
  parameter logic [BlockAw-1:0] PATTGEN_PREDIV_CH0_OFFSET = 6'h 10;
  parameter logic [BlockAw-1:0] PATTGEN_PREDIV_CH1_OFFSET = 6'h 14;
  parameter logic [BlockAw-1:0] PATTGEN_DATA_CH0_0_OFFSET = 6'h 18;
  parameter logic [BlockAw-1:0] PATTGEN_DATA_CH0_1_OFFSET = 6'h 1c;
  parameter logic [BlockAw-1:0] PATTGEN_DATA_CH1_0_OFFSET = 6'h 20;
  parameter logic [BlockAw-1:0] PATTGEN_DATA_CH1_1_OFFSET = 6'h 24;
  parameter logic [BlockAw-1:0] PATTGEN_SIZE_OFFSET = 6'h 28;

  // Reset values for hwext registers and their fields
  parameter logic [1:0] PATTGEN_INTR_TEST_RESVAL = 2'h 0;
  parameter logic [0:0] PATTGEN_INTR_TEST_DONE_CH0_RESVAL = 1'h 0;
  parameter logic [0:0] PATTGEN_INTR_TEST_DONE_CH1_RESVAL = 1'h 0;

  // Register index
  typedef enum int {
    PATTGEN_INTR_STATE,
    PATTGEN_INTR_ENABLE,
    PATTGEN_INTR_TEST,
    PATTGEN_CTRL,
    PATTGEN_PREDIV_CH0,
    PATTGEN_PREDIV_CH1,
    PATTGEN_DATA_CH0_0,
    PATTGEN_DATA_CH0_1,
    PATTGEN_DATA_CH1_0,
    PATTGEN_DATA_CH1_1,
    PATTGEN_SIZE
  } pattgen_id_e;

  // Register width information to check illegal writes
  parameter logic [3:0] PATTGEN_PERMIT [11] = '{
    4'b 0001, // index[ 0] PATTGEN_INTR_STATE
    4'b 0001, // index[ 1] PATTGEN_INTR_ENABLE
    4'b 0001, // index[ 2] PATTGEN_INTR_TEST
    4'b 0001, // index[ 3] PATTGEN_CTRL
    4'b 1111, // index[ 4] PATTGEN_PREDIV_CH0
    4'b 1111, // index[ 5] PATTGEN_PREDIV_CH1
    4'b 1111, // index[ 6] PATTGEN_DATA_CH0_0
    4'b 1111, // index[ 7] PATTGEN_DATA_CH0_1
    4'b 1111, // index[ 8] PATTGEN_DATA_CH1_0
    4'b 1111, // index[ 9] PATTGEN_DATA_CH1_1
    4'b 1111  // index[10] PATTGEN_SIZE
  };

endpackage

