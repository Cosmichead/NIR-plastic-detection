"""
Fixed Thermal Model Training Script
Handles PyTorch 2.6 weights_only issue
"""

import torch
import sys
from pathlib import Path

# Fix PyTorch 2.6 weights_only issue
original_torch_load = torch.load
def patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)
torch.load = patched_torch_load

# Now import ultralytics after patching
from ultralytics import YOLO

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
        return
    
    print(f"✓ Dataset found: {dataset_yaml}")
    print()
    
    # Check for GPU and force its use
    if torch.cuda.is_available():
        device = '0'  # Force GPU 0
        device_name = torch.cuda.get_device_name(0)
        print(f"🚀 Using GPU: {device_name}")
        print(f"   CUDA Version: {torch.version.cuda}")
        print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        device = 'cpu'
        device_name = 'CPU'
        print("⚠️  GPU not available, using CPU")
        print("   Training will be slower (60-90 min instead of 30-45 min)")
    
    print()
    print("Training configuration:")
    print("  • Model: YOLOv8x (extra large - BEST ACCURACY)")
    print("  • Epochs: 50")
    print("  • Batch: 4 (optimized for YOLOv8x)")
    print("  • Image size: 640")
    print(f"  • Device: {device} ({device_name})")
    print()
    
    if device == '0':
        print("✅ GPU training enabled - Fast training!")
        print("   Expected time: 30-45 minutes")
    else:
        print("⚠️  CPU training - Slow but will work")
        print("   Expected time: 60-90 minutes")
    
    print()
    print("=" * 70)
    print()
    
    try:
        # Load YOLOv8x model (most accurate)
        print("📦 Loading YOLOv8x pretrained model...")
        model = YOLO('yolov8x.pt')
        
        print(f"✓ Model loaded successfully")
        print(f"Starting training on {device_name}...")
        print()
        
        # Train with GPU forced
        results = model.train(
            data=str(dataset_yaml),
            epochs=50,
            imgsz=640,
            batch=4,  # Reduced for YOLOv8x (larger model)
            project='models',
            name='thermal_plastic_x',
            patience=15,
            save=True,
            device=device,  # Force GPU or CPU
            plots=True,
            verbose=True,
            exist_ok=True  # Allow overwriting previous incomplete training
        )
        
        print()
        print("=" * 70)
        print("✅ TRAINING COMPLETE!")
        print("=" * 70)
        print()
        
        # Copy best model
        best_model = project_root / 'models' / 'thermal_plastic_x' / 'weights' / 'best.pt'
        target = project_root / 'models' / 'thermal_plastic_best.pt'
        
        if best_model.exists():
            import shutil
            shutil.copy(best_model, target)
            print(f"✓ Model saved to: {target}")
            print()
            print("Next steps:")
            print("1. Restart the app: RUN_APP.bat")
            print("2. Upload thermal images")
            print("3. See much better detection!")
        else:
            print("⚠️  Model training completed but best.pt not found")
            
    except Exception as e:
        print()
        print(f"❌ Training failed: {e}")
        print()
        print("If you got 'out of memory', try reducing batch size:")
        print("  Edit this file and change batch=8 to batch=4")

if __name__ == '__main__':
    main()
