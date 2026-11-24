Created the **b31** project and [schematic](./b31.kicad_sch). It includes the requested buck charger, sensing dividers, LEDs, supervisor, filtering and connector pin ordering.

**Before building:** the controller compensation, MPPT threshold and charge-current assumptions need datasheet verification. The newly created DMP1045U-7 and APX803L-29SA-7 symbols also need their pinouts checked. The supervisor signals reset; it does **not** disconnect the battery rail. That rail is unregulated, so check the external ESP32’s voltage limits and use suitable cell protection.

ERC reported **0 errors and 29 symbol-library mismatch warnings**.