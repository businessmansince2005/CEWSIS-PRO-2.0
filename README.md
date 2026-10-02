# CEWSIS PRO 2.0

A CPU-friendly cognitive spectrum intelligence platform for RF signal classification, visualization, and anomaly research.

## ⚠️ Ethical Disclaimer

**This project uses only open, synthetic, or publicly released data for academic research. It simulates a cognitive EW system for demonstration purposes only. No classified or sensitive data is used or processed in this project.**

## 📋 Project Overview

This system implements a cognitive electronic warfare framework capable of:
- **Modulation Classification**: CNN-based classification of RF signal modulations from spectrograms
- **Anomaly Detection**: LSTM-Autoencoder for detecting unknown or anomalous signal patterns
- **Real-time Processing**: FastAPI backend for live signal analysis
- **Closed-loop Simulation**: Demonstrates cognitive feedback loops for adaptive EW

## 🗂️ Project Structure

```
cognitive_ew_system/
│
├── data/
│   ├── raw/                 # Store downloaded datasets (RML2016.10a, etc.)
│   ├── processed/           # Cleaned, preprocessed data (spectrograms)
│   └── synthetic/           # Synthetic signal datasets
│
├── src/                     # All source code
│   ├── data_preprocessing/
│   │   ├── load_data.py     # Dataset loading (RML2016, synthetic)
│   │   └── create_spectrograms.py  # IQ to spectrogram conversion
│   │
│   ├── models/
│   │   ├── cnn_classifier.py      # CNN for modulation classification
│   │   ├── lstm_autoencoder.py    # LSTM-AE for anomaly detection
│   │   └── train_utils.py        # Training pipeline utilities
│   │
│   ├── evaluation/
│   │   └── metrics.py       # Classification and detection metrics
│   │
│   └── api/                 # FastAPI backend
│       └── app.py           # REST API for real-time classification
│
├── notebooks/              # Jupyter notebooks for exploration
│   ├── 01_data_exploration.ipynb
│   ├── 02_model_training.ipynb
│   └── 03_results_analysis.ipynb
│
├── tests/                  # Unit tests
│   └── test_preprocessing.py
│
├── requirements.txt        # Python dependencies
├── config.yaml            # Configuration parameters
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt

# Train the deployable model and start the web dashboard
python train_model.py --samples 1400
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`. The CEWSIS PRO 2.0 dashboard calls the trained model through
the `/analyze` API; results are no longer random demo responses. For
Codespaces, open the forwarded port 8000 after the dev container finishes
its automatic install and training step. See [DATA_SOURCES.md](DATA_SOURCES.md)
for the offline dataset and public RF-data workflow.

### Dashboard login

The dashboard opens at a login screen. Configure local credentials with the values
from `.env.example` before starting the server:

```powershell
$env:CEWSIS_ADMIN_EMAIL = "researcher@example.com"
$env:CEWSIS_ADMIN_PASSWORD = "use-a-long-random-password"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

After login, the Overview, Live Lab, Spectrum, Models, and Experiments views are
available. Sessions last eight hours in the current single-instance deployment.
See [DEPLOYMENT.md](DEPLOYMENT.md) for public GitHub and Render instructions.

### One-click hosted deployment

[Deploy CEWSIS to Render](https://render.com/deploy?repo=https://github.com/businessmansince2005/CEWSIS-PRO-2.0)

Render will create the FastAPI service from `render.yaml` and provide a public
HTTPS URL. During setup, enter `CEWSIS_ADMIN_EMAIL` and `CEWSIS_ADMIN_PASSWORD`
when Render asks for the private environment values.

### 2. Data Setup

#### Option A: Use Synthetic Data (Quick Start)
The system can generate synthetic RF signals for testing:

```python
from src.data_preprocessing.load_data import create_synthetic_dataset

create_synthetic_dataset(
    output_dir='data/synthetic',
    num_samples=1000,
    seed=42
)
```

#### Option B: Use RML2016.10a Dataset (Recommended)
1. Download RML2016.10a from [IEEE DataPort](https://ieee-dataport.org/open-access/rml201610a)
2. Place the `.pkl` file in `data/raw/`
3. The system will automatically detect and load it

### 3. Data Exploration

Open `notebooks/01_data_exploration.ipynb` to:
- Load and examine the dataset structure
- Visualize IQ constellations for different modulations
- Generate and inspect spectrograms
- Analyze dataset statistics

### 4. Model Training

Open `notebooks/02_model_training.ipynb` to:
- Convert IQ samples to spectrograms
- Train the CNN classifier
- Evaluate on validation and test sets
- Visualize training history

**Target Performance**: >90% validation accuracy on known modulations

### 5. Run Tests

```bash
pytest tests/
```

## 📊 Data Sources

### Primary Dataset: RML2016.10a
- **Source**: IEEE DataPort / DeepSig
- **Content**: 11 modulation types at various SNRs (-20 to +18 dB)
- **Format**: IQ samples with modulation labels
- **Size**: ~20 GB
- **Download**: [RML2016.10a](https://ieee-dataport.org/open-access/rml201610a)

### Alternative: RML2018.01a
- Larger dataset with more modulations
- [RML2018.01a](https://ieee-dataport.org/open-access/deepsig-datasets)

### Synthetic Data
- Generated using `create_synthetic_dataset()` function
- Useful for testing and augmentation
- Configurable modulations and SNR levels

## 🔧 Configuration

Edit `config.yaml` to adjust:
- Data paths
- Model hyperparameters (batch size, learning rate, epochs)
- Training device (CPU/GPU)
- Spectrogram parameters (FFT size, hop length)

## 🧪 Model Architecture

### CNN Classifier
- **Input**: Spectrograms (grayscale images)
- **Architecture**: 4-layer CNN with batch normalization
- **Output**: Modulation class probabilities
- **Classes**: BPSK, QPSK, 8PSK, 16QAM, 64QAM, GFSK, GMSK, etc.

### LSTM Autoencoder (Anomaly Detection)
- **Input**: Sequential IQ samples
- **Architecture**: Encoder-Decoder with LSTM layers
- **Output**: Reconstruction error (anomaly score)

## 📈 Performance Metrics

The system tracks:
- **Classification**: Accuracy, Precision, Recall, F1-score
- **Anomaly Detection**: ROC-AUC, Precision-Recall curve
- **Per-class Performance**: Confusion matrix, per-modulation accuracy

## 🔄 Closed-Loop Simulation (Killer Feature)

The closed-loop simulation demonstrates cognitive feedback:
1. Generates a stream of synthetic signals (known + unknown types)
2. Feeds them to the classification system
3. System classifies known signals and flags anomalies
4. Feedback loop adapts detection thresholds

This is the most impressive feature for defense mentors as it shows the "cognitive" aspect of the system.

## 🛠️ Development Workflow

### Day 1: Environment & Data Setup
- [x] Create folder structure
- [x] Set up virtual environment
- [x] Install dependencies
- [ ] Download RML2016.10a dataset

### Day 2-3: Data Exploration & Preprocessing
- [x] Explore dataset structure
- [x] Implement spectrogram conversion
- [x] Visualize IQ samples and spectrograms

### Day 4-5: Build CNN Classifier
- [x] Implement CNN architecture
- [x] Create training pipeline
- [x] Train and evaluate model
- [x] Achieve >90% validation accuracy

### Day 6-7: Anomaly Detection & API
- [ ] Implement LSTM-Autoencoder
- [ ] Create FastAPI backend
- [ ] Build closed-loop simulation

## 📝 Code Standards

- **Documentation**: All functions have docstrings
- **Type Hints**: Functions use type annotations
- **Testing**: Unit tests for critical functions
- **Version Control**: Git with meaningful commit messages
- **Comments**: Clear explanations for defense/security reviewers

## 🔒 Security & Compliance

- No classified data is used
- All datasets are publicly available
- Code is designed for review by security-cleared personnel
- Clear separation between simulation and operational code

## 📚 References

- O'Shea, T. J., et al. "Radio machine learning dataset generation with GNU Radio." (2016)
- DeepSig Inc. "RML2016.10a Dataset" - IEEE DataPort
- Cognitive EW concepts from defense research literature

## 🤝 Contributing

This is an academic/research project. For contributions:
1. Follow the code style and documentation standards
2. Add unit tests for new features
3. Update this README with changes
4. Ensure all data sources are publicly available

## 📄 License

This project is for academic and research purposes only.

## 👥 Authors

Cognitive EW System Development Team

---

**Status**: Prototype ready for public deployment
