"""
Train Custom Thermal Plastic Detection Model
Uses the downloaded thermal imaging datasets to train a YOLOv8 model
"""

import os
import sys
from pathlib import Path
import shutil

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def train_thermal_model():
    """Train YOLOv8 on thermal imaging dataset"""
    print("=" * 70)
    print("  Training Custom Thermal Plastic Detection Model")
    print("=" * 70)
    
    try:
        from ultralytics import YOLO
        import torch
        
        # Check for GPU
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        device_name = torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU'
        print(f"\n🚀 Using device: {device_name}")
        
        # Dataset path
        thermal_dataset = PROJECT_ROOT / 'datasets' / 'Thermal image.v1i.yolov8'
        data_yaml = thermal_dataset / 'data.yaml'
        
        if not data_yaml.exists():
            print(f"\n❌ Dataset not found at {thermal_dataset}")
            print("Please ensure the thermal dataset is downloaded to datasets/Thermal image.v1i.yolov8/")
            return False
        
        print(f"\n✓ Dataset found: {thermal_dataset}")
        print(f"✓ Using config: {data_yaml}")
        
        # Load pretrained YOLOv8 model
        print("\n📦 Loading YOLOv8n pretrained model...")
        model = YOLO('yolov8n.pt')
        
        # Training parameters
        epochs = 100
        batch_size = 16
        img_size = 640
        
        print(f"\n🎯 Training Configuration:")
        print(f"   • Epochs: {epochs}")
        print(f"   • Batch Size: {batch_size}")
        print(f"   • Image Size: {img_size}")
        print(f"   • Device: {device}")
        print(f"   • Patience: 20 (early stopping)")
        
        # Create models directory
        models_dir = PROJECT_ROOT / 'models'
        models_dir.mkdir(exist_ok=True)
        
        # Train the model
        print("\n🚀 Starting training...")
        print("=" * 70)
        
        results = model.train(
            data=str(data_yaml),
            epochs=epochs,
            imgsz=img_size,
            batch=batch_size,
            name='thermal_plastic_v1',
            project=str(models_dir),
            patience=20,
            save=True,
            device=device,
            workers=4,
            verbose=True,
            plots=True,
            # Augmentation
            hsv_h=0.015,
            hsv_s=0.7,
            hsv_v=0.4,
            degrees=10,
            translate=0.1,
            scale=0.5,
            shear=0.0,
            perspective=0.0,
            flipud=0.0,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0
        )
        
        print("\n" + "=" * 70)
        print("✅ Training Complete!")
        print("=" * 70)
        
        # Find best model
        best_model = models_dir / 'thermal_plastic_v1' / 'weights' / 'best.pt'
        
        if best_model.exists():
            print(f"\n✓ Best model saved to: {best_model}")
            
            # Copy to main models directory for easy access
            target_model = models_dir / 'thermal_plastic_best.pt'
            shutil.copy(best_model, target_model)
            print(f"✓ Copied to: {target_model}")
            
            print("\n📊 Training Results:")
            print(f"   • Model: {target_model}")
            print(f"   • Training plots: {models_dir / 'thermal_plastic_v1'}")
            
            print("\n🎯 Next Steps:")
            print("1. Check training plots in models/thermal_plastic_v1/")
            print("2. Model is ready to use!")
            print("3. The system will automatically use this model")
            
            return True
        else:
            print("\n⚠️  Training completed but best model not found")
            return False
            
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def train_plastic_model():
    """Train on plastic classification dataset"""
    print("=" * 70)
    print("  Training Plastic Classification Model")
    print("=" * 70)
    
    try:
        from ultralytics import YOLO
        import torch
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        device_name = torch.cuda.get_device_name(0) if device == 'cuda' else 'CPU'
        print(f"\n🚀 Using device: {device_name}")
        
        # Dataset path
        plastic_dataset = PROJECT_ROOT / 'datasets' / 'plastic.v1i.yolov8'
        data_yaml = plastic_dataset / 'data.yaml'
        
        if not data_yaml.exists():
            print(f"\n❌ Plastic dataset not found at {plastic_dataset}")
            return False
        
        print(f"\n✓ Dataset found: {plastic_dataset}")
        
        # Load model
        model = YOLO('yolov8n.pt')
        
        print("\n🚀 Starting training...")
        
        results = model.train(
            data=str(data_yaml),
            epochs=100,
            imgsz=640,
            batch=16,
            name='plastic_classifier_v1',
            project=str(PROJECT_ROOT / 'models'),
            patience=20,
            save=True,
            device=device,
            workers=4
        )
        
        print("\n✅ Plastic model training complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        return False

def main():
    """Main training function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Train thermal plastic detection models')
    parser.add_argument('--thermal', action='store_true', help='Train thermal imaging model')
    parser.add_argument('--plastic', action='store_true', help='Train plastic classification model')
    parser.add_argument('--both', action='store_true', help='Train both models')
    
    args = parser.parse_args()
    
    # Default to thermal if no args
    if not (args.thermal or args.plastic or args.both):
        args.thermal = True
    
    success = True
    
    if args.thermal or args.both:
        print("\n" + "=" * 70)
        print("TRAINING THERMAL IMAGING MODEL")
        print("=" * 70)
        success = train_thermal_model() and success
    
    if args.plastic or args.both:
        print("\n" + "=" * 70)
        print("TRAINING PLASTIC CLASSIFICATION MODEL")
        print("=" * 70)
        success = train_plastic_model() and success
    
    if success:
        print("\n" + "=" * 70)
        print("🎉 ALL TRAINING COMPLETE!")
        print("=" * 70)
        print("\nYour custom models are ready to use!")
        print("The system will automatically detect and use them.")
    else:
        print("\n⚠️  Some training tasks failed. Check the logs above.")

if __name__ == '__main__':
    main()
