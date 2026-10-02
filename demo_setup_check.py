"""
SETUP VERIFICATION SCRIPT
Run this FIRST to ensure everything is ready for the demo.
This checks all dependencies and creates necessary data.
"""

import sys
from pathlib import Path

def check_setup():
    """Verify that the environment is ready for demos."""
    print("=" * 60)
    print("COGNITIVE EW SYSTEM - SETUP VERIFICATION")
    print("=" * 60)
    print()
    
    errors = []
    warnings = []
    
    # Check 1: Python version
    print("1. Checking Python version...")
    if sys.version_info >= (3, 8):
        print(f"   [OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    else:
        errors.append(f"Python 3.8+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        print(f"   [ERROR] Python version too old: {sys.version_info.major}.{sys.version_info.minor}")
    print()
    
    # Check 2: Required packages
    print("2. Checking required packages...")
    required_packages = [
        'numpy', 'scipy', 'sklearn', 'matplotlib', 
        'torch', 'pandas', 'yaml', 'jupyter'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'yaml':
                __import__('yaml')
            else:
                __import__(package)
            print(f"   [OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   [MISSING] {package} - NOT INSTALLED")
            errors.append(f"Missing package: {package}")
    
    if missing_packages:
        print(f"\n   Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
    print()
    
    # Check 3: Project structure
    print("3. Checking project structure...")
    required_dirs = [
        'src/data_preprocessing',
        'src/models',
        'src/evaluation',
        'data',
        'notebooks',
        'tests'
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   [OK] {dir_path}/")
        else:
            errors.append(f"Missing directory: {dir_path}")
            print(f"   [ERROR] {dir_path}/ - NOT FOUND")
    print()
    
    # Check 4: Source modules
    print("4. Checking source modules...")
    required_modules = [
        'src/data_preprocessing/load_data.py',
        'src/data_preprocessing/create_spectrograms.py',
        'src/models/cnn_classifier.py',
        'src/models/train_utils.py',
        'src/evaluation/metrics.py'
    ]
    
    for module in required_modules:
        if Path(module).exists():
            print(f"   [OK] {module}")
        else:
            errors.append(f"Missing module: {module}")
            print(f"   [ERROR] {module} - NOT FOUND")
    print()
    
    # Check 5: Data directories
    print("5. Checking data directories...")
    data_dirs = ['data/raw', 'data/processed', 'data/synthetic']
    for data_dir in data_dirs:
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        print(f"   [OK] {data_dir}/ (created if needed)")
    print()
    
    # Check 6: Checkpoints directory
    print("6. Checking checkpoints directory...")
    checkpoint_dir = Path('checkpoints')
    checkpoint_dir.mkdir(exist_ok=True)
    print(f"   [OK] checkpoints/ (created if needed)")
    
    model_files = list(checkpoint_dir.glob('*.pth'))
    if model_files:
        print(f"   [OK] Found {len(model_files)} trained model(s)")
    else:
        warnings.append("No trained models found. Demo will show model architecture only.")
        print(f"   [WARNING] No trained models found (this is OK for first demo)")
    print()
    
    # Check 7: Test imports
    print("7. Testing critical imports...")
    try:
        sys.path.insert(0, str(Path.cwd()))
        from src.data_preprocessing.load_data import create_synthetic_dataset
        from src.data_preprocessing.create_spectrograms import iq_to_spectrogram
        from src.models.cnn_classifier import CNNClassifier
        print("   [OK] All critical imports successful")
    except Exception as e:
        errors.append(f"Import error: {e}")
        print(f"   [ERROR] Import failed: {e}")
    print()
    
    # Summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    if errors:
        print(f"[FAILED] {len(errors)} ERROR(S) FOUND:")
        for error in errors:
            print(f"   - {error}")
        print()
        print("Please fix these errors before running the demo.")
        return False
    else:
        print("[SUCCESS] All critical checks passed!")
    
    if warnings:
        print(f"\n[WARNING] {len(warnings)} WARNING(S):")
        for warning in warnings:
            print(f"   - {warning}")
        print()
        print("Warnings are non-critical but may affect demo functionality.")
    
    print()
    print("=" * 60)
    print("READY FOR DEMO!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run: python demo_pipeline.py       (Data pipeline demo)")
    print("2. Run: python demo_classification.py (Model classification demo)")
    print()
    
    return len(errors) == 0


if __name__ == "__main__":
    success = check_setup()
    sys.exit(0 if success else 1)

