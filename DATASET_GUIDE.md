# NIR Plastic Detection - Dataset Integration Guide

## Overview
This project now includes support for thermal/NIR imaging plastic classification using custom-trained YOLO models.

## Available Datasets

### 1. Thermal Imaging Plastic Dataset (Kaggle)
- **Source**: `arcanand/thermal-image-dataset`
- **Content**: Thermal images of plastic and glass objects
- **Classes**: Plastic, Glass
- **Size**: ~60 images (augmented)

### 2. Visual Plastic Classification Dataset (Backup)
- **Source**: Various Kaggle plastic classification datasets
- **Classes**: PET, HDPE, PVC, LDPE, PP, PS, Other
- **Use**: Fallback if thermal dataset is insufficient

## Quick Start

### Step 1: Setup Kaggle API

1. Go to https://www.kaggle.com/settings/account
2. Scroll to "API" section
3. Click "Create New Token"
4. Save `kaggle.json` to `C:\Users\<YourUsername>\.kaggle\`

### Step 2: Download Datasets

```bash
# Install dependencies
pip install kaggle

# Download datasets
python download_datasets.py
```

### Step 3: Prepare Dataset (Manual)

The script creates a YOLO-format directory structure:
```
datasets/thermal_plastic/yolo_format/
├── images/
│   ├── train/  (put training images here)
│   └── val/    (put validation images here)
├── labels/
│   ├── train/  (put training labels here)
│   └── val/    (put validation labels here)
└── data.yaml
```

**Label Format** (YOLO .txt files):
```
<class_id> <x_center> <y_center> <width> <height>
```
All values are normalized (0-1).

### Step 4: Train Custom Model

```bash
# Automatic training
python download_datasets.py --train

# Or manual training
yolo train data=datasets/thermal_plastic/yolo_format/data.yaml model=yolov8n.pt epochs=50
```

### Step 5: Use Custom Model

After training, the model will be saved to `models/thermal_plastic_detector/weights/best.pt`

Update the detector to use it:
```python
detector = NIRPlasticDetector(
    model_path='models/thermal_plastic_detector/weights/best.pt',
    confidence_threshold=0.05
)
```

## Current Implementation

The system currently uses:
- **NIR Image Preprocessing**: CLAHE, bilateral filtering, sharpening
- **YOLOv8n Base Model**: Pretrained on COCO dataset
- **NIR Spectral Analysis**: Simulated based on image characteristics
- **Plastic Class Filtering**: Focuses on common plastic items

## Future Improvements

1. **Custom Trained Model**: Train on actual thermal plastic images
2. **Data Augmentation**: Increase dataset size with augmentation
3. **Multi-Modal**: Combine thermal + visual RGB images
4. **Real-Time Optimization**: Quantize model for faster inference

## Troubleshooting

### Kaggle API Not Working
- Ensure `kaggle.json` is in the correct location
- Check file permissions (should be readable)
- Verify Kaggle account is active

### Training Fails
- Check GPU availability: `torch.cuda.is_available()`
- Reduce batch size if out of memory
- Ensure dataset is properly formatted

### Low Detection Accuracy
- Lower confidence threshold (try 0.01-0.05)
- Use YOLOv8x for better accuracy (slower)
- Train custom model on your specific data

## Dataset Sources

- **Kaggle Thermal Dataset**: https://www.kaggle.com/datasets/arcanand/thermal-image-dataset
- **Roboflow Plastic Datasets**: https://universe.roboflow.com/search?q=plastic
- **Visual Plastic Dataset**: https://www.kaggle.com/datasets (search "plastic classification")
