# 🚀 QUICK START - Train Your Thermal Model

## ONE-CLICK TRAINING

Just **double-click** this file:
```
TRAIN_MODEL.bat
```

That's it! The training will start automatically.

## What Happens

1. **Activates** virtual environment
2. **Loads** 5,031 thermal images from your dataset
3. **Trains** YOLOv8 model for 50 epochs (~15-30 minutes)
4. **Saves** best model to `models/thermal_plastic_best.pt`
5. **Auto-deploys** - system uses it automatically!

## Training Details

- **Model**: YOLOv8n (fastest, good accuracy)
- **Dataset**: Thermal image.v1i.yolov8 (5,031 images)
- **Epochs**: 50 (with early stopping)
- **Batch**: 8 (reduce to 4 if out of memory)
- **Time**: 15-30 minutes

## After Training

1. **Restart app**: Double-click `RUN_APP.bat`
2. **Upload thermal image**: Same one that failed before
3. **See the difference**: Much better detection!

## Manual Training (Alternative)

If you prefer command line:

```bash
# Open PowerShell
cd "C:\Users\--\Desktop\trial and error\GOAD\xmax2"
.\.venv\Scripts\activate

# Train
yolo train data="datasets/Thermal image.v1i.yolov8/data.yaml" model=yolov8n.pt epochs=50 batch=8 project=models name=thermal_plastic
```

## Troubleshooting

### "Out of memory" error
Edit `TRAIN_MODEL.bat` line 34, change:
```
batch=8  →  batch=4
```

### Training is slow
- **Normal on CPU**: 30-45 minutes
- **With GPU**: 15-20 minutes
- Check Task Manager → Performance → GPU to verify GPU usage

### Want to stop early?
- Press `Ctrl+C`
- Best model so far will still be saved

## Check Training Progress

While training, you'll see:
```
Epoch 1/50: 100%|████████| 220/220 [01:23<00:00,  2.64it/s]
      Class     Images  Instances      Box(P          R      mAP50  mAP50-95)
        all       755       1234      0.856      0.789      0.823      0.612
```

- **P** (Precision): How many detections are correct
- **R** (Recall): How many objects were found
- **mAP50**: Overall accuracy metric

## After Training Files

```
models/
├── thermal_plastic/
│   ├── weights/
│   │   ├── best.pt          # Best model during training
│   │   └── last.pt          # Final epoch model
│   ├── results.png          # Training graphs
│   ├── confusion_matrix.png # Accuracy visualization
│   └── ...
└── thermal_plastic_best.pt  # Auto-copied for easy use
```

## Expected Results

After training, your thermal images should show:
- ✅ **Detected objects** with bounding boxes
- ✅ **Higher confidence** scores (>0.7)
- ✅ **Correct classification** (plastic vs glass)
- ✅ **Fewer false positives**

---

**Ready?** Just double-click `TRAIN_MODEL.bat` and wait 15-30 minutes! ☕
