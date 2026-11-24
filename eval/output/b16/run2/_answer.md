Created the **b16** KiCad project and [schematic](./b16.kicad_sch). The display pin mapping, duplicate solder-pad pairs, bypass capacitors, backlight switch, and unconnected alignment-hole pad are wired as requested.

**Checks:** ERC reports 0 errors and 11 symbol-library mismatch warnings. One schematic note overlaps the title-block area.

**Assumptions:** The host supplies regulated 3.3 V and 3.3 V logic. Verify the display backlight’s forward voltage and current against the selected 22 Ω resistor before assembly. No custom symbols were needed.