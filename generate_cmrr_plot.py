import numpy as np
import matplotlib.pyplot as plt

# Configurare stil
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.grid": True,
    "grid.linestyle": "--",
    "grid.alpha": 0.5
})

# Generare date
t = np.linspace(0, 0.02, 1000)  # 20ms
f = 100  # 100Hz semnal util
f_noise = 50  # 50Hz zgomot de mod comun (brum)

s1 = 1.0 * np.sin(2 * np.pi * f * t)
s2 = -1.0 * np.sin(2 * np.pi * f * t)
# Zgomot compus din 50Hz si putin zgomot alb
noise = 0.4 * np.sin(2 * np.pi * f_noise * t) + 0.05 * np.random.normal(size=len(t))

hot = s1 + noise
cold = s2 + noise
diff = hot - cold

# Creare plot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6), sharex=True)

# Plot 1: Semnal Cald
ax1.plot(t*1000, s1, color='blue', linestyle='--', alpha=0.3, label='Semnal util ($S$)')
ax1.plot(t*1000, hot, color='#1f77b4', label='Semnal Cald ($S + Zgomot$)')
ax1.set_ylabel('Amplitudine [V]')
ax1.legend(loc='upper right', fontsize='x-small')

# Plot 2: Semnal Rece
ax2.plot(t*1000, s2, color='red', linestyle='--', alpha=0.3, label='Semnal util ($-S$)')
ax2.plot(t*1000, cold, color='#d62728', label='Semnal Rece ($-S + Zgomot$)')
ax2.set_ylabel('Amplitudine [V]')
ax2.legend(loc='upper right', fontsize='x-small')

# Plot 3: Semnal Diferențial
ax3.plot(t*1000, diff, color='#2ca02c', linewidth=2, label='Semnal Diferențial')
ax3.set_xlabel('Timp [ms]')
ax3.set_ylabel('Amplitudine [V]')
ax3.legend(loc='upper right', fontsize='x-small')

plt.tight_layout()
plt.savefig('writeing/Template__ETTI_Licenta_RO/figuri/cmrr_signals.pdf', bbox_inches='tight')
print("Graficul a fost generat cu succes în figuri/cmrr_signals.pdf")
