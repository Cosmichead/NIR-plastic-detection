import PyInstaller.__main__
import os
import shutil
import sys

# Clean previous builds
if os.path.exists('build'):
    shutil.rmtree('build')
if os.path.exists('dist'):
    shutil.rmtree('dist')

# Define paths
base_path = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.join(base_path, 'frontend')
models_path = os.path.join(base_path, 'models')
backend_path = os.path.join(base_path, 'backend')

# Ensure paths exist
if not os.path.exists(frontend_path):
    print(f"Error: Frontend path not found at {frontend_path}")
    sys.exit(1)

if not os.path.exists(models_path):
    print(f"Warning: Models path not found at {models_path}. App might fail if models are missing.")

# PyInstaller arguments
args = [
    'desktop_app.py',
    '--name=PlasticDetector',
    '--onefile',
    '--windowed',  # No console window
    '--clean',
    
    # Add data files
    f'--add-data={frontend_path}{os.pathsep}frontend',
    f'--add-data={models_path}{os.pathsep}models',
    # We add backend as data too, just in case some dynamic loading needs it, 
    # though code is bundled by analysis.
    # Actually, adding it as data ensures the file structure exists for any 
    # __file__ based logic that might still linger (though we patched it).
    f'--add-data={backend_path}{os.pathsep}backend',
    
    # Collect all dependencies for heavy packages
    '--collect-all=ultralytics',
    '--collect-all=flask',
    '--collect-all=cv2',
    '--collect-all=PIL',
    
    # Hidden imports that might be missed
    '--hidden-import=engineio.async_drivers.threading',
    '--hidden-import=backend',
    '--hidden-import=backend.api',
    '--hidden-import=backend.api.advanced_server',
    '--hidden-import=backend.detection',
    '--hidden-import=backend.detection.plastic_detector',
]

print("Building executable with PyInstaller...")
PyInstaller.__main__.run(args)
print("Build complete. Check 'dist' folder.")
