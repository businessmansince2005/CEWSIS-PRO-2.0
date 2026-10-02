"""
Unit tests for data preprocessing modules.

Tests cover:
- Dataset loading (synthetic and RML formats)
- Spectrogram generation
- Data partitioning
"""
import numpy as np
import pytest
from pathlib import Path
import pickle
import tempfile
import shutil

from src.data_preprocessing.load_data import (
    create_synthetic_dataset,
    load_dataset,
    partition_dataset,
    load_rml2016_dataset
)
from src.data_preprocessing.create_spectrograms import (
    iq_to_spectrogram,
    batch_iq_to_spectrograms
)


def test_create_synthetic_dataset(tmp_path):
    """Test synthetic dataset creation."""
    output_dir = str(tmp_path / "synthetic")
    create_synthetic_dataset(output_dir=output_dir, num_samples=100, seed=42)
    
    # Check file was created
    pkl_file = Path(output_dir) / 'synthetic_dataset.pkl'
    assert pkl_file.exists()
    
    # Load and verify
    dataset = load_dataset(output_dir)
    assert len(dataset) == 100
    assert 'iq_data' in dataset[0]
    assert 'modulation' in dataset[0]
    assert 'snr' in dataset[0]


def test_load_dataset(tmp_path):
    """Test dataset loading from pickle file."""
    # Create a test dataset
    test_data = [
        {
            'iq_data': np.random.randn(1024) + 1j * np.random.randn(1024),
            'modulation': 'BPSK',
            'snr': 10,
            'sample_id': i
        }
        for i in range(10)
    ]
    
    pkl_path = tmp_path / 'test_dataset.pkl'
    with open(pkl_path, 'wb') as f:
        pickle.dump(test_data, f)
    
    # Load it
    dataset = load_dataset(str(tmp_path))
    assert len(dataset) == 10
    assert dataset[0]['modulation'] == 'BPSK'


def test_partition_dataset():
    """Test dataset partitioning."""
    # Create test dataset
    dataset = [
        {'iq_data': np.random.randn(100), 'modulation': 'BPSK', 'snr': 10, 'sample_id': i}
        for i in range(100)
    ]
    
    train, val, test = partition_dataset(dataset, train_ratio=0.7, val_ratio=0.15, seed=42)
    
    assert len(train) == 70
    assert len(val) == 15
    assert len(test) == 15
    assert len(train) + len(val) + len(test) == 100


def test_iq_to_spectrogram():
    """Test spectrogram generation from IQ samples."""
    # Create test IQ signal
    iq_data = np.random.randn(1024) + 1j * np.random.randn(1024)
    
    # Generate spectrogram
    spec = iq_to_spectrogram(iq_data, n_fft=256, hop_length=64)
    
    # Check output shape and properties
    assert spec.ndim == 2
    assert spec.shape[0] > 0  # Frequency bins
    assert spec.shape[1] > 0  # Time frames
    assert np.all(spec >= 0)  # Log magnitude should be non-negative


def test_batch_iq_to_spectrograms():
    """Test batch spectrogram generation."""
    # Create test dataset
    dataset = [
        {
            'iq_data': np.random.randn(1024) + 1j * np.random.randn(1024),
            'modulation': 'BPSK',
            'snr': 10,
            'sample_id': i
        }
        for i in range(5)
    ]
    
    # Generate spectrograms
    specs = batch_iq_to_spectrograms(dataset, n_fft=256)
    
    # Check output
    assert specs.ndim == 3  # [samples, freq, time]
    assert specs.shape[0] == 5
    assert specs.shape[1] > 0
    assert specs.shape[2] > 0


def test_spectrogram_normalization():
    """Test that spectrograms can be normalized."""
    iq_data = np.random.randn(1024) + 1j * np.random.randn(1024)
    spec = iq_to_spectrogram(iq_data)
    
    # Normalize
    spec_norm = (spec - spec.min()) / (spec.max() - spec.min() + 1e-8)
    
    assert spec_norm.min() >= 0
    assert spec_norm.max() <= 1


def test_rml_dataset_loading(tmp_path):
    """Test RML2016 format dataset loading."""
    # Create a mock RML2016 format dictionary
    rml_data = {
        ('BPSK', 10): np.random.randn(1024) + 1j * np.random.randn(1024),
        ('QPSK', 0): np.random.randn(1024) + 1j * np.random.randn(1024),
    }
    
    pkl_path = tmp_path / 'RML2016_test.pkl'
    with open(pkl_path, 'wb') as f:
        pickle.dump(rml_data, f)
    
    # Load it
    dataset = load_rml2016_dataset(str(pkl_path))
    
    assert len(dataset) == 2
    assert dataset[0]['modulation'] in ['BPSK', 'QPSK']
    assert 'iq_data' in dataset[0]

