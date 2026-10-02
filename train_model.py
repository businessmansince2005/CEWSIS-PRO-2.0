"""Train the deployable CEWSIS signal classifier.

The default dataset is generated locally from reproducible, structured IQ
signals so Codespaces can train without a large download. A compatible
pickle dataset can be supplied with --dataset for public RF datasets.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from src.data_preprocessing.load_data import create_synthetic_dataset, load_dataset

MODEL_PATH = Path("checkpoints/cewsis_signal_classifier.joblib")
LABELS = ["BPSK", "QPSK", "8PSK", "16QAM", "64QAM", "GFSK", "GMSK"]


def _features(iq: np.ndarray) -> np.ndarray:
    iq = np.asarray(iq, dtype=np.complex64)
    spectrum = np.abs(np.fft.fft(iq))[: len(iq) // 2]
    power = np.abs(iq) ** 2
    normalized = spectrum / (spectrum.sum() + 1e-8)
    frequencies = np.arange(len(normalized), dtype=np.float32)
    centroid = float((frequencies * normalized).sum())
    return np.array([
        float(iq.real.mean()), float(iq.imag.mean()),
        float(iq.real.std()), float(iq.imag.std()),
        float(power.mean()), float(power.std()),
        float(np.percentile(power, 95)), centroid,
        float(spectrum.max() / (spectrum.mean() + 1e-8)),
    ], dtype=np.float32)


def train(dataset_path: str | None = None, samples: int = 1400, seed: int = 42) -> dict:
    if dataset_path:
        dataset = load_dataset(dataset_path)
    else:
        dataset_dir = Path("data/synthetic")
        create_synthetic_dataset(str(dataset_dir), samples, seed)
        dataset = load_dataset(str(dataset_dir))

    usable = [item for item in dataset if item.get("modulation") in LABELS]
    if not usable:
        raise ValueError("No supported modulation samples were found")

    X = np.stack([_features(item["iq_data"]) for item in usable])
    y = np.array([item["modulation"] for item in usable])
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y
    )
    classifier = RandomForestClassifier(
        n_estimators=180, max_depth=14, min_samples_leaf=2,
        random_state=seed, n_jobs=-1, class_weight="balanced",
    )
    classifier.fit(X_train, y_train)
    predictions = classifier.predict(X_test)
    accuracy = float(accuracy_score(y_test, predictions))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": classifier, "labels": LABELS, "feature_count": X.shape[1]}, MODEL_PATH)
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    result = {"model_path": str(MODEL_PATH), "samples": len(usable), "accuracy": accuracy, "report": report}
    print(f"Saved {MODEL_PATH} | samples={len(usable)} | accuracy={accuracy:.3f}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CEWSIS classifier")
    parser.add_argument("--dataset", help="Directory containing compatible .pkl data")
    parser.add_argument("--samples", type=int, default=1400)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    train(args.dataset, args.samples, args.seed)