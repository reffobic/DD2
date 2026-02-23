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

## Create a new repo on GitHub

**Are you signed in to GitHub?**  
Open [github.com](https://github.com) in your browser. If you see your profile picture and your username in the top-right, you’re signed in. If not, sign in (or create an account), then come back here.

**Create the repo and push this project:**

1. Go to [github.com/new](https://github.com/new).
2. Pick a **Repository name** (e.g. `rtl-verification` or `DD2`).
3. Choose **Public**.
4. Leave **“Add a README”** and **“Add .gitignore”** unchecked (this project already has them).
5. Click **Create repository**.
6. In your project folder, run (use your username and repo name):

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

   If you use SSH:

   ```bash
   git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```

   When you push, the browser may ask you to sign in or use a personal access token; follow the prompts.
