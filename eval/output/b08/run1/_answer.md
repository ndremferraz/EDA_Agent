Created the [b08 KiCad schematic](sandbox:/home/andreferraz/EDA_Agent/eval/output/b08/run1/b08.kicad_sch) with the requested passive connections. The card-detect contacts are unused, and headphone common is separate from GND.

**Before use:** J3 has no footprint assigned; select a TRRS jack and verify its contact-to-pad mapping. Also verify that the supplied FFC footprint’s mounting pad is numbered `MP`.

ERC reports **0 errors and 6 symbol-library mismatch warnings**. The design assumes the host supplies power and the SD/I²C pull-ups; the expansion headers use 2.54 mm pitch.