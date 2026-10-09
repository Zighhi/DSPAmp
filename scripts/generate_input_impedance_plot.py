import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # run from repo root
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import os
import re

# Files to parse
files = {
    'Calea Caldă (Echilibrat)': r'simulations/Results/Doc/Input Interface_balanced_Hot_impedance.txt',
    'Calea Rece (Echilibrat)': r'simulations/Results/Doc/Input Interface_balanced_Cold_impedance.txt'
}

data = {}

for name, filepath in files.items():
    if not os.path.exists(filepath):
        print(f'File not found: {filepath}')
        continue
    
    freqs = []
    mags = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not line: continue
            
            match = re.match(r'([0-9\.eE\+\-]+)\s+\(([-0-9\.eE\+\-]+)dB,\s*([-0-9\.eE\+\-]+)', line)
            if match:
                freq = float(match.group(1))
                mag_db = float(match.group(2))
                
                # Convert magnitude from dB to linear Ohms
                mag_ohms = 10**(mag_db / 20)
                
                freqs.append(freq)
                mags.append(mag_ohms)
    
    data[name] = {'freq': freqs, 'mag': mags}


# Unbalanced mode files
filepath_unbal_imp = r'simulations/Results/Doc/Input Interface_unbalanced_impedance.txt'
if os.path.exists(filepath_unbal_imp):
    freqs = []
    mags = []
    with open(filepath_unbal_imp, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[1:]:
            line = line.strip()
            if not line: continue
            match = re.match(r'([0-9\.eE\+\-]+)\s+\(([-0-9\.eE\+\-]+)dB,\s*([-0-9\.eE\+\-]+)', line)
            if match:
                freq = float(match.group(1))
                mag_db = float(match.group(2))
                mag_ohms = 10**(mag_db / 20)
                freqs.append(freq)
                mags.append(mag_ohms)
    data['Mod Neechilibrat'] = {'freq': freqs, 'mag': mags}

fig, ax_mag = plt.subplots(figsize=(8, 6))

for name in data:
    color = 'red' if 'Cald' in name else ('blue' if 'Rece' in name else 'green')
    ax_mag.plot(data[name]['freq'], data[name]['mag'], label=name, color=color)

ax_mag.set_xlabel('Frecvență [Hz]')
ax_mag.set_ylabel('Impedanță')
ax_mag.set_xscale('log')
ax_mag.grid(True, which='both', linestyle='--', linewidth=0.5)
ax_mag.legend()
ax_mag.set_xlim(10, 100000)

# Format y axis to show kOhm
def ohm_formatter(x, pos):
    if x >= 1000:
        return f'{x/1000:g} kΩ'
    return f'{x:g} Ω'

ax_mag.yaxis.set_major_formatter(FuncFormatter(ohm_formatter))

plt.tight_layout()

output_path = r'thesis/figuri/input_impedance.pdf'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path, format='pdf', bbox_inches='tight')
print(f'Successfully created {output_path}')

