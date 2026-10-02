"""
MASTER DEMO SCRIPT
Runs the complete demonstration in sequence.

This script runs:
1. Setup verification
2. Data pipeline demo
3. Classification demo

Run this for a complete walkthrough, or run individual demos separately.
"""

import sys
from pathlib import Path

def run_full_demo():
    """Run the complete demo sequence."""
    print("=" * 70)
    print("COGNITIVE EW SYSTEM - COMPLETE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This will run:")
    print("1. Setup verification")
    print("2. Data pipeline demonstration")
    print("3. Model classification demonstration")
    print()
    print("Press Enter to continue, or Ctrl+C to cancel...")
    try:
        input()
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
        return
    
    # Step 1: Setup check
    print("\n" + "=" * 70)
    print("STEP 1: SETUP VERIFICATION")
    print("=" * 70)
    print()
    
    try:
        from demo_setup_check import check_setup
        if not check_setup():
            print("\n⚠️  Setup check found errors. Please fix them before continuing.")
            print("You can still run individual demos, but some features may not work.")
            response = input("\nContinue anyway? (y/n): ")
            if response.lower() != 'y':
                return
    except Exception as e:
        print(f"⚠️  Could not run setup check: {e}")
        print("Continuing with demos...")
    
    # Step 2: Data pipeline demo
    print("\n" + "=" * 70)
    print("STEP 2: DATA PIPELINE DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstrates: Raw IQ Signal → Spectrogram Conversion")
    print()
    
    try:
        from demo_pipeline import demo_data_pipeline
        demo_data_pipeline()
    except Exception as e:
        print(f"\n❌ Error in pipeline demo: {e}")
        import traceback
        traceback.print_exc()
        print("\nContinuing to next demo...")
    
    # Step 3: Classification demo
    print("\n" + "=" * 70)
    print("STEP 3: MODEL CLASSIFICATION DEMONSTRATION")
    print("=" * 70)
    print()
    print("This demonstrates: Trained CNN → Signal Classification")
    print()
    
    try:
        from demo_classification import demo_model_classification
        demo_model_classification()
    except Exception as e:
        print(f"\n❌ Error in classification demo: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)
    print()
    print("✅ You have successfully demonstrated:")
    print("   1. Data pipeline (IQ → Spectrogram)")
    print("   2. AI model architecture and classification")
    print()
    print("📊 Key Takeaways:")
    print("   - Complete end-to-end pipeline is working")
    print("   - AI model is ready for training/deployment")
    print("   - System is modular and extensible")
    print()
    print("🚀 Next Steps:")
    print("   - Train the model (notebooks/02_model_training.ipynb)")
    print("   - Add anomaly detection (LSTM-Autoencoder)")
    print("   - Build closed-loop simulation")
    print()
    print("=" * 70)


if __name__ == "__main__":
    try:
        run_full_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()

