ULP coprocessor instruction set
===============================

ULP は 4つの 16-bit の汎用レジスタ `R0`, `R1`, `R2`, `R3` がある。
また 8-bit のカウンタレジスタ `stage_cnt` がありループ処理に用いる。
`stage_cnt` は専用の命令によってアクセスされる。

ULP は 8k bytes の `RTC_SLOW_MEM` というメモリ領域を持つ。
32-bit word 単位のため 2k word のメモリとして CPU と ULP の両方からアクセスできる。
`RTC_CNTL`, `RTC_IO`, `SENS` ペリフェラルのレジスタにもアクセスできる。

すべての命令は 32-bit 長で、JUMP命令、ALU命令、ペリフェラルレジスタやメモリアクセスの命令は 1 cycle で実行される。TSENS, ADC, I2C の周辺装置を操作する命令は操作事項に応じて数 cycle が必要となる。

命令文は大文字小文字関係ない。レジスタ名も同様である。


命令実行時間について
--------------------

ULP は `RTC_FAST_CLK` という内蔵 8MHz の発振器のクロックを利用する。
正確な精度を必要する場合は下記の手順でキャリブレートする。

```
#include "soc/rtc.h"

// calibrate 8M/256 clock against XTAL, get 8M/256 clock period
uint32_t rtc_8md256_period = rtc_clk_cal(RTC_CAL_8MD256, 100);
uint32_t rtc_fast_freq_hz = 1000000ULL * (1 << RTC_CLK_CAL_FRACT) * 256 / rtc_8md256_period;
```

NOP (2c to execute, 4c to fetch)
-----
    NOP
何もしない、PCをすすめるだけ


ADD (2c to execute, 4c to fetch)
-----
Syntax
    ADD Rdst, Rsrc1, Rsrc2
    ADD Rdst, Rsrc1, imm
      Rdst - Register R[0..3]    Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]   Imm - 16-bit signed value
Rsrc1 と Rsrc2 または 16bit の符号付き値を加算して Rdst に代入する。

1:    add r1, r2, r3        //r1 = r2 + r3
2:    add r1, r2, 0x1234    //r1 = r2 + 0x1234
3:    .set value1, 0x03     //constant value1=0x03
      add r1, r2, value1    //r1 = r2 + value1
4:    .global label         //declaration of variable label
      add r1, r2, label     //r1 = r2 + label
        ...
      label: nop            //definition of variable label

SUB (2c to execute, 4c to fetch)
-----
    SUB Rdst, Rsrc1, Rsrc2
    SUB Rdst, Rsrc1, imm
      Rdst - Register R[0..3]      Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]     Imm - 16-bit signed value
Rsrc1 から Rsrc2 もしくは 16bit の符号付き値を引いて、 Rdst に代入する。

1:         sub r1, r2, r3             //r1 = r2 - r3
2:         sub r1, r2, 0x1234         //r1 = r2 - 0x1234
3:         .set value1, 0x03          //constant value1=0x03
           sub r1, r2, value1         //r1 = r2 - value1
4:         .global label              //declaration of variable label
           sub r1, r2, label          //r1 = r2 - label
             ....
  label:   nop                        //definition of variable label


AND (2c to execute, 4c to fetch)
-----
    AND Rdst, Rsrc1, Rsrc2
    AND Rdst, Rsrc1, imm
      Rdst - Register R[0..3]      Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]     Imm - 16-bit signed value
Rsrc1 と Rsrc2 もしくは 16-bit 符号付き値と論理ANDを計算し、Rdst に代入する。

1:        and r1, r2, r3          //r1 = r2 & r3
2:        and r1, r2, 0x1234      //r1 = r2 & 0x1234
3:        .set value1, 0x03       //constant value1=0x03
          and r1, r2, value1      //r1 = r2 & value1
4:        .global label           //declaration of variable label
          and r1, r2, label       //r1 = r2 & label
              ...
  label:  nop                     //definition of variable label


OR - Logical OR of two operands
-----
    OR Rdst, Rsrc1, Rsrc2
    OR Rdst, Rsrc1, imm
      Rdst - Register R[0..3]     Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]    Imm - 16-bit signed value
Rsrc1 と Rsrc2 もしくは 16-bit 符号付き値と論理ORを計算し、Rdst に代入する。

1:       or r1, r2, r3           //r1 = r2 \| r3
2:       or r1, r2, 0x1234       //r1 = r2 \| 0x1234
3:       .set value1, 0x03       //constant value1=0x03
         or r1, r2, value1       //r1 = r2 \| value1
4:       .global label           //declaration of variable label
         or r1, r2, label        //r1 = r2 \|label
         ...
  label: nop                     //definition of variable label


LSH - Logical Shift Left
-----
    LSH Rdst, Rsrc1, Rsrc2
    LSH Rdst, Rsrc1, imm
      Rdst - Register R[0..3]      Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]     Imm - 16-bit signed value

The instruction does logical shift to left of source register to number of bits from another source register or 16-bit signed value and store result to the destination register.

1:       lsh r1, r2, r3            //r1 = r2 << r3
2:       lsh r1, r2, 0x03          //r1 = r2 << 0x03
3:       .set value1, 0x03         //constant value1=0x03
         lsh r1, r2, value1        //r1 = r2 << value1
4:       .global label             //declaration of variable label
         lsh r1, r2, label         //r1 = r2 << label
         ...
  label:  nop                       //definition of variable label


RSH - Logical Shift Right
-----
    RSH Rdst, Rsrc1, Rsrc2
    RSH Rdst, Rsrc1, imm
      Rdst - Register R[0..3]      Rsrc1 - Register R[0..3]
      Rsrc2 - Register R[0..3]     Imm - 16-bit signed value
The instruction does logical shift to right of source register to number of bits from another source register or 16-bit signed value and store result to the destination register.

1:        rsh r1, r2, r3              //r1 = r2 >> r3
2:        rsh r1, r2, 0x03            //r1 = r2 >> 0x03
3:        .set value1, 0x03           //constant value1=0x03
          rsh r1, r2, value1          //r1 = r2 >> value1
4:        .global label               //declaration of variable label
          rsh r1, r2, label           //r1 = r2 >> label
  label:  nop                         //definition of variable label


MOVE – Move to register
-----
    MOVE Rdst, Rsrc
    MOVE Rdst, imm
      Rdst – Register R[0..3]     Rsrc – Register R[0..3]
      Imm – 16-bit signed value

The instruction move to destination register value from source register or 16-bit signed value.

Note that when a label is used as an immediate, the address of the label will be converted from bytes to words. This is because LD, ST, and JUMP instructions expect the address register value to be expressed in words rather than bytes. To avoid using an extra instruction

1:        move       r1, r2            //r1 = r2
2:        move       r1, 0x03          //r1 = 0x03
3:        .set       value1, 0x03      //constant value1=0x03
          move       r1, value1        //r1 = value1
4:        .global     label            //declaration of label
          move        r1, label        //r1 = address_of(label) / 4
          ...
  label:  nop                          //definition of label



ST (4c to execute, 4c to fetch next instruction)
-----
    ST Rsrc, Rdst, offset
      Rsrc – Register R[0..3], holds the 16-bit value to store
      Rdst – Register R[0..3], address of the destination, in 32-bit words
      Offset – 10-bit signed value, offset in bytes

The instruction stores the 16-bit value of Rsrc to the lower half-word of memory with address Rdst+offset. The upper half-word is written with the current program counter (PC), expressed in words, shifted left by 5 bits:

    Mem[Rdst + offset / 4]{31:0} = {PC[10:0], 5'b0, Rsrc[15:0]}

The application can use higher 16 bits to determine which instruction in the ULP program has written any particular word into memory.


1:        st  r1, r2, 0x12        //mem[r2+0x12] = r1
2:        .data                   //data section definition
  addr1:  .word     123           // define label addr1 16 bit
          .set      offs, 0x00    // define constant offs
          .text                   //text section definition
          move      r1, 1         // r1 = 1
          move      r2, addr1     // r2 = addr1
          st        r1, r2, offs  // mem[r2 +  0] = r1
                                  // mem[addr1 + 0] will be 32'h600001


LD – Load data from the memory
-----
    LD Rdst, Rsrc, offset
      Rdst – Register R[0..3], destination
      Rsrc – Register R[0..3], holds address of destination, in 32-bit words
      offset – 10-bit signed value, offset in bytes

The instruction loads lower 16-bit half-word from memory with address Rsrc+offset into the destination register Rdst:

    Rdst[15:0] = Mem[Rsrc + offset / 4][15:0]


1:        ld  r1, r2, 0x12            //r1 = mem[r2+0x12]
2:        .data                       //data section definition
  addr1:  .word     123               // define label addr1 16 bit
          .set      offs, 0x00        // define constant offs
          .text                       //text section definition
          move      r1, 1             // r1 = 1
          move      r2, addr1         // r2 = addr1 / 4 (address of label is converted into words)
          ld        r1, r2, offs      // r1 = mem[r2 +  0]
                                      // r1 will be 123

JUMP (2c to execute, 2c to fetch next instruction)
-----
    JUMP Rdst
    JUMP ImmAddr
    JUMP Rdst, Condition
    JUMP ImmAddr, Condition

      Rdst – Register R[0..3] containing address to jump to (expressed in 32-bit words)
      ImmAddr – 13 bits address (expressed in bytes), aligned to 4 bytes
      Condition:
         EQ – jump if last ALU operation result was zero
         OV – jump if last ALU has set overflow flag

The instruction makes jump to the specified address. Jump can be either unconditional or based on an ALU flag.

1:        JUMP       R1            // Jump to address in R1 (address in R1 is in 32-bit words)
2:        JUMP       0x120, EQ     // Jump to address 0x120 (in bytes) if ALU result is zero
3:        JUMP       label         // Jump to label
          ...
  label:  nop                      // Definition of label
4:        .global    label         // Declaration of global label
          MOVE       R1, label     // R1 = label (value loaded into R1 is in words)
          JUMP       R1            // Jump to label
          ...
  label:  nop                      // Definition of label



JUMPR (2c to execute, 2c to fetch next instruction)
-----
    JUMPR Step, Threshold, Condition
      Step – relative shift from current position, in bytes
      Threshold – threshold value for branch condition
      Condition:
         GE (greater or equal) – jump if value in R0 >= threshold
         LT (less than) – jump if value in R0 < threshold

The instruction makes a jump to a relative address if condition is true. Condition is the result of comparison of R0 register value and the threshold value.

1:pos:    jumpr       16, 20, ge   // jump to address (position + 16 bytes) if value in r0 >= 20
2:        // down counting loop using r0 register
          move        r0, 16       // load 16 into r0
  label:  sub         r0, r0, 1    // r0--
          nop                      // do something
          jumpr       label, 1, ge // jump to label if r0 >= 1


JUMPS – 2 cycles to execute, 2 cycles to fetch next instruction
-----

    JUMPS Step, Threshold, Condition
      Step – relative shift from current position, in bytes
      Threshold – threshold value for branch condition
      Condition:
         LT (less than) – jump if value in stage_cnt < threshold
         LE (less or equal) - jump if value in stage_cnt <= threshold
         GE (greater or equal) — jump if value in stage_cnt >= threshold

      Conditions EQ, GT are implemented in the assembler using two JUMPS instructions:
    // JUMPS target, threshold, EQ is implemented as:
             JUMPS next, threshold, LT
             JUMPS target, threshold, LE
    next:

    // JUMPS target, threshold, GT is implemented as:
             JUMPS next, threshold, LE
             JUMPS target, threshold, GE
    next:

Therefore the execution time will depend on the branches taken: either 2 cycles to execute + 2 cycles to fetch, or 4 cycles to execute + 4 cycles to fetch.
Description
The instruction makes a jump to a relative address if condition is true. Condition is the result of comparison of count register value and threshold value.

Examples:
1:pos:    JUMPS     16, 20, EQ     // Jump to (position + 16 bytes) if stage_cnt == 20
2:        // Up counting loop using stage count register
          STAGE_RST                  // set stage_cnt to 0
  label:  STAGE_INC  1               // stage_cnt++
          NOP                        // do something
          JUMPS       label, 16, LT  // jump to label if stage_cnt < 16


STAGE_RST (2 cycles to execute, 4 cycles to fetch next instruction)
-----
    STAGE_RST
The instruction sets the stage count register to 0
Cycles


STAGE_INC (2 cycles to execute, 4 cycles to fetch next instruction)
-----
    STAGE_INC Value
      Value – 8 bits value
The instruction increments stage count register by given value.

1:        STAGE_INC      10          // stage_cnt += 10
2:        // Up counting loop example:
          STAGE_RST                  // set stage_cnt to 0
  label:  STAGE_INC  1               // stage_cnt++
          NOP                        // do something
          JUMPS      label, 16, LT   // jump to label if stage_cnt < 16


STAGE_DEC – Decrement stage count register
-----
    STAGE_DEC Value
      Value – 8 bits value
The instruction decrements stage count register by given value.


1:        STAGE_DEC      10        // stage_cnt -= 10;
2:        // Down counting loop exaple
          STAGE_RST                // set stage_cnt to 0
          STAGE_INC  16            // increment stage_cnt to 16
  label:  STAGE_DEC  1             // stage_cnt--;
          NOP                      // do something
          JUMPS      label, 0, GT  // jump to label if stage_cnt > 0


HALT (2 cycles to execute)
-----
    HALT
Cycles

The instruction halts the ULP coprocessor and restarts ULP wakeup timer, if it is enabled.

1:       HALT      // Halt the coprocessor


WAKE (2 cycles to execute, 4 cycles to fetch next instruction)
-----
    WAKE

The instruction sends an interrupt from ULP to RTC controller.

If the SoC is in deep sleep mode, and ULP wakeup is enabled, this causes the SoC to wake up.
If the SoC is not in deep sleep mode, and ULP interrupt bit (RTC_CNTL_ULP_CP_INT_ENA) is set in RTC_CNTL_INT_ENA_REG register, RTC interrupt will be triggered.

Note that before using WAKE instruction, ULP program may needs to wait until RTC controller is ready to wake up the main CPU. This is indicated using RTC_CNTL_RDY_FOR_WAKEUP bit of RTC_CNTL_LOW_POWER_ST_REG register. If WAKE instruction is executed while RTC_CNTL_RDY_FOR_WAKEUP is zero, it has no effect (wake up does not occur).

1: is_rdy_for_wakeup:                   // Read RTC_CNTL_RDY_FOR_WAKEUP bit
          READ_RTC_FIELD(RTC_CNTL_LOW_POWER_ST_REG, RTC_CNTL_RDY_FOR_WAKEUP)
          AND r0, r0, 1
          JUMP is_rdy_for_wakeup, eq    // Retry until the bit is set
          WAKE                          // Trigger wake up
          REG_WR 0x006, 24, 24, 0       // Stop ULP timer (clear RTC_CNTL_ULP_CP_SLP_TIMER_EN)
          HALT                          // Stop the ULP program
          // After these instructions, SoC will wake up,
          // and ULP will not run again until started by the main program.



SLEEP (2 cycles to execute, 4 cycles to fetch next instruction)
-----
    SLEEP sleep_reg
      sleep_reg – 0..4, selects one of SENS_ULP_CP_SLEEP_CYCx_REG registers.
The instruction selects which of the SENS_ULP_CP_SLEEP_CYCx_REG (x = 0..4) register values is to be used by the ULP wakeup timer as wakeup period. By default, the value from SENS_ULP_CP_SLEEP_CYC0_REG is used.

1:        SLEEP     1         // Use period set in SENS_ULP_CP_SLEEP_CYC1_REG
2:        .set sleep_reg, 4   // Set constant
          SLEEP  sleep_reg    // Use period set in SENS_ULP_CP_SLEEP_CYC4_REG


WAIT (2 + Cycles cycles to execute, 4 cycles to fetch next instruction)
-----
    WAIT Cycles
      Cycles – number of cycles for wait
The instruction delays for given number of cycles.

1:        WAIT     10         // Do nothing for 10 cycles
2:        .set  wait_cnt, 10  // Set a constant
          WAIT  wait_cnt      // wait for 10 cycles


TSENS – do measurement with temperature sensor
-----
    TSENS Rdst, Wait_Delay
      Rdst – Destination Register R[0..3], result will be stored to this register
      Wait_Delay – number of cycles used to perform the measurement

Cycles
    2 + Wait_Delay + 3 * TSENS_CLK to execute, 4 cycles to fetch next instruction
The instruction performs measurement using TSENS and stores the result into a general purpose register.

1:        TSENS     R1, 1000     // Measure temperature sensor for 1000 cycles,
                                 // and store result to R1


ADC – do measurement with ADC
-----
    ADC Rdst, Sar_sel, Mux
      Rdst – Destination Register R[0..3], result will be stored to this register
      Sar_sel – Select ADC: 0 = SARADC1, 1 = SARADC2
      Mux - selected PAD, SARADC Pad[Mux+1] is enabled

Cycles
    23 + max(1, SAR_AMP_WAIT1) + max(1, SAR_AMP_WAIT2) + max(1, SAR_AMP_WAIT3) + SARx_SAMPLE_CYCLE + SARx_SAMPLE_BIT cycles to execute, 4 cycles to fetch next instruction

The instruction makes measurements from ADC.
ADC1 (GPIOs 32-39), and ADC2 (GPIOs 0, 2, 4, 12-15, 25-27)

1:        ADC      R1, 0, 1      // Measure value using ADC1 pad 2 and store result into R1

```
ADC1 ch0  GPIO36
ADC1 ch1  GPIO37
ADC1 ch2  GPIO38
ADC1 ch3  GPIO39
ADC1 ch4  GPIO32
ADC1 ch5  GPIO33
ADC1 ch6  GPIO34
ADC1 ch7  GPIO35

ADC2 ch0  GPIO4
ADC2 ch1  GPIO0
ADC2 ch2  GPIO2
ADC2 ch3  GPIO15
ADC2 ch4  GPIO13
ADC2 ch5  GPIO12
ADC2 ch6  GPIO14
ADC2 ch7  GPIO27
ADC2 ch8  GPIO25
ADC2 ch9  GPIO26
```

I2C_RD - read single byte from I2C slave
-----
    I2C_RD Sub_addr, High, Low, Slave_sel
      Sub_addr – Address within the I2C slave to read.
      High, Low — Define range of bits to read. Bits outside of [High, Low] range are masked.
      Slave_sel - Index of I2C slave address to use.

Cycles
    Execution time mostly depends on I2C communication time. 4 cycles to fetch next instruction.

I2C_RD instruction reads one byte from I2C slave with index Slave_sel. Slave address (in 7-bit format) has to be set in advance into SENS_I2C_SLAVE_ADDRx register field, where x == Slave_sel. 8 bits of read result is stored into R0 register.

1:        I2C_RD      0x10, 7, 0, 0      // Read byte from sub-address 0x10 of slave with address set in SENS_I2C_SLAVE_ADDR0


I2C_WR - write single byte to I2C slave
-----
    I2C_WR Sub_addr, Value, High, Low, Slave_sel
      Sub_addr – Address within the I2C slave to write.
      Value – 8-bit value to be written.
      High, Low — Define range of bits to write. Bits outside of [High, Low] range are masked.
      Slave_sel - Index of I2C slave address to use.

Cycles
    Execution time mostly depends on I2C communication time. 4 cycles to fetch next instruction.

I2C_WR instruction writes one byte to I2C slave with index Slave_sel. Slave address (in 7-bit format) has to be set in advance into SENS_I2C_SLAVE_ADDRx register field, where x == Slave_sel.

1:        I2C_WR      0x20, 0x33, 7, 0, 1      // Write byte 0x33 to sub-address 0x20 of slave with address set in SENS_I2C_SLAVE_ADDR1.


REG_RD – read from peripheral register
-----
    REG_RD Addr, High, Low
      Addr – register address, in 32-bit words
      High – High part of R0
      Low – Low part of R0

Cycles
    4 cycles to execute, 4 cycles to fetch next instruction


The instruction reads up to 16 bits from a peripheral register into a general purpose register: R0 = REG[Addr][High:Low].

This instruction can access registers in RTC_CNTL, RTC_IO, SENS, and RTC_I2C peripherals. Address of the the register, as seen from the ULP, can be calculated from the address of the same register on the DPORT bus as follows:

    addr_ulp = (addr_dport - DR_REG_RTCCNTL_BASE) / 4

1:        REG_RD      0x120, 2, 0     // load 4 bits: R0 = {12'b0, REG[0x120][7:4]}


`REG_WR` – write to peripheral register
-----
    REG_WR Addr, High, Low, Data
      Addr – register address, in 32-bit words.
      High – High part of R0
      Low – Low part of R0
      Data – value to write, 8 bits

Cycles
    8 cycles to execute, 4 cycles to fetch next instruction

The instruction writes up to 8 bits from a general purpose register into a peripheral register. REG[Addr][High:Low] = data

This instruction can access registers in RTC_CNTL, RTC_IO, SENS, and RTC_I2C peripherals. Address of the the register, as seen from the ULP, can be calculated from the address of the same register on the DPORT bus as follows:

    addr_ulp = (addr_dport - DR_REG_RTCCNTL_BASE) / 4

1:        REG_WR      0x120, 7, 0, 0x10   // set 8 bits: REG[0x120][7:0] = 0x10
