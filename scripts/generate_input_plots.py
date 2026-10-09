import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # run from repo root
import matplotlib.pyplot as plt
import numpy as np
import re
import os

# Files to parse
files = {
    'Mod Neechilibrat, Câștig Scăzut': r'simulations/Results/Doc/Input Interface_freq_resp_unbal_low_gain.txt',
    'Mod Neechilibrat, Câștig Ridicat': r'simulations/Results/Doc/Input Interface_freq_resp_unbal_high_gain.txt',
    'Mod Echilibrat, Câștig Scăzut': r'simulations/Results/Doc/Input Interface_freq_resp_bal_low_gain.txt',
    'Mod Echilibrat, Câștig Ridicat': r'simulations/Results/Doc/Input Interface_freq_resp_bal_high_gain.txt'
}

data = {}

for name, filepath in files.items():
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        continue
    
    freqs = []
    mags = []
    phases = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not line: continue
            
            match = re.match(r'([0-9\.eE\+\-]+)\s+\(([-0-9\.eE\+\-]+)dB,\s*([-0-9\.eE\+\-]+)', line)
            if match:
                freq = float(match.group(1))
                mag = float(match.group(2))
                phase = float(match.group(3))
                
                freqs.append(freq)
                mags.append(mag)
                phases.append(phase)
    
    data[name] = {'freq': freqs, 'mag': mags, 'phase': phases}

fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Răspunsul în frecvență al etajului de intrare', fontsize=16)

subplots = [
    ("Mod Neechilibrat, Câștig Scăzut", axs[0, 0]),
    ("Mod Neechilibrat, Câștig Ridicat", axs[0, 1]),
    ("Mod Echilibrat, Câștig Scăzut", axs[1, 0]),
    ("Mod Echilibrat, Câștig Ridicat", axs[1, 1])
]

for name, ax in subplots:
    if name not in data: continue
    
    ax.set_title(name)
    ax.set_xscale('log')
    ax.plot(data[name]['freq'], data[name]['mag'], color='blue', label='Magnitudine (dB)')
    
    ax.set_ylabel('Amplitudine [dB]', color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    ax2 = ax.twinx()
    ax2.plot(data[name]['freq'], data[name]['phase'], color='red', linestyle=':', label='Fază (°)')
    ax2.set_ylabel('Fază [°]', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

for ax in axs.flat:
    ax.set_xlabel('Frecvență [Hz]')
    ax.set_xlim(10, 100000)

plt.tight_layout()
plt.subplots_adjust(top=0.90)

output_path = r'thesis/figuri/freq_resp_input.pdf'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, format='pdf', bbox_inches='tight')
print(f'Successfully created {output_path}')
