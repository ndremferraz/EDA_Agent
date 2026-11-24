Created the [b31 KiCad project](./b31.kicad_pro) and [schematic](./b31.kicad_sch), using the supplied CN3801 symbol and local footprint library.

**The schematic is preliminary, not construction-ready.** The CN3801 application circuit, compensation and component ratings still need datasheet verification. The project-local DMP1045U-7 and APX803L symbols were created for this design; check their pinouts and the supervisor part suffix against their datasheets.

ERC reports **0 errors and 31 symbol-library mismatch warnings**. The supervisor drives the external active-low reset; it does not disconnect the battery. The ESP32 receives the unregulated battery rail directly, so verify that its supply tolerates the fully charged cell voltage.