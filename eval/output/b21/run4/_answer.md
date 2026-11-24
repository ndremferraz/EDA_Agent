Created the **incomplete** project at [b21.kicad_pro](./b21.kicad_pro) and its [schematic](./b21.kicad_sch).

The MCU, crystal, battery holder, programming header, five button pads and display symbol are placed. The AS1115 is **not placed**: its footprint was supplied, but no symbol or verified pinout was available. The display segment and digit nets therefore remain undriven, and the 40 kΩ resistor is not connected to a driver. No display footprint was supplied, so its footprint is unassigned.

ERC reports **12 errors and 31 warnings**; the errors are the undriven display pins. This is not ready to build.

Assumptions in the partial design: button contacts switch to ground using firmware pull-ups; the crystal is 12.5 pF load with 18 pF capacitors; and the battery-side diode blocks programming power from charging the cell. Its voltage drop and the CR2032’s pulse-current capability need verification.