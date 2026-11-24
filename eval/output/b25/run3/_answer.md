Created the [b25 project]( /home/andreferraz/EDA_Agent/eval/output/b25/run3/b25.kicad_pro) and its [schematic]( /home/andreferraz/EDA_Agent/eval/output/b25/run3/b25.kicad_sch).

The schematic includes the four passive lane pairs, separate bypassed activity-supply links, selectable sideband links, CLKREQ strap, and reset, wake and presence test pads. Alternative links are marked with assembly options.

**Before building:** the specified OCuLink interface has no reference-clock connection, so compatible independent clocking is required. The two project-local connector symbols need pinout verification, and connector footprints remain unassigned.

ERC reported **0 errors and 16 symbol-library mismatch warnings**.