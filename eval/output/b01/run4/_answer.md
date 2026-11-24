Created the [b01 project](./b01.kicad_pro) and [schematic](./b01.kicad_sch). The supplied Cherry MX RGB symbol and Kailh-socket footprint are connected to a 6-pin, 2.54 mm header, with a 100 nF capacitor across the symbol’s VCC and GND pins.

The design assumes the host supplies the switch pull-up and debounce. **Verify the LED pinout, supply voltage and drive requirements against the actual part before assembly**; the schematic follows the supplied symbol’s pin names.

ERC reported **0 errors and 8 warnings**: six connection-grid warnings and two library-symbol mismatch warnings. The generated netlist confirms all six header connections.