Created the [b28 KiCad project](./b28.kicad_pro) and its [schematic](./b28.kicad_sch). The requested header pin orders, USB protection and power path are connected; no 3.3 V regulator is fitted.

ERC reports **0 errors and 25 warnings**: 24 library-symbol mismatch warnings and one for the grounded bidirectional HWB pin. Standard footprint availability could not be independently verified with the footprint lookup tool.

**Design checks before building:**
- Diode and fuse voltage drop can bring VCC below the ATmega’s 4.5 V minimum for 16 MHz operation.
- The 22 pF crystal capacitors are provisional; select them for the chosen crystal and PCB stray capacitance.