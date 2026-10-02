# Demo Scripts - Quick Reference

## 🚀 Quick Start

**Before your presentation, run these in order:**

```bash
# 1. Check everything is ready
python demo_setup_check.py

# 2. Test data pipeline demo
python demo_pipeline.py

# 3. Test classification demo  
python demo_classification.py

# OR run everything at once:
python run_full_demo.py
```

---

## 📁 Demo Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `demo_setup_check.py` | Verify environment is ready | **First thing** - before presentation |
| `demo_pipeline.py` | Show IQ → Spectrogram conversion | **Slide 2** - Technical Foundation |
| `demo_classification.py` | Show model classification | **Slide 3** - Intelligent Core |
| `run_full_demo.py` | Run all demos in sequence | For practice/testing |

---

## 🎯 What Each Demo Shows

### `demo_setup_check.py`
- ✅ Verifies Python version
- ✅ Checks all required packages
- ✅ Validates project structure
- ✅ Tests critical imports
- ✅ Reports any issues

**Output:** Pass/fail report with specific errors if any

---

### `demo_pipeline.py`
**Shows:** Complete data processing pipeline

**What it does:**
1. Generates a sample RF signal (IQ data)
2. Visualizes IQ signal (time domain + constellation plot)
3. Converts to spectrogram
4. Displays the spectrogram

**What you'll see:**
- Two plots: IQ signal visualization and spectrogram
- Console output showing each step
- Files saved to `data/demo_*.png`

**Key message:** "This is how we convert raw RF signals to AI-ready data"

---

### `demo_classification.py`
**Shows:** AI model classification capability

**What it does:**
1. Prepares test signals
2. Converts to spectrograms
3. Loads/creates CNN model
4. Runs inference on test samples
5. Shows predictions with confidence scores
6. Displays detailed probability breakdown

**What you'll see:**
- Model architecture info
- Classification results table
- Confidence scores for each prediction
- Per-class probability breakdown

**Key message:** "Our AI can classify signals with high confidence"

**Note:** If no trained model exists, it will show the architecture and explain that training is needed.

---

## ⚙️ Requirements

All demos require:
- Python 3.8+
- All packages from `requirements.txt`
- Project structure intact

The setup check will verify all of this.

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Install missing packages
pip install -r requirements.txt
```

### "No module named 'src'"
- Make sure you're in the `cognitive_ew_system` directory
- Run: `cd cognitive_ew_system` first

### Demo scripts don't run
- Check: `python demo_setup_check.py` first
- Fix any errors it reports

### No trained model found
- This is OK! The demo will show model architecture
- To train: Run `notebooks/02_model_training.ipynb`

### Plots don't show
- Make sure matplotlib backend is working
- Try: `python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.show()"`

---

## 📝 Presentation Tips

1. **Run setup check first** - Fix any issues before presentation
2. **Test both demos** - Make sure they work on your machine
3. **Have backup** - If demo fails, show the code/notebooks
4. **Explain while running** - Don't just run code, explain what's happening
5. **Stay calm** - If something breaks, explain the architecture instead

---

## 🎤 During Presentation

### For Slide 2 (Data Pipeline):
```bash
python demo_pipeline.py
```
**While it runs, explain:**
- "This is raw RF data - complex IQ samples"
- "We convert it to a spectrogram - 2D frequency-time representation"
- "This is what our CNN sees - like an image"

### For Slide 3 (Classification):
```bash
python demo_classification.py
```
**While it runs, explain:**
- "This is our CNN architecture"
- "It takes spectrograms and outputs modulation probabilities"
- "Look at these confidence scores - very high certainty"

---

## ✅ Success Checklist

Before your presentation:
- [ ] `demo_setup_check.py` runs without errors
- [ ] `demo_pipeline.py` runs and shows plots
- [ ] `demo_classification.py` runs and shows results
- [ ] You understand what each demo shows
- [ ] You can explain the output

---

## 📚 Additional Resources

- **Full presentation guide:** `PRESENTATION_GUIDE.md`
- **Project documentation:** `README.md`
- **Quick start:** `QUICKSTART.md`
- **Training notebook:** `notebooks/02_model_training.ipynb`

---

**You're ready! Good luck with your presentation! 🚀**

