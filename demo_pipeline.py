"""
DEMO SCRIPT 1: Data Pipeline Demonstration
Shows: Raw IQ Data → Spectrogram Conversion

Run this to demonstrate the core data processing pipeline.
This is what you'll show in Slide 2: "Our Technical Foundation"
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data_preprocessing.load_data import create_synthetic_dataset, load_dataset
from src.data_preprocessing.create_spectrograms import iq_to_spectrogram, save_spectrogram_image

def demo_data_pipeline():
    """
    Demonstrate the complete data pipeline:
    1. Generate/create IQ signal
    2. Convert to spectrogram
    3. Visualize both
    """
    print("=" * 60)
    print("DEMO: Data Pipeline - IQ Signal to Spectrogram")
    print("=" * 60)
    print()
    
    # Step 1: Create or load a sample signal
    print("Step 1: Generating sample RF signal (IQ data)...")
    print("-" * 60)
    
    # Create a synthetic signal
    iq_signal = np.random.randn(1024) + 1j * np.random.randn(1024)
    
    # Add some structure to make it more realistic
    t = np.linspace(0, 1, 1024)
    carrier = np.exp(1j * 2 * np.pi * 10 * t)  # 10 Hz carrier
    iq_signal = iq_signal * 0.3 + carrier * 0.7
    
    print(f"✓ Generated IQ signal: {len(iq_signal)} samples")
    print(f"  - Signal type: Complex-valued (I + jQ)")
    print(f"  - Shape: {iq_signal.shape}")
    print(f"  - Real part range: [{iq_signal.real.min():.2f}, {iq_signal.real.max():.2f}]")
    print(f"  - Imaginary part range: [{iq_signal.imag.min():.2f}, {iq_signal.imag.max():.2f}]")
    print()
    
    # Step 2: Visualize IQ signal (constellation plot)
    print("Step 2: Visualizing IQ signal (Constellation Plot)...")
    print("-" * 60)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Time domain
    axes[0].plot(iq_signal.real[:200], label='I (In-phase)', alpha=0.7)
    axes[0].plot(iq_signal.imag[:200], label='Q (Quadrature)', alpha=0.7)
    axes[0].set_xlabel('Sample Index')
    axes[0].set_ylabel('Amplitude')
    axes[0].set_title('IQ Signal (Time Domain)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Constellation plot
    axes[1].scatter(iq_signal.real, iq_signal.imag, alpha=0.5, s=10)
    axes[1].set_xlabel('I (In-phase)')
    axes[1].set_ylabel('Q (Quadrature)')
    axes[1].set_title('IQ Constellation Plot')
    axes[1].grid(True, alpha=0.3)
    axes[1].axis('equal')
    
    plt.tight_layout()
    output_path = Path('data/demo_iq_signal.png')
    output_path.parent.mkdir(exist_ok=True)
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"✓ Saved IQ visualization to: {output_path}")
    plt.show()
    print()
    
    # Step 3: Convert to spectrogram
    print("Step 3: Converting IQ signal to spectrogram...")
    print("-" * 60)
    
    spectrogram = iq_to_spectrogram(iq_signal, n_fft=256, hop_length=64)
    
    print(f"✓ Generated spectrogram")
    print(f"  - Shape: {spectrogram.shape} (Frequency bins × Time frames)")
    print(f"  - Frequency bins: {spectrogram.shape[0]}")
    print(f"  - Time frames: {spectrogram.shape[1]}")
    print(f"  - Value range: [{spectrogram.min():.2f}, {spectrogram.max():.2f}]")
    print()
    
    # Step 4: Visualize spectrogram
    print("Step 4: Visualizing spectrogram...")
    print("-" * 60)
    
    plt.figure(figsize=(10, 6))
    plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label='Log Magnitude (dB)')
    plt.xlabel('Time Frame')
    plt.ylabel('Frequency Bin')
    plt.title('Spectrogram: Frequency vs Time Representation')
    plt.tight_layout()
    
    output_path = Path('data/demo_spectrogram.png')
    plt.savefig(output_path, dpi=100, bbox_inches='tight')
    print(f"✓ Saved spectrogram to: {output_path}")
    plt.show()
    print()
    
    # Summary
    print("=" * 60)
    print("PIPELINE SUMMARY")
    print("=" * 60)
    print("✓ Raw IQ Signal (Complex-valued time series)")
    print("  ↓")
    print("✓ Spectrogram (2D frequency-time representation)")
    print("  ↓")
    print("✓ Ready for CNN input (image-like data)")
    print()
    print("This is the foundation of our system!")
    print("Any RF signal can now be converted to this format.")
    print("=" * 60)
    
    return iq_signal, spectrogram


if __name__ == "__main__":
    try:
        iq, spec = demo_data_pipeline()
        print("\n✅ Demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()

