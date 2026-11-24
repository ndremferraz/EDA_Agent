Created the [b30 KiCad project](./b30.kicad_pro) and its [schematic](./b30.kicad_sch). The requested interfaces, power rails, LIN master pull-up, ISP, buzzer, panel inputs, and test pads are connected.

**Checks:** ERC reports 0 errors and 29 symbol-library mismatch warnings. The netlist was checked against the requested pin assignments.

**Assumptions and review before building:**
- Panel inputs are active-low; external RX/TX use 5 V logic and should be isolated during ISP programming.
- The HT7550-1 symbol was created locally. **Check its pinout against the selected package** before assembly.
- The supplied MCP2003B symbol was retained, with RXD/TXD electrical types corrected.
- Qualify the 24 V transient protection for the actual supply: the SMBJ24A’s worst-case clamp can exceed the 7812 input rating.