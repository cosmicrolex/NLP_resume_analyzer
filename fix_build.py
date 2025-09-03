#!/usr/bin/env python3
"""
Fix setuptools.build_meta import issues for Python 3.13
This script ensures proper build system setup before package installation
"""

import subprocess
import sys
import os

def fix_setuptools_build_meta():
    """Fix setuptools.build_meta import issues"""
    print("🔧 Fixing setuptools.build_meta import issues...")
    
    try:
        # Upgrade pip first
        print("📦 Upgrading pip...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "pip>=24.0"
        ])
        
        # Install build system requirements
        print("🛠️ Installing build system requirements...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "setuptools>=70.0.0", "wheel>=0.42.0"
        ])
        
        # Verify setuptools.build_meta is available
        print("✅ Verifying setuptools.build_meta...")
        try:
            import setuptools.build_meta
            print("��� setuptools.build_meta is now available!")
            return True
        except ImportError as e:
            print(f"❌ setuptools.build_meta still not available: {e}")
            
            # Try alternative fix
            print("🔄 Attempting alternative fix...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--force-reinstall", "--no-cache-dir", 
                "setuptools>=70.0.0"
            ])
            
            # Test again
            import setuptools.build_meta
            print("✅ setuptools.build_meta fixed with alternative method!")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fix setuptools: {e}")
        return False
    except ImportError as e:
        print(f"❌ setuptools.build_meta still not available after fixes: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def install_requirements():
    """Install requirements after fixing build system"""
    print("📋 Installing requirements...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--no-cache-dir", "-r", "requirements.txt"
        ])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting build system fix...")
    
    # Fix setuptools.build_meta
    if not fix_setuptools_build_meta():
        print("❌ Failed to fix setuptools.build_meta")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements")
        sys.exit(1)
    
    print("🎉 Build system fix completed successfully!")
    sys.exit(0)