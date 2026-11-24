Created the [b10 KiCad project](./b10.kicad_pro) and its [schematic](./b10.kicad_sch).

The passive adapter includes the DIP-20 plug, both SOJ socket interfaces, and separate 2.54 mm ZIP rows, wired to the requested mapping. All sockets share the tester nets; **test one device at a time**.

ERC reports **0 errors and 7 symbol-library mismatch warnings**. The SOJ socket footprints remain unassigned pending selection of the actual sockets; verify the assumed DIP plug and ZIP-row footprints against the hardware.