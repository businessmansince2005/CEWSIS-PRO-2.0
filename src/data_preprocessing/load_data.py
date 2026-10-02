"""
Data loading utilities for Cognitive EW System.

This module handles loading of RF datasets, including:
- RML2016.10a format (RadioML dataset)
- Synthetic datasets
- Custom pickle formats

Author: Cognitive EW System Team
Date: 2024
"""
from pathlib import Path
from typing import List, Tuple, Dict, Optional, Union
import numpy as np
import pickle
import json
import scipy.io

def create_synthetic_dataset(output_dir: str, num_samples: int = 1000, seed: int = 42):
    """
    Generate synthetic RadioML-like dataset with IQ samples, modulations, and SNR levels.
    Each sample: {iq_data, modulation, snr}
    """
    np.random.seed(seed)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    modulations = ['BPSK', 'QPSK', '8PSK', '16QAM', '64QAM', 'GFSK', 'GMSK']
    snr_levels = [-20, -10, 0, 10, 20]
    iq_length = 1024
    
    dataset = []
    for i in range(num_samples):
        mod = modulations[i % len(modulations)]
        snr = snr_levels[i % len(snr_levels)]

        # Generate a learnable, modulation-specific baseband waveform.
        time_axis = np.arange(iq_length)
        carrier = 0.02 + (i % len(modulations)) * 0.025
        phase = 2 * np.pi * carrier * time_axis
        symbol_count = max(1, iq_length // 32)
        if mod == 'BPSK':
            symbols = np.random.choice([-1, 1], symbol_count)
        elif mod == 'QPSK':
            symbols = np.exp(1j * np.random.choice([0, np.pi / 2, np.pi, 3 * np.pi / 2], symbol_count))
        elif mod == '8PSK':
            symbols = np.exp(1j * np.random.choice(np.arange(8) * np.pi / 4, symbol_count))
        elif mod in {'16QAM', '64QAM'}:
            levels = np.arange(-3, 4, 2) if mod == '16QAM' else np.arange(-7, 8, 2)
            symbols = np.random.choice(levels, symbol_count) + 1j * np.random.choice(levels, symbol_count)
            symbols = symbols / np.abs(symbols).mean()
        else:
            symbols = np.exp(1j * np.cumsum(np.random.normal(0, 0.15, symbol_count)))
        envelope = np.repeat(symbols, int(np.ceil(iq_length / symbol_count)))[:iq_length]
        signal = envelope * np.exp(1j * phase)
        noise_scale = 0.03 if snr >= 10 else 0.12
        iq = signal + noise_scale * (np.random.randn(iq_length) + 1j * np.random.randn(iq_length))
        
        dataset.append({
            'iq_data': iq,
            'modulation': mod,
            'snr': snr,
            'sample_id': i
        })
    
    # Save as pickle
    out_path = Path(output_dir) / 'synthetic_dataset.pkl'
    with open(out_path, 'wb') as f:
        pickle.dump(dataset, f)
    print(f"Saved {len(dataset)} samples to {out_path}")

def load_dataset(data_dir: str) -> List[Dict]:
    """
    Load dataset from directory. Looks for .pkl files.
    """
    data_dir = Path(data_dir)
    pkl_files = list(data_dir.glob('**/*.pkl'))
    
    if not pkl_files:
        raise FileNotFoundError(f"No .pkl files found in {data_dir}")
    
    dataset = []
    for pkl_file in pkl_files:
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
            dataset.extend(data if isinstance(data, list) else [data])
    
    return dataset

def partition_dataset(dataset: List[Dict], train_ratio: float = 0.7, val_ratio: float = 0.15, seed: int = 42) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Split dataset into train, val, test sets.
    
    Args:
        dataset: List of sample dictionaries
        train_ratio: Proportion for training set (default: 0.7)
        val_ratio: Proportion for validation set (default: 0.15)
        seed: Random seed for reproducibility
    
    Returns:
        Tuple of (train_set, val_set, test_set)
    """
    np.random.seed(seed)
    indices = np.arange(len(dataset))
    np.random.shuffle(indices)
    
    n_train = int(len(dataset) * train_ratio)
    n_val = int(len(dataset) * val_ratio)
    
    train_indices = indices[:n_train]
    val_indices = indices[n_train:n_train + n_val]
    test_indices = indices[n_train + n_val:]
    
    train_set = [dataset[i] for i in train_indices]
    val_set = [dataset[i] for i in val_indices]
    test_set = [dataset[i] for i in test_indices]
    
    return train_set, val_set, test_set


def load_rml2016_dataset(file_path: str, max_samples: Optional[int] = None) -> List[Dict]:
    """
    Load RML2016.10a dataset from .pkl or .mat file.
    
    The RML2016.10a dataset contains IQ samples with modulation labels and SNR values.
    Format: Dictionary with keys like (modulation, SNR) -> IQ data array
    
    Args:
        file_path: Path to RML2016.10a .pkl or .mat file
        max_samples: Optional limit on number of samples to load (for testing)
    
    Returns:
        List of dictionaries with keys: 'iq_data', 'modulation', 'snr', 'sample_id'
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    
    dataset = []
    
    if file_path.suffix == '.pkl':
        # Load pickle file
        with open(file_path, 'rb') as f:
            data_dict = pickle.load(f, encoding='latin1')
    elif file_path.suffix == '.mat':
        # Load MATLAB file
        data_dict = scipy.io.loadmat(file_path)
        # Remove MATLAB metadata keys
        data_dict = {k: v for k, v in data_dict.items() if not k.startswith('__')}
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}. Expected .pkl or .mat")
    
    # RML2016 format: keys are tuples (modulation, SNR) or strings
    sample_id = 0
    for key, iq_data in data_dict.items():
        if isinstance(key, tuple):
            modulation, snr = key
        elif isinstance(key, str):
            # Try to parse modulation and SNR from key name
            # Format may vary, so we'll extract what we can
            modulation = key.split('_')[0] if '_' in key else key
            snr = 0  # Default if not found
        else:
            continue
        
        # Handle different data shapes
        if isinstance(iq_data, np.ndarray):
            if iq_data.ndim == 1:
                # Single sample
                dataset.append({
                    'iq_data': iq_data.astype(np.complex64),
                    'modulation': str(modulation),
                    'snr': int(snr) if isinstance(snr, (int, float, np.number)) else 0,
                    'sample_id': sample_id
                })
                sample_id += 1
            elif iq_data.ndim == 2:
                # Multiple samples
                for i in range(iq_data.shape[0]):
                    dataset.append({
                        'iq_data': iq_data[i].astype(np.complex64),
                        'modulation': str(modulation),
                        'snr': int(snr) if isinstance(snr, (int, float, np.number)) else 0,
                        'sample_id': sample_id
                    })
                    sample_id += 1
                    if max_samples and sample_id >= max_samples:
                        break
        
        if max_samples and sample_id >= max_samples:
            break
    
    print(f"Loaded {len(dataset)} samples from {file_path}")
    return dataset


def load_any_dataset(data_dir: str, file_name: Optional[str] = None) -> List[Dict]:
    """
    Universal dataset loader that tries multiple formats.
    
    Args:
        data_dir: Directory containing dataset files
        file_name: Optional specific file name to load
    
    Returns:
        List of sample dictionaries
    """
    data_dir = Path(data_dir)
    
    # If specific file provided
    if file_name:
        file_path = data_dir / file_name
        if file_path.exists():
            if 'RML' in file_name or 'rml' in file_name:
                return load_rml2016_dataset(str(file_path))
            elif file_path.suffix == '.pkl':
                return load_dataset(str(data_dir))
    
    # Try RML2016 format first
    rml_files = list(data_dir.glob('*RML*.pkl')) + list(data_dir.glob('*RML*.mat'))
    if rml_files:
        return load_rml2016_dataset(str(rml_files[0]))
    
    # Fall back to generic pickle loader
    return load_dataset(str(data_dir))
