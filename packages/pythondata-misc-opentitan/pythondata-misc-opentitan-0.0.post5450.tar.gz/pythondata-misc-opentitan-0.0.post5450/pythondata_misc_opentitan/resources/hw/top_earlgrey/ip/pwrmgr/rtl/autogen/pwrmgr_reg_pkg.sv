// Copyright lowRISC contributors.
// Licensed under the Apache License, Version 2.0, see LICENSE for details.
// SPDX-License-Identifier: Apache-2.0
//
// Register Package auto-generated by `reggen` containing data structure

package pwrmgr_reg_pkg;

  // Param list
  parameter int NumWkups = 4;
  parameter int DEBUG_CABLE_WAKEUP_IDX = 0;
  parameter int AON_WKUP_REQ_IDX = 1;
  parameter int USB_WKUP_REQ_IDX = 2;
  parameter int AON_TIMER_WKUP_REQ_IDX = 3;
  parameter int NumRstReqs = 1;

  // Address widths within the block
  parameter int BlockAw = 6;

  ////////////////////////////
  // Typedefs for registers //
  ////////////////////////////

  typedef struct packed {
    logic        q;
  } pwrmgr_reg2hw_intr_state_reg_t;

  typedef struct packed {
    logic        q;
  } pwrmgr_reg2hw_intr_enable_reg_t;

  typedef struct packed {
    logic        q;
    logic        qe;
  } pwrmgr_reg2hw_intr_test_reg_t;

  typedef struct packed {
    struct packed {
      logic        q;
    } low_power_hint;
    struct packed {
      logic        q;
    } core_clk_en;
    struct packed {
      logic        q;
    } io_clk_en;
    struct packed {
      logic        q;
    } usb_clk_en_lp;
    struct packed {
      logic        q;
    } usb_clk_en_active;
    struct packed {
      logic        q;
    } main_pd_n;
  } pwrmgr_reg2hw_control_reg_t;

  typedef struct packed {
    logic        q;
    logic        qe;
  } pwrmgr_reg2hw_cfg_cdc_sync_reg_t;

  typedef struct packed {
    logic        q;
  } pwrmgr_reg2hw_wakeup_en_mreg_t;

  typedef struct packed {
    logic        q;
  } pwrmgr_reg2hw_reset_en_mreg_t;

  typedef struct packed {
    logic        q;
  } pwrmgr_reg2hw_wake_info_capture_dis_reg_t;

  typedef struct packed {
    struct packed {
      logic [3:0]  q;
      logic        qe;
    } reasons;
    struct packed {
      logic        q;
      logic        qe;
    } fall_through;
    struct packed {
      logic        q;
      logic        qe;
    } abort;
  } pwrmgr_reg2hw_wake_info_reg_t;

  typedef struct packed {
    logic        d;
    logic        de;
  } pwrmgr_hw2reg_intr_state_reg_t;

  typedef struct packed {
    logic        d;
  } pwrmgr_hw2reg_ctrl_cfg_regwen_reg_t;

  typedef struct packed {
    struct packed {
      logic        d;
      logic        de;
    } low_power_hint;
  } pwrmgr_hw2reg_control_reg_t;

  typedef struct packed {
    logic        d;
    logic        de;
  } pwrmgr_hw2reg_cfg_cdc_sync_reg_t;

  typedef struct packed {
    logic        d;
    logic        de;
  } pwrmgr_hw2reg_wake_status_mreg_t;

  typedef struct packed {
    logic        d;
    logic        de;
  } pwrmgr_hw2reg_reset_status_mreg_t;

  typedef struct packed {
    logic        d;
    logic        de;
  } pwrmgr_hw2reg_escalate_reset_status_reg_t;

  typedef struct packed {
    struct packed {
      logic [3:0]  d;
    } reasons;
    struct packed {
      logic        d;
    } fall_through;
    struct packed {
      logic        d;
    } abort;
  } pwrmgr_hw2reg_wake_info_reg_t;

  // Register -> HW type
  typedef struct packed {
    pwrmgr_reg2hw_intr_state_reg_t intr_state; // [26:26]
    pwrmgr_reg2hw_intr_enable_reg_t intr_enable; // [25:25]
    pwrmgr_reg2hw_intr_test_reg_t intr_test; // [24:23]
    pwrmgr_reg2hw_control_reg_t control; // [22:17]
    pwrmgr_reg2hw_cfg_cdc_sync_reg_t cfg_cdc_sync; // [16:15]
    pwrmgr_reg2hw_wakeup_en_mreg_t [3:0] wakeup_en; // [14:11]
    pwrmgr_reg2hw_reset_en_mreg_t [0:0] reset_en; // [10:10]
    pwrmgr_reg2hw_wake_info_capture_dis_reg_t wake_info_capture_dis; // [9:9]
    pwrmgr_reg2hw_wake_info_reg_t wake_info; // [8:0]
  } pwrmgr_reg2hw_t;

  // HW -> register type
  typedef struct packed {
    pwrmgr_hw2reg_intr_state_reg_t intr_state; // [24:23]
    pwrmgr_hw2reg_ctrl_cfg_regwen_reg_t ctrl_cfg_regwen; // [22:22]
    pwrmgr_hw2reg_control_reg_t control; // [21:20]
    pwrmgr_hw2reg_cfg_cdc_sync_reg_t cfg_cdc_sync; // [19:18]
    pwrmgr_hw2reg_wake_status_mreg_t [3:0] wake_status; // [17:10]
    pwrmgr_hw2reg_reset_status_mreg_t [0:0] reset_status; // [9:8]
    pwrmgr_hw2reg_escalate_reset_status_reg_t escalate_reset_status; // [7:6]
    pwrmgr_hw2reg_wake_info_reg_t wake_info; // [5:0]
  } pwrmgr_hw2reg_t;

  // Register offsets
  parameter logic [BlockAw-1:0] PWRMGR_INTR_STATE_OFFSET = 6'h 0;
  parameter logic [BlockAw-1:0] PWRMGR_INTR_ENABLE_OFFSET = 6'h 4;
  parameter logic [BlockAw-1:0] PWRMGR_INTR_TEST_OFFSET = 6'h 8;
  parameter logic [BlockAw-1:0] PWRMGR_CTRL_CFG_REGWEN_OFFSET = 6'h c;
  parameter logic [BlockAw-1:0] PWRMGR_CONTROL_OFFSET = 6'h 10;
  parameter logic [BlockAw-1:0] PWRMGR_CFG_CDC_SYNC_OFFSET = 6'h 14;
  parameter logic [BlockAw-1:0] PWRMGR_WAKEUP_EN_REGWEN_OFFSET = 6'h 18;
  parameter logic [BlockAw-1:0] PWRMGR_WAKEUP_EN_OFFSET = 6'h 1c;
  parameter logic [BlockAw-1:0] PWRMGR_WAKE_STATUS_OFFSET = 6'h 20;
  parameter logic [BlockAw-1:0] PWRMGR_RESET_EN_REGWEN_OFFSET = 6'h 24;
  parameter logic [BlockAw-1:0] PWRMGR_RESET_EN_OFFSET = 6'h 28;
  parameter logic [BlockAw-1:0] PWRMGR_RESET_STATUS_OFFSET = 6'h 2c;
  parameter logic [BlockAw-1:0] PWRMGR_ESCALATE_RESET_STATUS_OFFSET = 6'h 30;
  parameter logic [BlockAw-1:0] PWRMGR_WAKE_INFO_CAPTURE_DIS_OFFSET = 6'h 34;
  parameter logic [BlockAw-1:0] PWRMGR_WAKE_INFO_OFFSET = 6'h 38;

  // Reset values for hwext registers and their fields
  parameter logic [0:0] PWRMGR_INTR_TEST_RESVAL = 1'h 0;
  parameter logic [0:0] PWRMGR_INTR_TEST_WAKEUP_RESVAL = 1'h 0;
  parameter logic [0:0] PWRMGR_CTRL_CFG_REGWEN_RESVAL = 1'h 1;
  parameter logic [0:0] PWRMGR_CTRL_CFG_REGWEN_EN_RESVAL = 1'h 1;
  parameter logic [5:0] PWRMGR_WAKE_INFO_RESVAL = 6'h 0;
  parameter logic [3:0] PWRMGR_WAKE_INFO_REASONS_RESVAL = 4'h 0;
  parameter logic [0:0] PWRMGR_WAKE_INFO_FALL_THROUGH_RESVAL = 1'h 0;
  parameter logic [0:0] PWRMGR_WAKE_INFO_ABORT_RESVAL = 1'h 0;

  // Register index
  typedef enum int {
    PWRMGR_INTR_STATE,
    PWRMGR_INTR_ENABLE,
    PWRMGR_INTR_TEST,
    PWRMGR_CTRL_CFG_REGWEN,
    PWRMGR_CONTROL,
    PWRMGR_CFG_CDC_SYNC,
    PWRMGR_WAKEUP_EN_REGWEN,
    PWRMGR_WAKEUP_EN,
    PWRMGR_WAKE_STATUS,
    PWRMGR_RESET_EN_REGWEN,
    PWRMGR_RESET_EN,
    PWRMGR_RESET_STATUS,
    PWRMGR_ESCALATE_RESET_STATUS,
    PWRMGR_WAKE_INFO_CAPTURE_DIS,
    PWRMGR_WAKE_INFO
  } pwrmgr_id_e;

  // Register width information to check illegal writes
  parameter logic [3:0] PWRMGR_PERMIT [15] = '{
    4'b 0001, // index[ 0] PWRMGR_INTR_STATE
    4'b 0001, // index[ 1] PWRMGR_INTR_ENABLE
    4'b 0001, // index[ 2] PWRMGR_INTR_TEST
    4'b 0001, // index[ 3] PWRMGR_CTRL_CFG_REGWEN
    4'b 0011, // index[ 4] PWRMGR_CONTROL
    4'b 0001, // index[ 5] PWRMGR_CFG_CDC_SYNC
    4'b 0001, // index[ 6] PWRMGR_WAKEUP_EN_REGWEN
    4'b 0001, // index[ 7] PWRMGR_WAKEUP_EN
    4'b 0001, // index[ 8] PWRMGR_WAKE_STATUS
    4'b 0001, // index[ 9] PWRMGR_RESET_EN_REGWEN
    4'b 0001, // index[10] PWRMGR_RESET_EN
    4'b 0001, // index[11] PWRMGR_RESET_STATUS
    4'b 0001, // index[12] PWRMGR_ESCALATE_RESET_STATUS
    4'b 0001, // index[13] PWRMGR_WAKE_INFO_CAPTURE_DIS
    4'b 0001  // index[14] PWRMGR_WAKE_INFO
  };

endpackage

