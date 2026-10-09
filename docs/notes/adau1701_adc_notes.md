# ADAU1701 ADC Input Notes

## 1. ADC Characteristics and Input Type
*   The ADAU1701 features two Σ-Δ ADCs (ADC0 and ADC1).
*   The ADCs are **current input**, meaning a voltage-to-current conversion resistor is required on the inputs.
*   **Internal Resistors:**
    *   ADC0, ADC1, and ADC_RES pins each have an internal 2 kΩ resistor for ESD protection.
    *   The voltage seen directly on the ADC input pins is the 1.5 V common mode.
*   **ADC_RES Pin:**
    *   An external resistor connected to ADC_RES sets the full-scale current input of the ADCs.
    *   The full range of the ADC inputs is 100 µA rms.
    *   For a 48 kHz sampling rate, an external 18 kΩ resistor is typically used on ADC_RES (resulting in a total of 20 kΩ with the internal 2 kΩ).
    *   The ADC_RES resistor value only needs to be changed if a sampling rate other than 48 kHz is used.
*   **ADC0/ADC1 Input Pins:**
    *   The voltage-to-current resistors connected to ADC0/ADC1 determine the full-scale voltage input of the ADCs.
    *   With a full-scale current input of 100 µA rms, a 2.0 V rms signal with an external 18 kΩ resistor (total 20 kΩ with the internal 2 kΩ) results in an input utilizing the full range of the ADC.
    *   Matching these input resistors to the ADC_RES resistor is crucial, and 1% tolerance resistors are recommended for all three.

## 2. Resistor Calculation Formula (for 48 kHz sampling rate)
The total input resistance (external + internal 2kΩ) required for a given RMS Input Voltage to reach full-scale is calculated as:
`R_Input Total = (RMS Input Voltage) * 10 kΩ * (48,000 / fs_NEW)`
(Assuming `fs_NEW` is 48,000 Hz, the `(48,000 / fs_NEW)` term becomes 1).

## 3. Desired Input Level for DSP (-6dBFS)

The goal is to design the input interface such that the nominal signal level results in -6dBFS inside the DSP. This implies setting the ADC's full-scale (0dBFS) point to be 6dB higher than the nominal input signal level.

Using the provided data, a 2.0 V RMS full-scale input is explicitly mentioned as utilizing the full range of the ADC and corresponds to a total input resistance of 20 kΩ. This provides good headroom for common audio line levels.

*   **Chosen ADC Full-Scale (0dBFS) Reference:** 2.0 V RMS (at 48 kHz sampling rate).

*   **Input Signal Level for -6dBFS in DSP (relative to 2.0V RMS full scale):**
    A -6dB change in voltage corresponds to dividing the voltage by 10^(6/20) ≈ 1.995.
    Therefore, for -6dBFS: `2.0 V RMS / 1.995 ≈ 1.002 V RMS`.
    So, an input signal of approximately **1.0 V RMS** would correspond to -6dBFS within the DSP when the ADC is configured for a 2.0 V RMS full scale.

## 4. Recommended Input Configuration for 2.0 V RMS Full-Scale (48 kHz)

Based on Table 13 and Figure 17 (Audio ADC Input Configuration for 2.0 V rms signal):

*   **External Resistor for ADC_RES:** 18 kΩ (Total: 20 kΩ including internal 2 kΩ).
*   **External Resistors for ADC0/ADC1:** 18 kΩ each (Total: 20 kΩ each, including internal 2 kΩ).
*   **AC Coupling Capacitors:** 47 µF capacitors are used to AC-couple the input signals, biasing them at the 1.5 V common mode.

### Summary of Component Values for 2.0 V RMS Full-Scale (0dBFS)
*   **Input coupling capacitors:** 47 µF (AC-coupling)
*   **Input series resistors (for ADC0/ADC1):** 18 kΩ (external, in series with internal 2 kΩ, total 20 kΩ)
*   **ADC_RES resistor:** 18 kΩ (external, in series with internal 2 kΩ, total 20 kΩ)

This configuration ensures the ADC is set to its full range for a 2.0 V RMS input, allowing a nominal signal of approximately 1.0 V RMS to register as -6dBFS in the DSP with appropriate headroom.

## 5. Input Driver, Protection, and Layout
_Based on general best practices for interfacing with ADCs._

### 5.1. Driving the ADC Inputs
*   The ADAU1701 has **unbuffered switched-capacitor inputs**. These inputs can generate switching glitches and present a complex impedance that must be driven by a stable, low-impedance source.
*   It is crucial to drive the ADC inputs with an **op-amp buffer stage**. This prevents the ADC's input from being affected by the source impedance and ensures accurate conversion.
*   To filter glitches from the switched-capacitor input and isolate the driving op-amp, a **low-pass RC filter** is recommended between the op-amp output and the ADC input pin (before the main series input resistor).
    *   *Note: While the ADAU1701 datasheet's basic configuration doesn't explicitly show this filter, it is a standard and recommended practice for driving unbuffered ADC inputs to improve stability and performance.*

### 5.2. Input Overvoltage Protection
*   The ADC inputs have internal ESD protection diodes, but these are small and can be easily damaged by the high current an op-amp can deliver if the input voltage exceeds the ADC's supply rails. It is recommended that the input voltage does not exceed the rails by more than 300 mV.
*   If the driving op-amp is powered from higher voltage rails (e.g., +/-15V) than the ADC's analog supply, **external clamping diodes** are essential for protection.
*   **Implementation:**
    *   Connect two **Schottky diodes** per input: one from the input line to the ADC's analog supply voltage (AVDD) and one from the input line to ground (AGND). Schottky diodes are used because their forward voltage is lower than the internal silicon ESD diodes, ensuring they conduct first.
    *   A **series resistor** (e.g., 1 kΩ) should be placed between the op-amp output and the clamping diodes to limit the current flowing through them during an overvoltage event. This resistor also helps to isolate the op-amp from the ADC's input capacitance, improving stability.

### 5.3. PCB Layout Considerations
*   **Grounding:**
    *   Use separate **analog and digital ground planes**.
    *   Connect the two planes at a **single point ("star" ground)**, ideally close to the ADC chip. Some manufacturers (like Analog Devices) recommend making this connection through a **ferrite bead** to filter high-frequency noise.
    *   Run the analog ground plane under the ADC to shield it from digital noise.
*   **Decoupling:**
    *   Decouple all analog and digital supply pins thoroughly.
    *   Use a **0.1 µF ceramic capacitor** in parallel with a **10 µF electrolytic or tantalum capacitor** for each supply.
    *   Place the decoupling capacitors as **physically close** to the IC pins as possible.
*   **Signal Routing:**
    *   Keep digital signal traces (especially clocks) far away from analog input traces.
    *   Do not run digital traces under the ADC chip itself, as they can couple noise directly into the die.
    *   If traces must cross on opposite sides of the PCB, they should cross at **right angles** to minimize capacitive coupling.