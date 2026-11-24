Created the [5 V to 3.3 V regulator schematic](./regulator_5v_3v3.kicad_sch). It uses an AP2112K-3.3 with input and output capacitors and two-pin connectors. ERC reports **0 violations**.

The regulator is rated for up to 600 mA, but the usable current depends on PCB thermal design. Project-local symbols were created; their pinouts should be checked against the datasheet. Footprint availability could not be verified in this environment.

I could not order or pay for the 10 assembled boards. No PCB layout or manufacturing files were created, so the design is not yet ready to order.