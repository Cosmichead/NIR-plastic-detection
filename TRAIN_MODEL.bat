@echo off
echo ============================================
echo   TRAIN THERMAL PLASTIC DETECTION MODEL
echo ============================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run RUN_APP.bat first to create it.
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo ============================================
echo   TRAINING CONFIGURATION
echo ============================================
echo   Model: YOLOv8x (EXTRA LARGE - BEST ACCURACY)
echo   Dataset: Thermal Imaging (5,031 images)
echo   Epochs: 50
echo   Batch Size: 4 (optimized for YOLOv8x)
echo   Image Size: 640x640
echo ============================================
echo.
echo This will take 30-60 minutes with GPU...
echo (Longer than YOLOv8n but MUCH better accuracy!)
echo Press Ctrl+C to stop training at any time.
echo.

REM Train using Python script (handles PyTorch 2.6 weights_only issue)
python train_thermal.py

echo.
echo ============================================
echo   TRAINING COMPLETE!
echo ============================================
echo.

REM Copy best model to main models directory
if exist "models\thermal_plastic_x\weights\best.pt" (
    echo Copying trained model to models directory...
    copy "models\thermal_plastic_x\weights\best.pt" "models\thermal_plastic_best.pt"
    echo.
    echo ✓ Model saved to: models\thermal_plastic_best.pt
    echo.
    echo Next steps:
    echo 1. Check training results in: models\thermal_plastic_x\
    echo 2. Restart the app: RUN_APP.bat
    echo 3. The system will automatically use your custom model!
    echo 4. Test with thermal images for MAXIMUM accuracy!
) else (
    echo.
    echo ⚠️  Training completed but model not found.
    echo Check models\thermal_plastic_x\ for results.
)

echo.
pause

