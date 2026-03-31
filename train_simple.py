"""
Simple Thermal Model Training Script
Trains YOLOv8 on your thermal imaging dataset
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 70)
    print("  TRAINING THERMAL PLASTIC DETECTION MODEL")
    print("=" * 70)
    print()
    
    # Project paths
    project_root = Path(__file__).parent
    dataset_yaml = project_root / 'datasets' / 'Thermal image.v1i.yolov8' / 'data.yaml'
    
    if not dataset_yaml.exists():
        print(f"❌ Dataset not found: {dataset_yaml}")
        print("Please ensure the thermal dataset is in datasets/Thermal image.v1i.yolov8/")
        return
    
    print(f"✓ Dataset found: {dataset_yaml}")
    print()
    print("Training configuration:")
    print("  • Model: YOLOv8n (nano - fastest)")
    print("  • Epochs: 50")
    print("  • Batch: 8 (reduce if out of memory)")
    print("  • Image size: 640x640")
    print()
    print("This will take 15-30 minutes...")
    print("Press Ctrl+C to stop at any time.")
    print()
    print("=" * 70)
    print()
    
    # Use YOLO CLI directly (simpler and more reliable)
    cmd = [
        sys.executable, '-m', 'ultralytics',
        'train',
        f'data={dataset_yaml}',
        'model=yolov8n.pt',
        'epochs=50',
        'imgsz=640',
        'batch=8',
        'project=models',
        'name=thermal_plastic',
        'patience=15',
        'save=True',
        'plots=True',
        'verbose=True'
    ]
    
    try:
        # Run training
        subprocess.run(cmd, check=True)
        
        print()
        print("=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print()
        print("Model saved to: models/thermal_plastic/weights/best.pt")
        print()
        print("Next steps:")
        print("1. Copy the model:")
        print("   copy models\\thermal_plastic\\weights\\best.pt models\\thermal_plastic_best.pt")
        print()
        print("2. Restart the app:")
        print("   .\\RUN_APP.bat")
        print()
        print("3. The system will automatically use your custom model!")
        print()
        
    except subprocess.CalledProcessError as e:
        print()
        print("❌ Training failed!")
        print(f"Error: {e}")
        print()
        print("Try reducing batch size if you got 'out of memory' error:")
        print("  Edit this file and change batch=8 to batch=4")
    except KeyboardInterrupt:
        print()
        print("⚠️  Training stopped by user")
        print("Best model so far has been saved")

if __name__ == '__main__':
    main()
