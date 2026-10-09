import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # run from repo root
import numpy as np
import matplotlib.pyplot as plt
import os

def load_rew_txt(file_path):
    freqs = []
    mags = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(('*', ' ', 'F')): # Skip header lines
                continue
            parts = line.split()
            if len(parts) >= 2:
                freqs.append(float(parts[0]))
                mags.append(float(parts[1]))
    return np.array(freqs), np.array(mags)

# File paths
diff_file = 'measurements/cmmr_diff.txt'
comun_file = 'measurements/cmmr_comun.txt'
output_pdf = 'thesis/figuri/cmrr_real.pdf'

# Load data
f_diff, m_diff = load_rew_txt(diff_file)
f_comun, m_comun = load_rew_txt(comun_file)

# Ensure same length (truncate to minimum)
min_len = min(len(f_diff), len(f_comun))
f = f_diff[:min_len]
m_diff = m_diff[:min_len]
m_comun = m_comun[:min_len]

# Calculate CMRR
cmrr = m_diff - m_comun

# Plotting
plt.figure(figsize=(10, 6))
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.6
})

plt.semilogx(f, cmrr, color='teal', linewidth=1.5, label='CMRR Masurat')

# Add average value annotation
avg_cmrr = np.mean(cmrr[(f > 100) & (f < 10000)])
plt.axhline(y=avg_cmrr, color='red', linestyle=':', alpha=0.7, label=f'CMRR Mediu (~{avg_cmrr:.1f} dB)')

plt.title('Common Mode Rejection Ratio (CMRR)')
plt.xlabel('Frecventa [Hz]')
plt.ylabel('CMRR [dB]')
plt.xlim(20, 20000)
plt.ylim(0, 80)
plt.xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000], 
           ['20', '50', '100', '200', '500', '1k', '2k', '5k', '10k', '20k'])
plt.legend(loc='lower right')

plt.tight_layout()
plt.savefig(output_pdf, bbox_inches='tight')
print(f"Graficul CMRR a fost salvat in: {output_pdf}")
print(f"Valoare medie CMRR (100Hz-10kHz): {avg_cmrr:.2f} dB")
