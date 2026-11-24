Created the [b28 KiCad project](./b28.kicad_pro) and its [schematic](./b28.kicad_sch), using the supplied castellated and USB-C footprints. The requested header orders and USB, power, reset, clock and bypass connections are present.

**Checks and limitations:**
- ERC reports **0 errors and 25 symbol-library mismatch warnings**.
- Created project-local ATmega32U4-MU and USB-C receptacle symbols. Their pinouts, including the MCU exposed pad, should be checked against the selected parts before manufacture. Standard footprints could not be verified in this environment.
- The 16 MHz design assumes an 18 pF-load crystal and approximately 4.5 pF stray capacitance per side.
- VCC is unregulated and diode-fed. Fuse and diode drops can take it below the **4.5 V minimum for 16 MHz operation**; check the voltage budget at the intended load.