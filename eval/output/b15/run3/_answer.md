Created the **b15** project and [schematic](./b15.kicad_sch). It includes the supplied Framework plug footprint, always-enabled 3.3 V regulator, CC resistor, capacitors, two M2 holes, four grounded pads, and named USB data stubs.

**Verification:** ERC reports 0 errors and 13 warnings: two are for the intentionally single-pin USB data stubs; eleven report embedded-symbol differences from the installed libraries. Standard footprint lookup was unavailable, so the non-plug footprint assignments should be checked in KiCad.

**Assumptions:** VBUS is 5 V, the connector shield is grounded, and any future load must respect the host’s available current and regulator thermal limits. No USB peripheral or PCB layout was added.