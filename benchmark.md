
### KiCAD EDA Agent Benchmark

## Benchmark Data Gathering 
To ensure that the benchmark was alligned with realistic KiCAD project expectations, I manually selected Github projects that I deemed suitable for me goals. 
The following are all the github repositories that were selected:

- https://github.com/electron271/tuxkeychain.git
- https://github.com/siderakb/mdbt-micro.git
- https://github.com/CDFER/NIMRS-21Pin-Decoder.git
- https://github.com/protolux-electronics/soleil_hardware.git
- https://github.com/RemiFM/USB-LiDAR-VL53L9.git  
- https://github.com/tjko/tiny-picoprobe.git
- https://github.com/cajunpanda/gameboy-hifi-audio.git 
- https://github.com/Jana-Marie/CH330_Hardware.git  
- https://github.com/valletw/esp-atx-power.git  
- https://github.com/BenjaminSoelberg/elektronika-1.git
- https://github.com/luni64/USB-C---MicroB.git 
- https://github.com/badjeff/paw3222-pcb.git 
- https://github.com/Nurgak/Internet-of-Things-Power-Meter.git
- https://github.com/nu31hackerspace/prismo.git
- https://github.com/fadushin/solar-esp32.git
- https://github.com/badjeff/paw3395-pcb.git
- https://github.com/M4a1x/TPS5430.git 
- https://github.com/DoImant/TP4056-Power-Path-PCB.git 
- https://github.com/RonMcKay/capacitive-soil-moisture-sensor.git
- https://github.com/hackup/Pi1541io.git
- https://github.com/sszczep/Cherry-MX-Breakout-Board.git 
- https://github.com/tops4u/Ram-Tester.git 
- https://github.com/scottbez1/smartknob.git
- https://github.com/staticintlucas/goldfish.git 
- https://github.com/bbogush/nand_programmer.git 
- https://github.com/raeedcho/temper.git 
- https://github.com/OpenDrone-hw/OpenRX-Gemini.git
- https://github.com/OpenDrone-hw/OpenRX-Mono.git  
- https://github.com/OpenDrone-hw/OpenRX-Lite-UFL.git
- https://github.com/OpenDrone-hw/OpenRX-Lite.git
- https://github.com/cardonabits/haxo-hw.git
- https://github.com/gcormier/megadesk.git
- https://github.com/tzarc/keyboards.git 
- https://github.com/siderakb/pmw3360-pcb.git 
- https://github.com/OLIMEX/UEXT-CH390.git
- https://github.com/antmicro/ftdi-toolkit.git
- https://github.com/antmicro/m2-oculink-adapter.git
- https://github.com/OLIMEX/BB-LVL-SHIFT.git
- https://github.com/FrameworkComputer/ExpansionCards.git



## License Assesment Report 

I asked AI to make an assesment of which projects we would be able to include in our benchmark based on their licenses.

- BB-LVL-SHIFT -> hardware license: CERN-OHL-S-2.0 (`README.md`); eligible: yes, with reciprocal terms and retained silkscreen credits. Root `LICENSE` is MIT, but the README specifically assigns the hardware to CERN-OHL-S.
- CH330_Hardware -> license: GPL-3.0 (`LICENSE`); eligible: yes, with GPL terms.
- Cherry-MX-Breakout-Board -> license: MIT (`LICENSE`); eligible: yes, retain notice.
- ExpansionCards -> license: CC BY 4.0 (`LICENSE`, `Electrical/README.md`); eligible: yes, with attribution.
- Internet-of-Things-Power-Meter -> hardware license: CC BY-SA 4.0 (`README.md`); eligible: yes, with attribution and share-alike for adaptations. Software is separately GPL.
- NIMRS-21Pin-Decoder -> license: MIT (`README.md`, `Decoder PCB/LICENSE`); eligible: yes, retain notice. The README states project-wide MIT, though the license file is under `Decoder PCB`.
- OpenRX-Gemini -> hardware license: CERN-OHL-S-2.0 (`README.md`, `LICENSE`); eligible: yes, with reciprocal terms.
- OpenRX-Lite -> hardware license: CERN-OHL-S-2.0 (`README.md`, `LICENSE`); eligible: yes, with reciprocal terms.
- OpenRX-Lite-UFL -> hardware license: CERN-OHL-S-2.0 (`README.md`, `LICENSE`); eligible: yes, with reciprocal terms.
- OpenRX-Mono -> hardware license: CERN-OHL-S-2.0 (`README.md`, `LICENSE`); eligible: yes, with reciprocal terms.
- Pi1541io -> license: CC BY-SA 4.0 (`README.md`, `LICENSE`); eligible: yes, with attribution and share-alike for adaptations.
- Ram-Tester -> hardware license: CERN-OHL-S-2.0 (`LICENSE`); eligible: yes, with reciprocal terms. Firmware is separately GPL-3.0-or-later.
- TP4056-Power-Path-PCB -> license: CC BY-SA 4.0 (`LICENSE.md`); eligible: yes, with attribution and share-alike for adaptations.
- TPS5430 -> license: CERN-OHL-S-2.0 (`README.md`, `LICENSE`); eligible: yes, with reciprocal terms.
- UEXT-CH390 -> hardware license: CERN-OHL-S-2.0 (`README.md`); eligible: yes, with reciprocal terms and retained silkscreen credits. Root `LICENSE` is MIT, but the README specifically assigns the hardware to CERN-OHL-S.
- USB-C---MicroB -> license: MIT (`LICENSE`); eligible: yes, retain notice.
- USB-LiDAR-VL53L9 -> license: MIT (`LICENSE`); eligible: yes, retain notice.
- capacitive-soil-moisture-sensor -> hardware license: CERN-OHL-P-2.0 (`COPYRIGHT.TXT`, `README.md`); eligible: yes, retain notices.
- elektronika-1 -> license: GPL-3.0 (`LICENSE`); eligible: yes, with GPL terms.
- esp-atx-power -> license: MIT (`LICENSE`); eligible: yes, retain notice.
- ftdi-toolkit -> license: Apache-2.0 (`LICENSE`, `README.md`); eligible: yes, retain notices.
- gameboy-hifi-audio -> hardware license: CERN-OHL-P-2.0 (`hardware/LICENSE`, `README.md`); eligible: yes, retain notices. Root MIT and documentation CC BY 4.0 apply to other parts.
- goldfish -> license: CC BY-SA 4.0 (`README.md`); eligible: yes, with attribution and share-alike for adaptations. No standalone license file, but the README contains an explicit grant.
- haxo-hw -> hardware license: CC BY-SA 4.0 (`LICENSE`); eligible: yes, with attribution and share-alike for adaptations.
- keyboards -> hardware license: CERN-OHL-S-2.0 (root and per-keyboard `LICENSE` files); eligible: yes, with reciprocal terms. Bundled `reversible-kicad` has its own CC0 notice.
- m2-oculink-adapter -> license: Apache-2.0 (`LICENSE`, `README.md`); eligible: yes, retain notices.
- mdbt-micro -> license: MIT (`LICENSE`); eligible: yes, retain notice.
- megadesk -> license: GPL-3.0 (`LICENSE`); eligible: yes, with GPL terms.
- nand_programmer -> hardware license: GPL-3.0 (`README.md`, `LICENSE.txt`); eligible: yes, with GPL terms.
- paw3222-pcb -> license: CERN-OHL-P-2.0 (`LICENSE`, `README.md`); eligible: yes, retain notices.
- paw3395-pcb -> license: CERN-OHL-P-2.0 (`LICENSE`, `README.md`); eligible: yes, retain notices.
- pmw3360-pcb -> KiCad files license: CERN-OHL-P-2.0 (`README.md`, `LICENSE-CERN-OHL-P`); eligible: yes, retain notices. Firmware has different licenses.
- prismo -> license: MIT (`LICENSE`, `README.md`); eligible: yes, retain notice.
- smartknob -> electronics license: Apache-2.0 (`README.md`, `LICENSE.txt`); eligible: yes, retain notices. Mechanical files are separately CC BY 4.0.
- solar-esp32 -> license text: BSD-3-Clause (`LICENSE`); eligible: yes, retain notice and avoid endorsement. The file calls itself “BSD License 2.0” but contains the third non-endorsement clause, and the README links to BSD-3-Clause.
- soleil_hardware -> license: CERN-OHL-P-2.0 (`LICENSE`); eligible: yes, retain notices.
- temper -> license: CERN-OHL-P-2.0 (`LICENSE`); eligible: yes, retain notices.
- tiny-picoprobe -> license: GPL-3.0 (`LICENSE`); eligible: yes, with GPL terms.
- tuxkeychain -> license: CC BY-SA 4.0 (`LICENSE`); eligible: yes, with attribution and share-alike for adaptations.

License interpretation references: [Creative Commons BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/), [Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), [CERN OHL license variants](https://ohwr.org/licences/), [BSD 3-Clause text](https://opensource.org/license/bsd-3-clause).

### Excluded source

`rfm9x_breakout_board` was removed from `sources.txt` and the Task 1 and Task 2 repository lists. Its `README.md` licenses the design under CC BY-NC 4.0, which restricts commercial use; the benchmark may permit commercial use. It has two KiCad project files and no project or KiCad dependency triggered script was identified in the static Task 1 review. Its local clone remains present for reference.
