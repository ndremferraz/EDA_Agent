Created the [b32 KiCad project](./b32.kicad_pro) and [schematic](./b32.kicad_sch). The requested interfaces and pin assignments are wired, using the supplied flash symbol and card footprints.

**Checks:** ERC reports 0 errors and 32 symbol-library mismatch warnings. The schematic passed structural validation.

The USB-C connection is treated as a plug, with one CC pull-down; the 2×6 header exposes raw VBUS. Drive PA18 low before disabling LED power. A project-local **TLV70036DDC** symbol was created; check its pinout against the selected part’s datasheet before fabrication.