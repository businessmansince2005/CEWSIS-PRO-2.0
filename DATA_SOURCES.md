# Data and Training

CEWSIS has two supported research-data paths:

1. **Default, zero-download path:** `train_model.py` generates reproducible,
   modulation-specific IQ signals locally. This is free, deterministic, and
   suitable for Codespaces demos and automated tests.
2. **Public RF data:** place a compatible `.pkl` file in `data/raw/` and run
   `python train_model.py --dataset data/raw`. The loader supports the
   public RML2016.10a dictionary format documented by DeepSig at
   <https://www.deepsig.ai/datasets>.

The generated model is saved to
`checkpoints/cewsis_signal_classifier.joblib` and is loaded by the FastAPI
service at request time. The UI is a research demonstrator, not an operational
electronic-warfare system; do not use it with sensitive or classified data.