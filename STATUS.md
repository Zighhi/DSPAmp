# Proiect Disertatie - Project Status Report
**Project Name:** Amplificator audio multicanal cu procesor digital de semnal programabil  
**Author:** [Your Name]  
**Date:** March 23, 2026

## 1. Project Overview
This project involves the design and implementation of a multichannel audio amplifier with an integrated, real-time programmable digital signal processor (ADAU1701). The system includes balanced/unbalanced inputs, two gain stages, four balanced outputs, and four Class D power outputs.

## 2. Completed Milestones
- **[✅] Schematic Design:** The full circuit is completed in KiCad 9.0 (`hardware/DSPAmp.kicad_sch`).
- **[✅] Input Stage:** Balanced/unbalanced inputs with switchable gain (+4dBu / -10dBV).
- **[✅] Output Stage:** Four channels of balanced line-level outputs and four Class D power stages.
- **[✅] Power Supply:** 12V DC input with a virtual ground circuit (TL072) for single-rail op-amp operation.
- **[✅] Programmer Integration:** FreeUSBi-based programmer (CY7C68013A) integrated with I2C bus isolation (2N7000 MOSFETs).
- **[✅] Simulation:** All functional blocks have been simulated and verified using LTSpice.
- **[✅] Project Documentation:** Core dissertation requirements mapped and tracked in `docs/PROIECT_DISERTATIE.md`.

## 3. Current State
The project is currently in the **Procurement Phase**. The schematic is finalized, and a preliminary Bill of Materials (BOM) has been generated.

## 4. Pending Tasks (Immediate Actions)
- **[ ] Update BOM with Links:** The `DSPAmp(in).csv` file needs to be updated with direct Mouser/TME part numbers and purchase links.
- **[ ] Component Order:** Place the order for the remaining passive and active components (specifically the 5x OPA2134, 2N7000, and audio-grade capacitors).
- **[ ] Perfboard Layout Planning:** Map the completed schematic blocks to a physical perfboard layout.
- **[ ] Physical Implementation:** Begin soldering the modules and discrete components onto the perfboard.

## 5. Technical Notes
- **EEPROM Write Protect:** The WP pin on the ADAU1701 module will be permanently jumpered to GND for seamless flashing.
- **I2C Addressing:** The ADAU1701 is configured for 0x68 (7-bit) or 0xD0 (8-bit) addressing.
- **Mute Circuit:** Ensure the common `MUTE` net is correctly pulled to the active-state rail on the final physical build.
