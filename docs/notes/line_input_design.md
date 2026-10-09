# Line Input Stage Design Notes

This document provides design notes for creating unbalanced and balanced audio line input circuits, based on the principles outlined in Douglas Self's "Line Inputs" chapter.

## 1. Input Signal Levels & Goals

The primary goals of a line input stage are:
*   Provide a high and stable input impedance (typically > 10 kΩ) to avoid loading the source equipment.
*   Apply RF filtering at the very first point of entry to prevent electromagnetic interference (EMI) from being demodulated into the audio band.
*   Block any DC voltage from the source.
*   Provide appropriate gain or attenuation to match external signal levels to the system's internal nominal level.
*   For balanced inputs, provide high common-mode rejection (CMRR) to eliminate noise and hum from ground loops and interference.

**Nominal Line Levels (from Table 14.1):**
*   **Semi-professional (Unbalanced):** -10 dBV = 0.316 Vrms
*   **Professional (Balanced):** +4 dBu = 1.228 Vrms

## 2. Unbalanced Input Circuit Design

A robust unbalanced input requires a buffer amplifier to present a high, stable impedance. A simple unity-gain op-amp follower is often used.

### Unbalanced Circuit Example (based on Figure 14.1)

![Unbalanced Input Circuit](https://i.imgur.com/3yT6jZ2.png)
*(This is a conceptual representation of the circuit in Figure 14.1)*

```
      [IN+] ----R1---+---C2---+-------------------- |~| ----C3---+---- [OUT]
                     |        |                      | |        |
                     C1       R2 ---+-------------- |-|--+      R4
                     |        |     |              | |  |      |
                   [GND]      |     |              | |  |    [GND]
                              |     |              | |  |
                              |     `-------------- |+|-+
                              |                    | |
                              `---- R3 ----------- |~|
                                    |
                                  [GND]
```
*(Circuit ASCII art for context)*

### Component Functions:

*   **Op-Amp (U1A):** A low-noise op-amp like the **NE5532** is a good choice for low-impedance sources. It is configured as a non-inverting amplifier (here, a unity-gain follower).
*   **RF Input Filter (R1, C1):**
    *   Forms a low-pass filter to shunt RF interference to ground before it can reach the op-amp. **This must be placed as physically close to the input connector as possible.**
    *   Typical values: `R1 = 100 Ω`, `C1 = 100 pF`.
    *   The effectiveness of this filter is a compromise with the unknown output impedance of the source equipment. A high source impedance combined with C1 can cause an undesirable roll-off in the audio band.
*   **DC Blocking Capacitor (C2):**
    *   A non-polarized (NP) electrolytic capacitor (e.g., `22 µF, 35V NP`) prevents any DC from the source from entering the circuit and upsetting the op-amp's operating point.
*   **Input Impedance and Biasing (R2, R3):**
    *   The input impedance of the stage is primarily determined by `R2` and `R3`. In the reference diagram `R3` is a DC drain for `C2` and `R2` provides the bias current path for the op-amp. The total input impedance is `R3` in parallel with `R2`, which is `220 kΩ || 100 kΩ ≈ 68 kΩ`. This is a good high value.
*   **Output DC Blocking (C3, R4):**
    *   Even with no DC at the input, the op-amp's own input offset voltage will be present at its output. `C3` (`47 µF`) blocks this DC from reaching the next stage, while `R4` (`22 kΩ`) acts as a DC drain resistor.

## 3. Balanced Input Circuit Design

A balanced input uses a differential amplifier to subtract the "cold" signal from the "hot" signal. Any noise or hum that is identical on both lines (common-mode noise) is canceled out.

### Practical Balanced Circuit Example (based on Figure 14.7)

This circuit adds the necessary real-world components for RF immunity and DC blocking to a basic single-op-amp differential amplifier.

![Practical Balanced Input Circuit](https://i.imgur.com/u5jS5xU.png)
*(This is a conceptual representation of the circuit in Figure 14.7)*

### Component Functions:

*   **Differential Amplifier (U1, R1-R4):**
    *   The core of the circuit. The output is `(IN+ - IN-) * Gain`.
    *   Gain is set by `R2/R1` (assuming `R1=R3` and `R2=R4`). For unity gain, all four resistors are equal (e.g., `10 kΩ`).
    *   **Crucially, the CMRR is determined almost entirely by the matching of these four resistors.**
*   **RF Input Filters (R5/C3 and R6/C4):**
    *   Symmetrical RC low-pass filters are required on **both** the hot and cold inputs (`100 Ω`, `100 pF` each). Like the unbalanced circuit, these must be located directly at the input XLR connector pins.
*   **DC Blocking Capacitors (C5, C6):**
    *   Symmetrical non-polarized capacitors (e.g., `47 µF NP`) on both inputs. Mismatches in their value can degrade CMRR at low frequencies, so large values are chosen to make their impedance negligible in the audio band.
*   **DC Drain Resistors (R7, R8):**
    *   Provides a DC path to ground for the blocking caps, preventing charge buildup (`100 kΩ` each).
*   **HF Stability Capacitors (C1, C2):**
    *   Small capacitors (e.g., `27 pF`) are placed across the feedback resistors (`R2`, `R4`) to prevent op-amp instability at high frequencies and maintain balance. `C1` must equal `C2`.

### Achieving High CMRR

**CMRR is the most important specification of a balanced input stage.**
1.  **Resistor Matching is Critical:** The accuracy of the CMRR is limited by the tolerance of the four main amplifier resistors (R1, R2, R3, R4).
    *   Using standard 1% resistors, the worst-case CMRR is only around 40 dB.
    *   Using **0.1% tolerance resistors** is highly recommended and can yield a much better CMRR of ~60 dB.
    *   For the highest performance, one resistor can be made trimmable (using a fixed resistor and a multi-turn cermet potentiometer) to allow for precise nulling of common-mode signals.
2.  **Symmetrical PCB Layout:** The physical layout of the hot and cold paths should be as identical as possible to maintain balance at high frequencies.
3.  **Op-Amp Choice:** While the op-amp's own internal CMRR and open-loop gain affect performance at high frequencies, the passive component matching is almost always the limiting factor at low-to-mid frequencies where ground loop hum is the primary problem.
