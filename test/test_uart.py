import cocotb
from cocotb.triggers import Timer


CLOCKS_PER_BIT = 434


async def tick(dut, expected=None):
    dut.clk.value = 0
    await Timer(10, unit="ns")
    dut.clk.value = 1
    await Timer(10, unit="ns")
    if expected is not None:
        assert int(dut.uo_out.value) == expected
    assert int(dut.uio_out.value) == 0
    assert int(dut.uio_oe.value) == 0


async def reset(dut):
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await tick(dut, 1)
    dut.rst_n.value = 1
    await tick(dut, 1)


@cocotb.test()
async def frames_and_requests(dut):
    await reset(dut)
    for byte in (0x00, 0xFF, 0x55, 0xA6):
        dut.ui_in.value = byte
        dut.uio_in.value = 1
        await tick(dut, 2)
        bits = [0] + [(byte >> bit) & 1 for bit in range(8)] + [1]
        dut.ui_in.value = byte ^ 0xFF
        for bit_index, bit in enumerate(bits):
            for cycle in range(CLOCKS_PER_BIT):
                if bit_index == 2:
                    dut.uio_in.value = int(cycle == 1)
                if bit_index == 8:
                    dut.uio_in.value = 1
                if cycle == CLOCKS_PER_BIT - 1:
                    expected = (2 | bits[bit_index + 1]) if bit_index < 9 else 1
                else:
                    expected = 2 | bit
                await tick(dut, expected)
        for _ in range(4):
            await tick(dut, 1)
        dut.uio_in.value = 0
        await tick(dut, 1)


@cocotb.test()
async def reset_aborts_frame_and_enable_gates_requests(dut):
    await reset(dut)
    dut.ena.value = 0
    dut.uio_in.value = 1
    await tick(dut, 1)
    dut.ena.value = 1
    await tick(dut, 1)
    dut.uio_in.value = 0
    await tick(dut, 1)
    dut.ui_in.value = 0xFF
    dut.uio_in.value = 1
    await tick(dut, 2)
    dut.ena.value = 0
    dut.uio_in.value = 0
    for _ in range(CLOCKS_PER_BIT):
        await tick(dut)
    assert int(dut.uo_out.value) == 3
    await reset(dut)
    dut.uio_in.value = 1
    await tick(dut, 2)
