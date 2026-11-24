Created the [b01 KiCad project](./b01.kicad_pro) and [schematic](./b01.kicad_sch), using the supplied Cherry MX RGB symbol and Kailh-socket footprint.

The header breaks out GND, LED DIN, LED DOUT, +5 V, SW1 and SW2. A 100 nF decoupling capacitor is included. The design assumes an external controller supplies power and switch bias; verify the LED pinout and supply voltage against the selected LED’s datasheet before powering it.

ERC reports **0 errors and 8 warnings**: six off-grid pin warnings and two library-symbol mismatch warnings. The standard header and capacitor footprints could not be verified in the available footprint libraries.