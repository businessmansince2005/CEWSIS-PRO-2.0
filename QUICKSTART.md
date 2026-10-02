# Quick Start Guide - Cognitive EW System

This guide will help you get the system running quickly through Day 4-5.

## Prerequisites

- Python 3.8 or higher
- 8GB+ RAM recommended
- GPU optional but recommended for training

## Step 1: Environment Setup (5 minutes)

```bash
# Navigate to project directory
cd cognitive_ew_system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Generate Synthetic Data (2 minutes)

Since the RML2016.10a dataset is large (~20GB), we'll start with synthetic data:

```python
# Run in Python or Jupyter
from src.data_preprocessing.load_data import create_synthetic_dataset

create_synthetic_dataset(
    output_dir='data/synthetic',
    num_samples=1000,
    seed=42
)
```

This creates `data/synthetic/synthetic_dataset.pkl` with 1000 samples.

## Step 3: Explore the Data (10 minutes)

Open `notebooks/01_data_exploration.ipynb` and run all cells. This will:
- Load the synthetic dataset
- Show modulation types and SNR levels
- Visualize IQ constellations
- Generate sample spectrograms

**Expected Output**: You should see:
- 7 modulation types (BPSK, QPSK, 8PSK, 16QAM, 64QAM, GFSK, GMSK)
- 5 SNR levels (-20, -10, 0, 10, 20 dB)
- IQ constellation plots
- Spectrogram visualizations

## Step 4: Train the CNN Model (30-60 minutes)

Open `notebooks/02_model_training.ipynb` and run all cells. This will:
1. Load and partition the dataset (70% train, 15% val, 15% test)
2. Convert IQ samples to spectrograms
3. Normalize the data
4. Create data loaders
5. Initialize the CNN model
6. Train for up to 50 epochs
7. Evaluate on test set

**Expected Results**:
- Training should show improving accuracy over epochs
- Validation accuracy should reach >90% (target)
- Test set metrics will be displayed
- Training history plots will be saved

**Note**: Training on CPU may take 30-60 minutes. On GPU, it should take 5-10 minutes.

## Step 5: Verify Results

After training, check:
- `checkpoints/` directory for saved models
- `data/training_history.png` for training curves
- `data/training_config.json` for training configuration

## Troubleshooting

### Import Errors
If you get import errors, make sure:
1. Virtual environment is activated
2. You're in the `cognitive_ew_system` directory
3. All dependencies are installed: `pip install -r requirements.txt`

### Out of Memory
If you run out of memory:
- Reduce `batch_size` in the notebook (default: 32)
- Reduce `num_samples` when creating synthetic data
- Use smaller `n_fft` for spectrograms (default: 256)

### CUDA/GPU Issues
- The system defaults to CPU if CUDA is not available
- To force CPU: Set `device = torch.device('cpu')` in the notebook
- GPU training is automatic if CUDA is detected

## Next Steps (Days 6-7)

After completing Days 1-5:
1. Implement LSTM-Autoencoder for anomaly detection
2. Create FastAPI backend for real-time classification
3. Build closed-loop simulation (the "killer feature")

## Using Real RML2016.10a Data

Once you download RML2016.10a from IEEE DataPort:

1. Place the `.pkl` file in `data/raw/`
2. Update the notebook to use:
   ```python
   from src.data_preprocessing.load_data import load_any_dataset
   
   dataset = load_any_dataset('data/raw', 'RML2016.10a_dict.pkl')
   ```

The system will automatically detect and load the RML format.

## Support

For issues or questions:
1. Check the main `README.md` for detailed documentation
2. Review the code comments (all functions are documented)
3. Check `config.yaml` for configuration options

---

**Status**: Days 1-5 Complete ✅ | Ready for Training!

