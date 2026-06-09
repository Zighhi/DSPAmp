import matplotlib.pyplot as plt
import numpy as np

# Set style for academic look
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],
    "font.size": 10,
    "axes.labelsize": 11,
})

# Data: exactly 2 periods
t = np.linspace(0, 2, 500)
v_cc = 12
v_gnd = 6
amplitude = 3
waveform = v_gnd + amplitude * np.sin(2 * np.pi * 1 * t)

fig, ax1 = plt.subplots(figsize=(8, 4.5))

# Plot waveform
ax1.plot(t, waveform, color='#1f77b4', linewidth=2, label='Semnal Audio')

# Reference lines
ax1.axhline(y=v_cc, color='red', linestyle='--', alpha=0.7, label='Rail Pozitiv (12V)')
ax1.axhline(y=v_gnd, color='green', linestyle='-', alpha=0.8, label='Masă Virtuală (6V)')
ax1.axhline(y=0, color='black', linestyle='--', alpha=0.7, label='Masă Reală (0V)')

# Headroom regions
ax1.fill_between(t, 10, 12, color='red', alpha=0.1, label='Limită Clipping (Vcc-2V)')
ax1.fill_between(t, 0, 2, color='red', alpha=0.1)



# Axis 1 (Physical)
ax1.set_xlabel('Timp[s]')
ax1.set_ylabel('Potențial Fizic [V]')
ax1.set_ylim(-1, 13)
ax1.set_yticks([0, 2, 6, 10, 12])
ax1.grid(True, linestyle=':', alpha=0.6)

# Axis 2 (Virtual)
ax2 = ax1.twinx()
ax2.set_ylabel('Potențial Virtual [V]')
ax2.set_ylim(ax1.get_ylim())
ax2.set_yticks([0, 2, 6, 10, 12])
ax2.set_yticklabels(['-6V', '-4V', '0V', '+4V', '+6V'])

# Put legend outside or in a clean spot
ax1.legend(loc='upper right', frameon=True, fontsize=9)

plt.tight_layout()
plt.savefig('D:/Pers/DSPAmp/writeing/Template__ETTI_Licenta_RO/figuri/virtual_ground_concept.pdf')
