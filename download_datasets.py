"""
Dataset Download and Training Script for NIR Plastic Detection
Downloads thermal imaging plastic dataset from Kaggle and trains a custom YOLO model
"""

import os
import sys
import subprocess
import zipfile
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DATASET_DIR = PROJECT_ROOT / 'datasets' / 'thermal_plastic'
MODELS_DIR = PROJECT_ROOT / 'models'

def setup_kaggle():
    """Setup Kaggle API credentials"""
    print("📦 Setting up Kaggle API...")
    
    # Check if kaggle is installed
    try:
        import kaggle
        print("✓ Kaggle API already installed")
    except ImportError:
        print("Installing Kaggle API...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'kaggle'], check=True)
        import kaggle
    
    # Check for Kaggle credentials
    kaggle_dir = Path.home() / '.kaggle'
    kaggle_json = kaggle_dir / 'kaggle.json'
    
    if not kaggle_json.exists():
        print("\n⚠️  Kaggle API credentials not found!")
        print("Please follow these steps:")
        print("1. Go to https://www.kaggle.com/settings/account")
        print("2. Scroll to 'API' section and click 'Create New Token'")
        print("3. Save the downloaded kaggle.json to:", kaggle_dir)
        print("4. Run this script again")
        return False
    
    print("✓ Kaggle credentials found")
    return True

def download_thermal_dataset():
    """Download thermal imaging plastic dataset from Kaggle"""
    print("\n📥 Downloading thermal plastic dataset...")
    
    # Create dataset directory
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download dataset using Kaggle API
    dataset_name = "arcanand/thermal-image-dataset"
    
    try:
        subprocess.run([
            'kaggle', 'datasets', 'download', 
            '-d', dataset_name,
            '-p', str(DATASET_DIR),
            '--unzip'
        ], check=True)
        
        print(f"✓ Dataset downloaded to {DATASET_DIR}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download dataset: {e}")
        return False

def download_plastic_visual_dataset():
    """Download visual plastic classification dataset as backup"""
    print("\n📥 Downloading visual plastic classification dataset...")
    
    dataset_name = "asdasdasasdas/garbage-classification"
    
    try:
        subprocess.run([
            'kaggle', 'datasets', 'download',
            '-d', dataset_name,
            '-p', str(DATASET_DIR / 'visual'),
            '--unzip'
        ], check=True)
        
        print(f"✓ Visual dataset downloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Visual dataset download failed: {e}")
        return False

def prepare_yolo_dataset():
    """Prepare dataset in YOLO format"""
    print("\n🔧 Preparing dataset for YOLO training...")
    
    # Create YOLO directory structure
    yolo_dir = DATASET_DIR / 'yolo_format'
    (yolo_dir / 'images' / 'train').mkdir(parents=True, exist_ok=True)
    (yolo_dir / 'images' / 'val').mkdir(parents=True, exist_ok=True)
    (yolo_dir / 'labels' / 'train').mkdir(parents=True, exist_ok=True)
    (yolo_dir / 'labels' / 'val').mkdir(parents=True, exist_ok=True)
    
    # Create data.yaml for YOLO
    data_yaml = yolo_dir / 'data.yaml'
    yaml_content = f"""# Thermal Plastic Detection Dataset
path: {yolo_dir.absolute()}
train: images/train
val: images/val

# Classes
names:
  0: plastic
  1: glass
  2: PET
  3: HDPE
  4: PVC
  5: LDPE
  6: PP
  7: PS
"""
    
    with open(data_yaml, 'w') as f:
        f.write(yaml_content)
    
    print(f"✓ YOLO dataset structure created at {yolo_dir}")
    print(f"✓ data.yaml created")
    
    return yolo_dir

def train_custom_model(yolo_dir):
    """Train custom YOLO model on thermal plastic dataset"""
    print("\n🚀 Training custom YOLO model...")
    
    try:
        from ultralytics import YOLO
        
        # Load pretrained YOLOv8n model
        model = YOLO('yolov8n.pt')
        
        # Train the model
        print("Starting training (this may take a while)...")
        results = model.train(
            data=str(yolo_dir / 'data.yaml'),
            epochs=50,
            imgsz=640,
            batch=16,
            name='thermal_plastic_detector',
            project=str(MODELS_DIR),
            patience=10,
            save=True,
            device='0' if __name__ == '__main__' else 'cpu'  # Use GPU if available
        )
        
        print("✓ Training complete!")
        print(f"Model saved to {MODELS_DIR / 'thermal_plastic_detector'}")
        
        return True
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def main():
    """Main execution"""
    print("=" * 60)
    print("  NIR Plastic Detection - Dataset Setup & Training")
    print("=" * 60)
    
    # Step 1: Setup Kaggle
    if not setup_kaggle():
        return
    
    # Step 2: Download thermal dataset
    if not download_thermal_dataset():
        print("\n⚠️  Thermal dataset download failed")
        print("Attempting to download visual plastic dataset as backup...")
        download_plastic_visual_dataset()
    
    # Step 3: Prepare YOLO dataset
    yolo_dir = prepare_yolo_dataset()
    
    # Step 4: Ask user if they want to train
    print("\n" + "=" * 60)
    print("Dataset preparation complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Organize images in the YOLO format directories")
    print("2. Create label files (.txt) for each image")
    print("3. Run training with: python download_datasets.py --train")
    print("\nOr manually train with:")
    print(f"  yolo train data={yolo_dir / 'data.yaml'} model=yolov8n.pt epochs=50")
    
    # Check if --train flag is provided
    if '--train' in sys.argv:
        train_custom_model(yolo_dir)

if __name__ == '__main__':
    main()
