# Protocol Emulator ASIC

Starter repository for the [Jane Street protocol emulator ASIC competition](https://blog.janestreet.com/protocol-emulator-asic-competition/), based on the [Tiny Tapeout CMOS5L Verilog template](https://github.com/TinyTapeout/ttihp-verilog-template/tree/cmos5l).

The RTL and testbench currently contain the template's example adder. The programmable protocol emulator is still to be designed.

## Build configuration

- Canonical branch: `main`. The original template snapshots are preserved in its merge history.
- Process: IHP 130 nm CMOS5L (`ihp-sg13cmos5l`).
- Allocation: 6×4 tiles, as required by the competition.
- Build actions: `TinyTapeout/tt-gds-action` at `ihp-cmos5l`.
- Support tools: `TinyTapeout/tt-support-tools` at `ihp-sg13cmos5l`.
- Local LibreLane: `3.1.0.dev3`, matching the build action.

Project metadata and source lists are in [info.yaml](info.yaml), with physical-design settings in [src/config.json](src/config.json). Update the title, author, clock frequency, top module, pin descriptions, and [design documentation](docs/info.md) as the design takes shape. When renaming `tt_um_example`, update both the RTL and `test/tb.v`, as well as `info.yaml`.

## Development and tests

Open this repository in its VS Code dev container for Icarus Verilog, Verilator, waveform viewers, and the Python toolchain. The support tools are copied to the ignored `tt/` directory on first startup. Installing the CMOS5L PDK is a separate step for local hardening; the GitHub GDS workflow installs it automatically.

To run the RTL test outside the container, install Icarus Verilog and Python, then:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r test/requirements.txt
cd test
make
python -m cocotb_tools.check_results results.xml
```

See [test/README.md](test/README.md) for gate-level simulation and waveform viewing.

## GitHub Actions

Pushes run RTL tests, documentation checks, and the GDS build with precheck and gate-level simulation. The FPGA workflow runs manually. The GDS viewer deploys using GitHub Pages; select **GitHub Actions** under **Settings → Pages → Source** in the repository if Pages is not already configured.

The project uses the [Apache 2.0 license](LICENSE).
