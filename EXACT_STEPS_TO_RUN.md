# 🎯 EXACT STEPS - See It Run With Your Eyes

## Your System:
- **Python Version:** 3.14.0 ✅ (Perfect!)
- **Location:** `C:\Python314\python.exe`
- **Project:** `D:\CEWSIS\cognitive_ew_system`

## ❌ What's Missing:
Packages need to be installed: numpy, scipy, torch, matplotlib, etc.

---

## 🚀 EASIEST WAY - Double Click This:

### **`RUN_ME_FIRST.bat`**
**Just double-click this file!** It will:
1. Check Python
2. Install missing packages
3. Run setup check
4. Show you everything

---

## 📝 OR Do It Manually (Step by Step):

### Step 1: Open Command Prompt
- Press `Windows Key + R`
- Type: `cmd`
- Press Enter

### Step 2: Go to Project Folder
```bash
cd D:\CEWSIS\cognitive_ew_system
```

### Step 3: Install Packages (ONE TIME - Takes 2-3 minutes)
```bash
python -m pip install --upgrade pip
python -m pip install numpy scipy scikit-learn matplotlib torch pandas pyyaml jupyter
```

**You'll see:** Lots of downloading and "Successfully installed..." messages

### Step 4: Verify Setup
```bash
python demo_setup_check.py
```

**You'll see:** 
- `[OK]` for everything that works
- `[MISSING]` for anything missing
- `[SUCCESS]` at the end if all good

### Step 5: Run Data Pipeline Demo
```bash
python demo_pipeline.py
```

**You'll see:**
- Console output showing each step
- Two windows will pop up with plots (IQ signal and spectrogram)
- Files saved to `data/demo_*.png`

### Step 6: Run Classification Demo
```bash
python demo_classification.py
```

**You'll see:**
- Model architecture info
- Classification results table
- Confidence scores

---

## 🎬 What You'll See When It Runs:

### When you run `demo_pipeline.py`:
```
============================================================
DEMO: Data Pipeline - IQ Signal to Spectrogram
============================================================

Step 1: Generating sample RF signal (IQ data)...
------------------------------------------------------------
[OK] Generated IQ signal: 1024 samples
  - Signal type: Complex-valued (I + jQ)
  - Shape: (1024,)
  ...

Step 2: Visualizing IQ signal (Constellation Plot)...
------------------------------------------------------------
[OK] Saved IQ visualization to: data/demo_iq_signal.png
[Plot window appears]

Step 3: Converting IQ signal to spectrogram...
------------------------------------------------------------
[OK] Generated spectrogram
  - Shape: (129, 15) (Frequency bins × Time frames)
  ...

Step 4: Visualizing spectrogram...
------------------------------------------------------------
[OK] Saved spectrogram to: data/demo_spectrogram.png
[Plot window appears]
```

### When you run `demo_classification.py`:
```
============================================================
DEMO: AI Model - Signal Classification
============================================================

Step 1: Preparing test signals...
------------------------------------------------------------
[OK] Test dataset prepared
  - Total samples: 50
  - Test samples: 10
  - Modulation classes: ['BPSK', 'GFSK', 'GMSK', 'QPSK', ...]
  ...

Step 2: Converting signals to spectrograms...
------------------------------------------------------------
[OK] Spectrograms prepared
  - Shape: (5, 1, 129, 15)
  ...

Step 3: Initializing CNN model...
------------------------------------------------------------
[OK] Model architecture:
  - Total parameters: 2,345,607
  - Output classes: 7
  ...

Step 4: Running inference on test samples...
------------------------------------------------------------

Classification Results:
------------------------------------------------------------
Sample   True         Predicted    Confidence   Match
------------------------------------------------------------
1        BPSK         BPSK         85.2%        [OK]
2        QPSK         QPSK         92.1%        [OK]
...
```

---

## ✅ Success Looks Like:

1. **Setup Check:** All `[OK]` messages, ends with `[SUCCESS]`
2. **Pipeline Demo:** Plots appear, files saved
3. **Classification Demo:** Results table shows predictions

---

## 🐛 If Something Goes Wrong:

### "Module not found"
→ Run: `pip install numpy scipy scikit-learn matplotlib torch pandas`

### "Python not found"
→ Make sure Python is installed and in PATH

### "Can't find file"
→ Make sure you're in: `D:\CEWSIS\cognitive_ew_system`

### Plots don't show
→ That's OK! Check the saved files in `data/demo_*.png`

---

## 🎯 Quick Test Right Now:

```bash
# 1. Go to folder
cd D:\CEWSIS\cognitive_ew_system

# 2. Check Python
python --version
# Should show: Python 3.14.0

# 3. Install packages (if needed)
python -m pip install numpy matplotlib

# 4. Test it works
python -c "import numpy; print('NumPy works!')"
# Should show: NumPy works!

# 5. Run setup check
python demo_setup_check.py
```

---

## 📁 Files You Can Double-Click:

1. **`RUN_ME_FIRST.bat`** - Does everything automatically
2. **`install_packages.bat`** - Just installs packages
3. **`run_demo.bat`** - Menu to run demos

**Just double-click and watch!**




