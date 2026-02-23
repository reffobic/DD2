# RTL Verification (Open-Source)

Tutorial 1: RTL verification using Icarus Verilog and cocotb.

## Layout

```
.
├── rtl/           # RTL (mul.v, counter.v)
├── tb/            # Verilog testbenches (mul_tb.v, counter_tb.v)
├── test_mul.py    # cocotb tests for multiplier
├── test_counter.py # cocotb tests for counter (Driver, Monitor, Scoreboard)
├── mul.f          # File list for iverilog (mul)
├── counter.f      # File list for iverilog (counter)
├── Makefile       # cocotb run for mul
└── Makefile.counter # cocotb run for counter
```

## Requirements

- Icarus Verilog (`iverilog`, `vvp`)
- Python 3 with venv
- cocotb (`pip install cocotb`), optionally `pytest` and `cocotb-test`

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install cocotb pytest cocotb-test
```

## Run

**Multiplier (Verilog TB only)**

```bash
iverilog -o mul.vvp -Wall -c mul.f && vvp mul.vvp
# Waveform: mul.vcd
```

**Multiplier (cocotb)**

```bash
make
```

**Counter (cocotb)**

```bash
make -f Makefile.counter
# Waveforms: sim_build/counter.fst
```

**Counter (Verilog TB, VCD for waveform viewer)**

```bash
iverilog -o counter.vvp -Wall -c counter.f && vvp counter.vvp
# Waveform: counter.vcd
```

## Waveforms

Open `.vcd` or `sim_build/*.fst` in a viewer (e.g. GTKWave or Surf).
