Created the [b12 KiCad project](./b12.kicad_pro) and its [schematic](./b12.kicad_sch).

The schematic includes the requested MOSFET, Schottky diode, 10 kΩ pull-down, and five individual solder connections. Both ground connections share a net. The charger and battery protection remain external.

**Assumptions:** nominal 5 V charger input and a protected single-cell battery. The load output is unregulated. Check the diode’s current and thermal limits for the intended load.

ERC reports **0 errors and 6 symbol-library mismatch warnings** for the resistor and solder-pad symbols.