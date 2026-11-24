Created the [b36 schematic](./b36.kicad_sch) and project. It includes the requested regulator, protection, filtering, four feedback-selection bridges, status LED, test pad, mounting holes and logo.

**This is a draft, not a build-ready 5.5–36 V, 3 A design:**

- The requested AO3401A is rated for 30 V drain-to-source, so it is unsuitable for a 36 V input. **Do not apply 36 V.**
- The supplied barrel-jack footprint describes a 2.5 A connector. Its pinout, the inductor’s peak-current capability, and thermal performance need verification.
- The polyfuse is specified but has no selected part or footprint. Output-capacitor ESR and loop stability also need validation.
- A buck converter cannot regulate 12 V from a 5.5 V input. The input must exceed the selected output by the required dropout margin.

Close **exactly one** solder bridge before powering the circuit. ERC reported **0 errors and 33 warnings**, primarily symbol-library mismatch warnings. The schematic passed structural and legibility checks.