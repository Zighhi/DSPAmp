import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # run from repo root
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# Use a standard style
plt.style.use('seaborn-v0_8-paper')

def get_abs_path(rel_path):
    # Get the directory of the current script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, rel_path)

def parse_complex_file(file_path):
    freqs = []
    vals1 = []
    vals2 = []
    
    abs_path = get_abs_path(file_path)
    if not os.path.exists(abs_path):
        print(f"Error: File {abs_path} not found.")
        return None, None, None

    with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) < 3: continue
            
            try:
                freqs.append(float(parts[0]))
                
                def clean_val(s):
                    match = re.search(r'\((.*)dB,(.*)\)', s)
                    if match:
                        mag = re.sub(r'[^0-9e.+-]', '', match.group(1))
                        phase = re.sub(r'[^0-9e.+-]', '', match.group(2))
                        return float(mag), float(phase)
                    return 0.0, 0.0

                vals1.append(clean_val(parts[1]))
                vals2.append(clean_val(parts[2]))
            except ValueError:
                continue
                
    return np.array(freqs), np.array(vals1), np.array(vals2)

def generate_freq_resp():
    file_path = 'simulations/Results/Doc/Output_Interface_freq_resp.txt'
    freqs, cold, hot = parse_complex_file(file_path)
    if freqs is None: return

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Magnitude plot
    ax1.semilogx(freqs, hot[:, 0], label='Ramura Caldă (Hot)', color='tab:red', linewidth=2)
    ax1.semilogx(freqs, cold[:, 0], label='Ramura Rece (Cold)', color='tab:blue', linestyle='--', linewidth=2)
    ax1.set_ylabel('Amplitudine [dB]')
    # ax1.set_title('Răspunsul în frecvență al interfeței de ieșire (Bode Plot)')
    ax1.grid(True, which="both", ls="-", alpha=0.5)
    ax1.set_ylim(-0.5, 0.5)
    ax1.legend(loc='upper right', frameon=True)
    
    # Phase plot
    ax2.semilogx(freqs, hot[:, 1], label='Fază Hot', color='tab:red', linewidth=2)
    ax2.semilogx(freqs, cold[:, 1], label='Fază Cold', color='tab:blue', linestyle='--', linewidth=2)
    ax2.set_xlabel('Frecvență [Hz]')
    ax2.set_ylabel('Fază [grade]')
    ax2.grid(True, which="both", ls="-", alpha=0.5)
    ax2.legend(loc='center right', frameon=True)
    
    fig.tight_layout()
    output_path = get_abs_path('thesis/figuri/freq_resp_output.pdf')
    plt.savefig(output_path)
    plt.close()

def generate_transient():
    file_path = 'simulations/Results/Doc/Output_Interface_time.txt'
    abs_path = get_abs_path(file_path)
    if not os.path.exists(abs_path):
        print(f"Error: File {abs_path} not found.")
        return

    times = []
    cold = []
    hot = []
    
    with open(abs_path, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split('\t')
            if len(parts) < 3: continue
            try:
                t = float(parts[0])
                if 0.002 <= t <= 0.004:
                    times.append(t * 1000)
                    cold.append(float(parts[1]))
                    hot.append(float(parts[2]))
            except ValueError:
                continue
            
    plt.figure(figsize=(10, 6))
    plt.plot(times, hot, label='Semnal Hot (V)', color='tab:red', linewidth=2)
    plt.plot(times, cold, label='Semnal Cold (V)', color='tab:blue', linewidth=2)
    plt.xlabel('Timp [ms]')
    plt.ylabel('Tensiune [V]')
    # plt.title('Simulare în regim tranzitoriu (1 kHz)')
    plt.grid(True, alpha=0.5)
    plt.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    output_path = get_abs_path('thesis/figuri/output_transient.pdf')
    plt.savefig(output_path)
    plt.close()

def generate_impedance():
    file_path = 'simulations/Results/Doc/Output_Interface_impedance.txt'
    freqs, cold_db, hot_db = parse_complex_file(file_path)
    if freqs is None: return
    
    cold_z = 10**(cold_db[:, 0] / 20)
    hot_z = 10**(hot_db[:, 0] / 20)
    
    plt.figure(figsize=(10, 6))
    plt.semilogx(freqs, hot_z, label='Z(hot)', color='tab:red', linewidth=2)
    plt.semilogx(freqs, cold_z, label='Z(cold)', color='tab:blue', linestyle='--', linewidth=2)
    plt.xlabel('Frecvență [Hz]')
    plt.ylabel(r'Impedanță [$\Omega$]')
    # plt.title('Impedanța de ieșire vs. Frecvență')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.ylim(60, 75)
    plt.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    output_path = get_abs_path('thesis/figuri/output_impedance.pdf')
    plt.savefig(output_path)
    plt.close()

if __name__ == "__main__":
    generate_freq_resp()
    generate_transient()
    generate_impedance()
    print("Plots generated successfully.")
