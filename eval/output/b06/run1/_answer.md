Created the [b06 KiCad project](./b06.kicad_pro) and its [schematic](./b06.kicad_sch). The target header, separate VSYS and VBUS connections, Pico grounds, and optional green LED with 5 kΩ resistor are wired.

ERC reports **0 errors and 3 warnings**: the resistor, LED, and connector symbols differ from the installed library copies.

The Pico module symbol was created locally. **Check its pinout and SWD contact numbering before use**; SWD pins 41–43 are local conventions. No Pico footprint is assigned. The design assumes a 3.3 V target; avoid backfeeding VSYS or VBUS.