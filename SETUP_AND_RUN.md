# 🚀 Step-by-Step Setup & Execution Guide

## What Python Version?
**You have Python 3.14.0** - This is PERFECT! ✅

**No virtual environment needed for demos** - We'll use your system Python directly.

---

## 📋 Step-by-Step: See It Run

### Step 1: Open Terminal/Command Prompt
- Press `Win + R`
- Type: `cmd` or `powershell`
- Press Enter

### Step 2: Navigate to Project
```bash
cd D:\CEWSIS\cognitive_ew_system
```

### Step 3: Verify Python Works
```bash
python --version
```
**Should show:** `Python 3.14.0`

### Step 4: Install Required Packages (First Time Only)
```bash
python -m pip install --upgrade pip
pip install numpy scipy scikit-learn matplotlib torch pandas pyyaml jupyter
```

**This will take 2-3 minutes** - It's downloading packages.

### Step 5: Run Setup Check
```bash
python demo_setup_check.py
```

**You'll see:** Green checkmarks if everything is OK

### Step 6: Run Data Pipeline Demo
```bash
python demo_pipeline.py
```

**You'll see:**
- Console output showing each step
- Two plots will appear (IQ signal and spectrogram)
- Files saved to `data/demo_*.png`

### Step 7: Run Classification Demo
```bash
python demo_classification.py
```

**You'll see:**
- Model architecture info
- Classification results table
- Confidence scores

---

## 🎯 Quick Test (Right Now)

Run these commands one by one and watch what happens:

```bash
# 1. Go to project folder
cd D:\CEWSIS\cognitive_ew_system

# 2. Check Python
python --version

# 3. Test import
python -c "import numpy; print('NumPy works!')"

# 4. Run setup check
python demo_setup_check.py
```

---

## ❓ Common Questions

### Do I need a virtual environment?
**No!** For the demo, you can use your system Python directly. Virtual environments are optional.

### What if packages are missing?
Run: `pip install numpy scipy scikit-learn matplotlib torch pandas pyyaml`

### What if I get errors?
- Check the error message
- Make sure you're in the right directory: `D:\CEWSIS\cognitive_ew_system`
- Make sure Python is installed: `python --version`

---

## 🎬 Let's Run It Now!

I'll run the setup check for you so you can see it work!




