Created the [b35 KiCad project](./b35.kicad_pro) and [schematic](./b35.kicad_sch). The requested power path, interfaces, headers, test pads, LEDs, crystal, and alternate-variant jumper are wired.

**Assumptions and checks:**
- Assumed a protected 1-cell LiPo suitable for approximately **196 mA** charging, using a 5.1 kΩ programming resistor.
- The switched 3.3 V output is active-low on P1.09 and defaults on.
- The supplied TP4057 symbol had no pin number for PROG. I created a corrected project-local symbol; **check its pinout against the selected charger datasheet**.
- ERC reports **0 errors and 39 warnings**, including library-symbol mismatches and an unresolved solder-jumper footprint. Resolve those warnings before using the design.

No PCB layout or manufacturing files were created.