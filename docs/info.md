## How it works

This is the CMOS5L starter for a programmable protocol emulator ASIC for the Jane Street competition. The protocol engine and instruction set are still to be designed.

The current template RTL is an 8-bit combinational adder: `uo_out = ui_in + uio_in`, with overflow discarded. The bidirectional pins are configured as inputs (`uio_oe = 0`), and their output values are tied to zero. The example does not use the clock, reset, or enable inputs. The pin descriptions in `info.yaml` describe this example and must be updated with the protocol engine.

The physical allocation is 6×4 tiles on IHP's 130 nm CMOS5L process. The 20 ns synthesis constraint in `src/config.json` is a template starting point; the operating frequency of the future protocol engine has not been selected.

## How to test

Run the cocotb testbench in `test/` with `make`, then check the results with `python -m cocotb_tools.check_results results.xml`. The existing test drives 20 and 30 on the two input buses and checks that the output is 50.

For a manual test of the current example, drive two 8-bit values on the dedicated and bidirectional inputs and read their sum modulo 256 from the dedicated outputs.

## External hardware

No external hardware is required for simulation. The eventual protocol interfaces and their electrical requirements are still to be specified.
