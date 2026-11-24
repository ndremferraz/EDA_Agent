Created the [b38 project](./b38.kicad_pro) and its [schematic](./b38.kicad_sch). The custom DIP and ZIP socket symbols are in [b38_symbols.kicad_sym](./b38_symbols.kicad_sym); check their pinouts against the actual sockets and DRAM before assembly.

The netlist check confirms the requested mappings, series resistors, switch options, LED drivers, reset, ICSP and power connections. ERC reported **0 errors and 40 warnings**, including symbol-library mismatch warnings.

**Before building:**
- PC5 powers the DRAM directly; verify that the selected DRAM’s current and startup load are within the MCU’s limits.
- Never drive A2, A3 or PC5 low while its corresponding switch is on. Fit only one DRAM at a time.
- J1 assumes an external two-contact Micro-USB power module. Select matching footprints for the polyfuse, LED and both sockets.
- The 16 MHz crystal uses assumed 22 pF load capacitors; verify them against the selected crystal.