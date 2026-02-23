import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, NextTimeStep
from cocotb.clock import Clock
from cocotb.queue import Queue

def _safe_int(val):
    """Convert signal to int; use 0 if X/Z (e.g. at startup)."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

# --- Reference model: mirrors counter.v (rst, load, load_value, en) [§6.3 / §6.5] ---
class CounterModel:
    def __init__(self, width: int):
        self.width = width
        self.mask = (1 << width) - 1
        self.count = 0

    def step(self, rst: int, load: int, load_val: int, en: int) -> int:
        current = self.count
        if rst:
            self.count = 0  # [cite: 345]
        elif load:
            self.count = load_val  # [cite: 346]
        elif en:
            self.count = (self.count + 1) & self.mask  # [cite: 347, 242]
        return current


# --- Driver: drives DUT inputs aligned to clock [§6.3 / §6.5] ---
class CounterDriver:
    def __init__(self, dut):
        self.dut = dut

    async def reset(self, cycles: int = 2):
        self.dut.rst.value = 1
        self.dut.load.value = 0
        self.dut.en.value = 0
        for _ in range(cycles):
            await RisingEdge(self.dut.clk)
        self.dut.rst.value = 0
        await RisingEdge(self.dut.clk)
        await NextTimeStep()

    async def set_enable(self, en: int, cycles: int = 1):
        self.dut.en.value = int(en)
        self.dut.load.value = 0
        for _ in range(cycles):
            await RisingEdge(self.dut.clk)
        await NextTimeStep()

    async def set_load(self, load_value: int, cycles: int = 1):
        self.dut.en.value = 0
        self.dut.load.value = 1
        self.dut.load_value.value = load_value
        for _ in range(cycles):
            await RisingEdge(self.dut.clk)
        self.dut.load.value = 0
        await NextTimeStep()


# --- Monitor: observes DUT and pushes samples into queue [§6.3 / §6.5] ---
class CounterMonitor:
    def __init__(self, dut, out_queue: Queue):
        self.dut = dut
        self.q = out_queue
        self.cycle = 0

    async def run(self):
        while True:
            await RisingEdge(self.dut.clk)
            # Capture inputs at edge (before test can change them for next cycle)
            rst = _safe_int(self.dut.rst.value)
            load = _safe_int(self.dut.load.value)
            load_value = _safe_int(self.dut.load_value.value)
            en = _safe_int(self.dut.en.value)
            await ReadOnly()
            self.cycle += 1
            sample = {
                "cycle": self.cycle,
                "rst": rst,
                "load": load,
                "load_value": load_value,
                "en": en,
                "count": _safe_int(self.dut.count.value),  # count after this edge
            }
            await self.q.put(sample)


# --- Scoreboard: compares monitor output with reference model [§6.3 / §6.5] ---
class Scoreboard:
    def __init__(self, model: CounterModel, in_queue: Queue):
        self.model = model
        self.q = in_queue

    async def check_n_samples(self, n: int):
        for _ in range(n):
            s = await self.q.get()
            self.model.step(
                rst=s["rst"], load=s["load"], load_val=s["load_value"], en=s["en"]
            )
            expected = self.model.count  # new count after this edge
            got = s["count"]
            assert got == expected, (
                f"Mismatch at cycle {s['cycle']}: "
                f"rst={s['rst']} load={s['load']} en={s['en']} expected={expected} got={got}"
            )


@cocotb.test()
async def counter_demo_components(dut):
    """§6.5 Demo: clock + reset + driver + monitor + model + scoreboard (with load)."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    q = Queue()
    driver = CounterDriver(dut)
    monitor = CounterMonitor(dut, q)
    model = CounterModel(width=len(dut.count))
    scoreboard = Scoreboard(model, q)
    total = 0

    cocotb.start_soon(monitor.run())
    await driver.reset(cycles=2)  # 2 edges rst=1 + 1 edge rst=0 = 3 samples
    total += 3
    await driver.set_enable(en=0, cycles=5)
    total += 5
    await driver.set_enable(en=1, cycles=10)
    total += 10
    await driver.set_enable(en=0, cycles=3)
    total += 3
    dut.rst.value = 1
    await driver.set_enable(en=1, cycles=1)
    dut.rst.value = 0
    total += 1
    await driver.set_enable(en=1, cycles=4)
    total += 4
    await driver.set_load(load_value=100, cycles=1)
    total += 1
    await driver.set_enable(en=1, cycles=2)
    total += 2
    await scoreboard.check_n_samples(total)


@cocotb.test()
async def test_counter_load(dut):
    """Test load functionality: load 42, then assert count is 42."""
    # Clock and reset setup
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    dut.load.value = 0
    dut.load_value.value = 0
    dut.en.value = 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)

    # Test loading a value
    dut.load.value = 1
    dut.load_value.value = 42
    await RisingEdge(dut.clk)
    dut.load.value = 0

    # After one clock, the count should be 42
    await ReadOnly()  # Wait for signals to settle [cite: 273]
    assert int(dut.count.value) == 42, f"Expected 42, got {int(dut.count.value)}"


@cocotb.test()
async def test_counter_scoreboard(dut):
    """Drive rst/load/en and compare DUT count to reference model (scoreboard)."""
    model = CounterModel(width=8)
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    dut.load.value = 0
    dut.load_value.value = 0
    dut.en.value = 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    await ReadOnly()
    assert int(dut.count.value) == 0, f"After reset expected 0, got {int(dut.count.value)}"

    await NextTimeStep()  # leave ReadOnly so we can drive inputs
    # Cycle 1: enable count -> 1
    dut.en.value = 1
    model.step(0, 0, 0, 1)
    await RisingEdge(dut.clk)
    await ReadOnly()
    assert int(dut.count.value) == model.count, f"Expected {model.count}, got {int(dut.count.value)}"

    await NextTimeStep()
    # Cycle 2: load 100
    dut.en.value = 0
    dut.load.value = 1
    dut.load_value.value = 100
    model.step(0, 1, 100, 0)
    await RisingEdge(dut.clk)
    dut.load.value = 0
    await ReadOnly()
    assert int(dut.count.value) == model.count, f"After load expected {model.count}, got {int(dut.count.value)}"

    await NextTimeStep()
    # Cycle 3–4: count 101, 102
    dut.en.value = 1
    for _ in range(2):
        model.step(0, 0, 0, 1)
        await RisingEdge(dut.clk)
        await ReadOnly()
        assert int(dut.count.value) == model.count, f"Expected {model.count}, got {int(dut.count.value)}"
        await NextTimeStep()
