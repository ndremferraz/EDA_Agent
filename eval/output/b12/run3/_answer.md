Created the [b12 KiCad project]( /home/andreferraz/EDA_Agent/eval/output/b12/run3/b12.kicad_pro ) and its [schematic]( /home/andreferraz/EDA_Agent/eval/output/b12/run3/b12.kicad_sch ).

The schematic includes the requested MOSFET, Schottky diode, 10 kΩ pull-down and five solder pads. The two ground pads share a net. The charger and battery protection are external.

Assumed a 5 V charger input and a protected single Li-ion cell. The load voltage is **unregulated**, and the input supply must accommodate both charging and load current.

ERC found **0 errors and 6 symbol-library mismatch warnings**.