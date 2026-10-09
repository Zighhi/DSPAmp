import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # run from repo root
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style for academic plotting
plt.style.use('bmh')
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman"],
    "axes.labelsize": 12,
    "font.size": 12,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "lines.linewidth": 1.5,
    "axes.grid": True,
    "grid.alpha": 0.5,
    "grid.linestyle": "--"
})

def read_ltspice_txt(filepath):
    """Reads LTspice exported text file, skipping headers if necessary."""
    try:
        # Assuming the first line is headers
        df = pd.read_csv(filepath, sep='\t')
        # Rename columns to strip whitespace and make them consistent
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

def calculate_rms(voltage_array):
    """Calculates RMS value of a voltage array."""
    return np.sqrt(np.mean(np.square(voltage_array)))

def plot_transient():
    base_path = r"simulations\Results\Doc"
    files = {
        'Bal_Low': fr"{base_path}\Input Interface._Balanced_Low_Gain.txt",
        'Bal_High': fr"{base_path}\Input Interface._Balanced_High_Hain.txt",
        'Unbal_Low': fr"{base_path}\Input Interface_Unbalanced_Low_Gain.txt",
        'Unbal_High': fr"{base_path}\Input Interface_Unbalanced_High_Gain.txt"
    }

    data = {}
    for key, path in files.items():
        df = read_ltspice_txt(path)
        if df is not None:
            data[key] = df

    fig, axes = plt.subplots(2, 2, figsize=(12, 7))
    fig.suptitle('Analiza în Regim Tranzitoriu a Interfeței de Intrare (1 kHz Sinusoidal)', fontsize=14)

    # Plot 1: Balanced Low Gain (+4 dBu input)
    ax = axes[0, 0]
    if 'Bal_Low' in data:
        df = data['Bal_Low']
        t = df['time'] * 1000 # convert to ms
        v_out = df['v(out)']
        v_hot = df['v(hot)']
        v_cold = df['v(cold)']
        v_diff = v_hot - v_cold
        
        rms_in = calculate_rms(v_diff)
        rms_out = calculate_rms(v_out)
        
        ax.plot(t, v_diff, label=f'Intrare Dif. ($V_{{hot}} - V_{{cold}}$): {rms_in:.3f} $V_{{rms}}$', color='gray', linestyle='--')
        ax.plot(t, v_out, label=f'Ieșire: {rms_out:.3f} $V_{{rms}}$', color='blue')
        
        ax.set_title('Mod Echilibrat, Câștig Scăzut (Intrare +4 dBu)')
        ax.set_xlabel('Timp [ms]')
        ax.set_ylabel('Tensiune [V]')
        ax.legend(loc='upper right')
        ax.set_xlim(0, 5) # Show 5 periods
        ax.set_ylim(-2.5, 2.5)

    # Plot 2: Balanced High Gain (-10 dBV input)
    ax = axes[0, 1]
    if 'Bal_High' in data:
        df = data['Bal_High']
        t = df['time'] * 1000
        v_out = df['v(out)']
        v_hot = df['v(hot)']
        v_cold = df['v(cold)']
        v_diff = v_hot - v_cold
        
        rms_in = calculate_rms(v_diff)
        rms_out = calculate_rms(v_out)
        
        ax.plot(t, v_diff, label=f'Intrare Dif. ($V_{{hot}} - V_{{cold}}$): {rms_in:.3f} $V_{{rms}}$', color='gray', linestyle='--')
        ax.plot(t, v_out, label=f'Ieșire: {rms_out:.3f} $V_{{rms}}$', color='red')
        
        ax.set_title('Mod Echilibrat, Câștig Ridicat (Intrare -10 dBV)')
        ax.set_xlabel('Timp [ms]')
        ax.set_ylabel('Tensiune [V]')
        ax.legend(loc='upper right')
        ax.set_xlim(0, 5)
        ax.set_ylim(-2.5, 2.5)

    # Plot 3: Unbalanced Low Gain (+4 dBu input)
    ax = axes[1, 0]
    if 'Unbal_Low' in data:
        df = data['Unbal_Low']
        t = df['time'] * 1000
        v_out = df['v(out)']
        v_in = df['v(n011)'] # Assuming n011 is the input node from the txt file columns provided
        
        rms_in = calculate_rms(v_in)
        rms_out = calculate_rms(v_out)
        
        ax.plot(t, v_in, label=f'Intrare Unbal.: {rms_in:.3f} $V_{{rms}}$', color='gray', linestyle='--')
        ax.plot(t, v_out, label=f'Ieșire: {rms_out:.3f} $V_{{rms}}$', color='green')
        
        ax.set_title('Mod Neechilibrat, Câștig Scăzut (Intrare +4 dBu)')
        ax.set_xlabel('Timp [ms]')
        ax.set_ylabel('Tensiune [V]')
        ax.legend(loc='upper right')
        ax.set_xlim(0, 5)
        ax.set_ylim(-2.5, 2.5)

    # Plot 4: Unbalanced High Gain (-10 dBV input)
    ax = axes[1, 1]
    if 'Unbal_High' in data:
        df = data['Unbal_High']
        t = df['time'] * 1000
        v_out = df['v(out)']
        v_in = df['v(n011)']
        
        rms_in = calculate_rms(v_in)
        rms_out = calculate_rms(v_out)
        
        ax.plot(t, v_in, label=f'Intrare Unbal.: {rms_in:.3f} $V_{{rms}}$', color='gray', linestyle='--')
        ax.plot(t, v_out, label=f'Ieșire: {rms_out:.3f} $V_{{rms}}$', color='purple')
        
        ax.set_title('Mod Neechilibrat, Câștig Ridicat (Intrare -10 dBV)')
        ax.set_xlabel('Timp [ms]')
        ax.set_ylabel('Tensiune [V]')
        ax.legend(loc='upper right')
        ax.set_xlim(0, 5)
        ax.set_ylim(-2.5, 2.5)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Save the figure
    output_path = r"thesis\figuri\input_transient.pdf"
    plt.savefig(output_path, format='pdf', bbox_inches='tight')
    print(f"Plot saved to {output_path}")

if __name__ == '__main__':
    plot_transient()
