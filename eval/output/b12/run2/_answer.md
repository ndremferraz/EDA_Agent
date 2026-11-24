Created the [b12 KiCad project]( /home/andreferraz/EDA_Agent/eval/output/b12/run2/b12.kicad_pro ) and its [schematic]( /home/andreferraz/EDA_Agent/eval/output/b12/run2/b12.kicad_sch ).

The schematic includes the requested MOSFET, Schottky diode, 10 kΩ pull-down, and five solder connections. The two ground connections share a net; the charger and battery protection remain external.

**Assumptions:** The charger input is regulated at 5 V, and the protected single-cell battery connects to OUT+. The load voltage is unregulated. Check diode and MOSFET thermal limits for the intended load current.

ERC reported **0 errors and 6 warnings**, all concerning embedded symbols differing from their library copies.