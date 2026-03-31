# 🚀 Quick Start - Train Custom Thermal Model

## You Have Downloaded the Dataset! ✅

Your thermal imaging dataset is ready at:
- `datasets/Thermal image.v1i.yolov8/` (YOLO format, ready to train!)
- `datasets/archive/` (Raw thermal images)
- `datasets/plastic.v1i.yolov8/` (Plastic classification dataset)

## Train Your Custom Model (2 Simple Steps)

### Step 1: Start Training

Open a **new terminal** (keep the app running) and run:

```bash
# Activate virtual environment
.\.venv\Scripts\activate

# Train thermal imaging model (recommended)
python train_model.py --thermal

# OR train both thermal + plastic models
python train_model.py --both
```

### Step 2: Wait for Training

Training will take **15-30 minutes** depending on your GPU:
- **With GPU (RTX 3050)**: ~15-20 minutes ⚡
- **Without GPU (CPU)**: ~30-45 minutes 🐌

You'll see:
```
🚀 Using device: NVIDIA GeForce RTX 3050
✓ Dataset found: datasets/Thermal image.v1i.yolov8
🚀 Starting training...
Epoch 1/100: ...
```

### Step 3: Model Auto-Deployment ✨

Once training completes:
1. Model is automatically saved to `models/thermal_plastic_best.pt`
2. **System will automatically use it** on next restart
3. No configuration needed!

## Restart the App to Use New Model

```bash
# Stop current app (Ctrl+C in the terminal running it)
# Then restart:
.\RUN_APP.bat
```

You'll see:
```
✓ Using custom trained thermal model: models/thermal_plastic_best.pt
```

## Training Options

```bash
# Train only thermal imaging model (recommended first)
python train_model.py --thermal

# Train only plastic classification model
python train_model.py --plastic

# Train both models
python train_model.py --both
```

## What Happens During Training?

1. **Loads Dataset**: Your thermal images from `datasets/Thermal image.v1i.yolov8/`
2. **Preprocesses**: Applies augmentation (flips, rotations, etc.)
3. **Trains**: 100 epochs with early stopping (stops if no improvement for 20 epochs)
4. **Saves Best Model**: Automatically saves the best performing model
5. **Creates Plots**: Training metrics saved to `models/thermal_plastic_v1/`

## Check Training Progress

Training creates these files:
```
models/thermal_plastic_v1/
├── weights/
│   ├── best.pt          # Best model (auto-copied to thermal_plastic_best.pt)
│   └── last.pt          # Last epoch model
├── results.png          # Training metrics graph
├── confusion_matrix.png # Model accuracy visualization
└── ...                  # Other training plots
```

## Expected Results

After training on your thermal dataset, you should see:
- **Better detection** of plastic vs glass in thermal images
- **Higher confidence** scores for correct classifications
- **Fewer false positives** compared to base model

## Troubleshooting

### "CUDA out of memory"
```bash
# Reduce batch size in train_model.py (line 48):
batch_size = 8  # instead of 16
```

### Training is slow
- **Normal on CPU**: 30-45 minutes is expected
- **Check GPU usage**: Open Task Manager → Performance → GPU
- **Ensure CUDA is working**: Should see "Using device: NVIDIA GeForce RTX 3050"

### Want to stop training early?
- Press `Ctrl+C` in the training terminal
- Best model so far will still be saved

## After Training

1. **Restart the app**: `.\RUN_APP.bat`
2. **Test with thermal images**: Upload thermal images to see improved detection
3. **Compare**: Try same images before/after training to see improvement

## Dataset Info

Your thermal dataset includes:
- **Train**: 3,521 images
- **Validation**: 755 images  
- **Test**: 755 images
- **Classes**: Thermal objects (plastic, glass, etc.)

This is a **great dataset size** for training! 🎉

---

**Ready to train?** Run: `python train_model.py --thermal`
