import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_mul_basic(dut):
    """Minimal test: drive inputs and read product."""
    dut.mc.value = 14
    dut.mp.value = 10
    await Timer(10, unit="ns")
    assert int(dut.p.value) == 140, f"expected 140, got {int(dut.p.value)}"

    dut.mc.value = 10
    dut.mp.value = 0xF6  # 246 unsigned, -10 signed
    await Timer(10, unit="ns")
    assert int(dut.p.value) == 2460, f"expected 2460, got {int(dut.p.value)}"
