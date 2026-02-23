TOPLEVEL_LANG = verilog
SIM = icarus
VERILOG_SOURCES = $(PWD)/rtl/mul.v
TOPLEVEL = mul
MODULE = test_mul
export WAVES = 1
include $(shell cocotb-config --makefiles)/Makefile.sim
