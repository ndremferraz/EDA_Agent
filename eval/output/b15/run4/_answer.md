Created the [b15 KiCad project](./b15.kicad_pro) and its [schematic](./b15.kicad_sch).

The template uses the supplied Framework plug footprint, a 5.1 kΩ CC sink resistor, an always-enabled AP2112K-3.3 with 10 µF input and output capacitors, two M2 unplated mounting holes, and four grounded test pads. USB D+ and D− are named stubs; no peripheral is fitted.

**Verification:** ERC reports no errors and 13 warnings: two intentional single-pin USB stub labels and 11 symbol-library mismatch warnings. The mismatch warnings remained after refreshing the embedded symbols.

Assumed a 5 V VBUS supply. Select ceramic capacitors that retain adequate capacitance under DC bias.