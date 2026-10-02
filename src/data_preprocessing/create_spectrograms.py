"""
Spectrogram generation utilities for RF signal analysis.

This module converts IQ (In-phase/Quadrature) samples to spectrograms
for use in CNN-based modulation classification.

Author: Cognitive EW System Team
Date: 2024
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from scipy import signal
from scipy.ndimage import zoom

def iq_to_spectrogram(iq_data: np.ndarray, n_fft: int = 256, hop_length: int = 64, 
                      window: str = 'hann') -> np.ndarray:
    """
    Convert IQ complex samples to magnitude spectrogram using Short-Time Fourier Transform (STFT).
    
    This function computes a spectrogram by applying STFT to the complex IQ signal,
    which is standard practice in RF signal analysis for modulation classification.
    
    Args:
        iq_data: Complex-valued IQ samples (1D array of complex numbers)
        n_fft: FFT size (number of frequency bins). Larger values give better frequency resolution.
        hop_length: Hop length between windows (samples). Smaller values give better time resolution.
        window: Window function type ('hann', 'hamming', 'blackman', etc.)
    
    Returns:
        Magnitude spectrogram (2D array, shape: [freq_bins, time_frames])
        Values are in log scale for better dynamic range.
    """
    # Ensure input is numpy array
    iq_data = np.asarray(iq_data)
    
    # Handle real-valued input (convert to complex)
    if not np.iscomplexobj(iq_data):
        if iq_data.ndim == 2 and iq_data.shape[1] == 2:
            # Assume [I, Q] format
            iq_data = iq_data[:, 0] + 1j * iq_data[:, 1]
        else:
            # Assume real part only, create complex with zero Q
            iq_data = iq_data + 0j
    
    # Use scipy's spectrogram for better quality
    if len(iq_data) > n_fft:
        # Compute STFT using scipy
        frequencies, times, stft = signal.stft(
            iq_data,
            nperseg=n_fft,
            noverlap=n_fft - hop_length,
            window=window,
            return_onesided=True
        )
        # Take magnitude
        spectrogram = np.abs(stft)
    else:
        # For short signals, use single FFT
        stft = np.fft.fft(iq_data, n=n_fft)[:n_fft // 2 + 1]
        spectrogram = np.abs(stft).reshape(-1, 1)
    
    # Apply log scale for better visualization and numerical stability
    # log1p = log(1 + x) to handle zeros
    spectrogram = np.log1p(spectrogram)
    
    return spectrogram

def iq_to_mel_spectrogram(iq_data: np.ndarray, sr: int = 1.0, n_mels: int = 128, n_fft: int = 256) -> np.ndarray:
    """
    Convert IQ samples to mel-spectrogram (similar to librosa.feature.melspectrogram).
    
    Args:
        iq_data: Complex IQ samples
        sr: Sample rate (normalized to 1.0 for RF signals)
        n_mels: Number of mel bands
        n_fft: FFT size
    
    Returns:
        Mel-spectrogram (2D array)
    """
    spec = iq_to_spectrogram(iq_data, n_fft=n_fft)
    
    # Simple mel-scale binning (approximate)
    mel_spec = np.zeros((n_mels, spec.shape[1]))
    for i in range(n_mels):
        freq_bin = int(i * spec.shape[0] / n_mels)
        next_freq_bin = int((i + 1) * spec.shape[0] / n_mels)
        mel_spec[i, :] = np.mean(spec[freq_bin:next_freq_bin, :], axis=0)
    
    return mel_spec

def save_spectrogram_image(spectrogram: np.ndarray, out_path: str, title: str = "Spectrogram"):
    """Save spectrogram as image."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    
    plt.figure(figsize=(8, 4))
    plt.imshow(spectrogram, aspect='auto', origin='lower', cmap='viridis')
    plt.colorbar(label='Log Magnitude')
    plt.title(title)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(out, dpi=100, bbox_inches='tight')
    plt.close()
    print(f"Saved spectrogram to {out}")

def batch_iq_to_spectrograms(dataset: List[dict], output_dir: str = None, 
                             n_fft: int = 256, target_shape: Tuple[int, int] = None) -> np.ndarray:
    """
    Convert a batch of IQ samples to spectrograms with consistent sizing.
    
    Args:
        dataset: List of dicts with 'iq_data' key
        output_dir: Optional directory to save sample spectrogram images
        n_fft: FFT size for spectrogram computation
        target_shape: Optional (height, width) to resize all spectrograms to.
                     If None, pads to maximum dimensions found.
    
    Returns:
        Stacked spectrograms (3D array: [samples, freq, time])
        All spectrograms are padded/resized to the same dimensions.
    """
    spectrograms = []
    
    for idx, sample in enumerate(dataset):
        iq = sample['iq_data']
        spec = iq_to_spectrogram(iq, n_fft=n_fft)
        spectrograms.append(spec)
        
        if output_dir and idx < 10:  # Save first 10 as examples
            mod = sample.get('modulation', 'unknown')
            snr = sample.get('snr', 0)
            out_path = Path(output_dir) / f"spec_{idx}_{mod}_{snr}dB.png"
            save_spectrogram_image(spec, str(out_path), title=f"{mod} @ {snr}dB")
    
    # Determine target dimensions
    if target_shape:
        target_height, target_width = target_shape
    else:
        # Pad all to maximum dimensions
        max_height = max(s.shape[0] for s in spectrograms)
        max_width = max(s.shape[1] for s in spectrograms)
        target_height, target_width = max_height, max_width
    
    # Pad or crop all spectrograms to target shape
    padded = []
    for s in spectrograms:
        if s.shape != (target_height, target_width):
            # Use interpolation to resize
            zoom_factors = (target_height / s.shape[0], target_width / s.shape[1])
            s_resized = zoom(s, zoom_factors, order=1)
            padded.append(s_resized)
        else:
            padded.append(s)
    
    return np.array(padded)
