Created the [led_notes project](led_notes.kicad_pro) and [schematic](led_notes.kicad_sch).

The netlist confirms J1 pin 1 → R1 (300 Ω) → LED anode, and LED cathode → J1 pin 2 (GND). ERC reports **0 errors and 0 warnings**.

Assumptions: a typical red LED with approximately 2 V forward voltage gives about 10 mA. Use a resistor rated at least 0.125 W, and verify the selected LED matches the assigned 0603 footprint.