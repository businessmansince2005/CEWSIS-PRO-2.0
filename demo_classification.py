import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import os

# Create data directory if it doesn't exist
os.makedirs('../data', exist_ok=True)

def generate_signal(signal_type='normal', duration=1.0, fs=1000):
    """
    Generate synthetic signals for the EW demo.
    - normal: 50Hz sine wave
    - jammer: 120Hz sine wave (representing interference)
    - anomaly: 50Hz sine wave with sudden high-power noise
    """
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    if signal_type == 'normal':
        # Normal signal at 50Hz
        signal = np.sin(2 * np.pi * 50 * t)
    elif signal_type == 'jammer':
        # Jammer/Interference at 120Hz
        signal = np.sin(2 * np.pi * 120 * t)
    elif signal_type == 'anomaly':
        # Normal signal with a burst of noise (Anomaly)
        signal = np.sin(2 * np.pi * 50 * t)
        # Add noise burst in the middle
        noise_start = int(0.4 * len(t))
        noise_end = int(0.6 * len(t))
        signal[noise_start:noise_end] += np.random.normal(0, 2.0, noise_end - noise_start)
    else:
        signal = np.zeros_like(t)
        
    # Add base white noise to all signals
    signal += np.random.normal(0, 0.1, len(t))
    return t, signal

def plot_spectrogram(t, signal, fs, title, filename):
    f, ts, Sxx = spectrogram(signal, fs)
    plt.figure(figsize=(8, 4))
    plt.pcolormesh(ts, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title(f'Spectrogram - {title}')
    plt.colorbar(label='Intensity [dB]')
    plt.savefig(f'../data/{filename}')
    plt.close()
    print(f"Saved spectrogram to data/{filename}")

def extract_features(signal):
    """Simple feature extraction for the demo."""
    mean = np.mean(signal)
    std = np.std(signal)
    energy = np.sum(signal**2)
    # Simple peak frequency estimate
    fft_vals = np.abs(np.fft.rfft(signal))
    peak_freq_idx = np.argmax(fft_vals)
    return [mean, std, energy, peak_freq_idx]

def run_demo():
    fs = 1000
    print("--- 1. Generating Synthetic Signals ---")
    
    # Generate samples for visualization
    t, sig_norm = generate_signal('normal')
    t, sig_jam = generate_signal('jammer')
    t, sig_anom = generate_signal('anomaly')
    
    # Visual proof: Spectrograms
    plot_spectrogram(t, sig_norm, fs, "Normal Signal (50Hz)", "spec_normal.png")
    plot_spectrogram(t, sig_jam, fs, "Jammer Signal (120Hz)", "spec_jammer.png")
    plot_spectrogram(t, sig_anom, fs, "Anomaly Detected (Noise Burst)", "spec_anomaly.png")

    print("\n--- 2. Training Classifier (Random Forest) ---")
    # Prepare dataset for classification (Normal vs Jammer)
    X = []
    y = []
    
    for _ in range(50):
        _, s = generate_signal('normal')
        X.append(extract_features(s))
        y.append(0) # Normal
        
        _, s = generate_signal('jammer')
        X.append(extract_features(s))
        y.append(1) # Jammer
        
    X = np.array(X)
    y = np.array(y)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    print("Classification Results (Normal vs Jammer):")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Jammer']))

    print("\n--- 3. Anomaly Detection (Threshold-based) ---")
    # Demo Anomaly Detection
    # Using Energy as a proxy for anomaly detection (Autoencoder logic simplified)
    normal_energies = [extract_features(generate_signal('normal')[1])[2] for _ in range(20)]
    threshold = np.mean(normal_energies) + 3 * np.std(normal_energies)
    
    print(f"Calculated Energy Threshold: {threshold:.2f}")
    
    test_signals = [
        ('Normal', generate_signal('normal')[1]),
        ('Anomaly', generate_signal('anomaly')[1])
    ]
    
    for name, s in test_signals:
        feat = extract_features(s)
        energy = feat[2]
        is_anomaly = energy > threshold
        status = "ANOMALY DETECTED" if is_anomaly else "Normal"
        print(f"Signal: {name:7} | Energy: {energy:7.2f} | Result: {status}")

    print("\n--- Demo Completed Successfully ---")
    print("Positioning Tip: 'Due to time constraints, this prototype demonstrates the core intelligence pipeline using simulation-based signals.'")

if __name__ == "__main__":
    run_demo()
