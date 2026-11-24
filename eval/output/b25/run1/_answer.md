Created the [b25 KiCad project](file:///home/andreferraz/EDA_Agent/eval/output/b25/run1/b25.kicad_pro) and its schematic.

The schematic carries all four PCIe lane pairs, includes the requested 3.3 V links and bypass capacitors, alternative control-signal links, CLKREQ# strap, and reset, wake and presence test pads. The OCuLink 5 V contacts are unpowered.

**Before use:**
- R5, R6, R8 and R10 are marked DNP in their values and assembly notes; select the appropriate stuffing option.
- M.2 contacts 53/55 are REFCLK+/− on a standard host. The root-port stuffing option requires compatible reassigned contacts; verify clocking and AC coupling for the intended system.
- The M.2 and OCuLink symbols were created locally. **Check their pinouts**, select matching connector footprints, and verify the OCuLink shield-pad mapping. Connector footprints are not assigned.

ERC reported **0 errors and 16 symbol-library mismatch warnings**.