"""
Quick GPU Check - Diagnose CUDA/GPU Issues
"""

import torch

print("=" * 70)
print("  GPU / CUDA DIAGNOSTIC")
print("=" * 70)
print()

# Check PyTorch version
print(f"PyTorch Version: {torch.__version__}")
print()

# Check CUDA availability
print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    print("✅ CUDA is working!")
    print()
    print("GPU Information:")
    print(f"  • CUDA Version: {torch.version.cuda}")
    print(f"  • GPU Count: {torch.cuda.device_count()}")
    print(f"  • Current Device: {torch.cuda.current_device()}")
    print(f"  • Device Name: {torch.cuda.get_device_name(0)}")
    print(f"  • Device Capability: {torch.cuda.get_device_capability(0)}")
    
    props = torch.cuda.get_device_properties(0)
    print(f"  • Total Memory: {props.total_memory / 1024**3:.2f} GB")
    print(f"  • Multi-Processor Count: {props.multi_processor_count}")
    print()
    print("✅ Your RTX 3050 is ready for training!")
    print("   Training will use GPU automatically.")
else:
    print("❌ CUDA is NOT available!")
    print()
    print("Possible reasons:")
    print("1. PyTorch CPU-only version installed")
    print("2. CUDA drivers not installed")
    print("3. CUDA version mismatch")
    print()
    print("Current PyTorch build:", torch.__version__)
    print()
    
    # Check if this is CPU-only build
    if '+cpu' in torch.__version__:
        print("⚠️  You have PyTorch CPU-only version!")
        print()
        print("To fix, reinstall PyTorch with CUDA support:")
        print()
        print("pip uninstall torch torchvision torchaudio")
        print("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
        print()
    else:
        print("Check NVIDIA drivers:")
        print("  nvidia-smi")
        print()
        print("If nvidia-smi works, reinstall PyTorch:")
        print("  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")

print()
print("=" * 70)
