import numpy as np
import matplotlib.pyplot as plt
import re
import os

# Configurare stil
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5
})

def parse_ltspice_txt(filepath):
    freqs = []
    mags = []
    phases = []
    with open(filepath, 'r', encoding='latin-1') as f:
        lines = f.readlines()
        for line in lines[1:]: # Skip header
            line = line.strip()
            if not line:
                continue
            # Example line: 1.00000000000000e+00	(-6.93654770588578e+00dB,7.05679606416525e+01°)
            # Also handle potentially different characters for degree symbol
            parts = line.split('\t')
            if len(parts) == 2:
                freq = float(parts[0])
                val_str = parts[1]
                
                # Extract magnitude and phase using regex
                match = re.match(r'\(([^d]+)dB,([^°]+)[°]?\)', val_str)
                if match:
                    mag = float(match.group(1))
                    phase = float(match.group(2))
                    freqs.append(freq)
                    mags.append(mag)
                    phases.append(phase)
    return np.array(freqs), np.array(mags), np.array(phases)

def plot_bode(files_and_labels, output_filename, title):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    
    for filepath, label, color, style in files_and_labels:
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            continue
        freqs, mags, phases = parse_ltspice_txt(filepath)
        ax1.semilogx(freqs, mags, label=label, color=color, linestyle=style)
        ax2.semilogx(freqs, phases, label=label, color=color, linestyle=style)
        
    ax1.set_ylabel('Amplitudine [dB]')
    ax1.set_title(title)
    ax1.legend(loc='lower left')
    
    ax2.set_ylabel('Fază [Grade]')
    ax2.set_xlabel('Frecvență [Hz]')
    
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches='tight')
    print(f"Generated {output_filename}")

# Generate Input Stage Frequency Response Plot
plot_bode([
    ('simulations/Results/Input/Freq_Resp_Balanced_Low_Gain_100pF.txt', 'Echilibrat (Low Gain, C=100pF)', '#1f77b4', '-'),
    ('simulations/Results/Input/Freq_Resp_Balanced_High_Gain_100pF.txt', 'Echilibrat (High Gain, C=100pF)', '#d62728', '-'),
    ('simulations/Results/Input/Freq_Resp_Unbalanced_Low_Gain_100pF.txt', 'Neechilibrat (Low Gain, C=100pF)', '#2ca02c', '--')
], 'writeing/Template__ETTI_Licenta_RO/figuri/freq_resp_input.pdf', 'Răspuns în Frecvență - Etaj Intrare Hibrid')

# Generate Output Stage Frequency Response Plot
plot_bode([
    ('simulations/Results/Output/Freq_Resp_Balanced_Out.txt', 'Răspuns Ieșire Echilibrată', '#9467bd', '-')
], 'writeing/Template__ETTI_Licenta_RO/figuri/freq_resp_output.pdf', 'Răspuns în Frecvență - Etaj Ieșire (Impedance Balanced)')

