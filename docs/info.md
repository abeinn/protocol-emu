<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This milestone implements an 8N1 UART transmitter: one low start bit, eight data
bits sent least-significant bit first, and one high stop bit. TX idles high.
The original adder example remains in `src/project.v` but is excluded from the build.
This transmitter is a first step toward the programmable protocol emulator;
it does not yet include an instruction engine or a UART receiver.

| Pin | Function |
| --- | --- |
| `ui_in[7:0]` | Byte to transmit |
| `uio_in[0]` | Synchronous send request, sampled on a rising clock edge |
| `uo_out[0]` | UART TX |
| `uo_out[1]` | Busy, high for the entire ten-bit frame |
| `uo_out[7:2]` | Zero |
| `uio[7:0]` | Inputs; output enables and output data are zero |

Hold the byte stable when raising send. A rising edge on send is accepted only
when busy is low and `ena` is high. The byte is latched at acceptance; changes
to it during transmission have no effect. Send requests during busy are discarded,
not queued. Holding send high does not repeat a transmission. Lower send for at
least one clock before requesting another byte, and wait until busy is low.
Inputs must meet the clock's setup and hold requirements; this interface does not
synchronize asynchronous request signals.

The `CLOCKS_PER_BIT` Verilog parameter must be a positive integer. Its default is
434: at a 50 MHz input clock, the baud rate is approximately 115,207 (suitable for
115,200 baud). Every bit lasts exactly `CLOCKS_PER_BIT` clock cycles. To change
the baud rate, choose the nearest positive integer to `clock_hz / baud` and
rebuild; this parameter is not programmable after fabrication.

Reset is synchronous and active low. A clock edge with `rst_n=0` aborts any frame,
clears busy, and restores TX high. Keep send low when releasing reset unless a
new transmission is intended. Deasserting `ena` prevents new requests but lets
an accepted frame finish.

## How to test

Install Icarus Verilog, make, and Python with venv support. From the repository root:

```sh
python3 -m venv /tmp/protocol-emu-venv
. /tmp/protocol-emu-venv/bin/activate
pip install -r test/requirements.txt
cd test
make -B
```

The cocotb tests check every clock cycle of frames for `0x00`, `0xFF`, `0x55`, and
`0xA6`, including bit order, exact bit durations, the stop bit, busy, latched data,
requests while busy, held requests, enable gating, and reset during transmission.
The waveform is written to `test/tb.fst` (relative to the repository root).
On Windows, run these commands in Ubuntu under WSL2.

Gate-level simulation requires Icarus Verilog 13 or newer for the PDK's delayed
input models (RTL simulation works with version 12). Copy the generated netlist
to `test/gate_level_netlist.v`, set `PDK_ROOT` to the matching PDK installation,
and run `make -B GATES=yes` in `test/`. The gate-level build includes both the
standard-cell models and their UDP primitives.

## External hardware

Simulation requires no external hardware. For a hardware test, use a 50 MHz clock
and a voltage-compatible USB-to-UART adapter at 115,200 baud, 8N1. Connect TX to
the adapter's RX and share ground. Supply the byte and synchronous send request
using a host controller. Do not connect RS-232 voltage levels directly to the chip.
