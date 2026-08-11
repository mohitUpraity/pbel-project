import os
import sys
import subprocess

def check_dependencies():
    """
    Checks if core packages are installed, showing a warning and installation prompt if missing.
    """
    missing_packages = []
    
    # Check Streamlit
    try:
        import streamlit
    except ImportError:
        missing_packages.append("streamlit")
        
    # Check PyMuPDF (fitz)
    try:
        import fitz
    except ImportError:
        missing_packages.append("pymupdf")
        
    # Check PyTesseract
    try:
        import pytesseract
    except ImportError:
        missing_packages.append("pytesseract")
        
    # Check Plotly
    try:
        import plotly
    except ImportError:
        missing_packages.append("plotly")
        
    # Check dotenv
    try:
        import dotenv
    except ImportError:
        missing_packages.append("python-dotenv")

    if missing_packages:
        print("⚠️ Warning: The following Python dependencies are missing:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\nPlease run the following command to install them:")
        print("👉 pip install -r requirements.txt\n")
        return False
    return True

def check_tesseract():
    """
    Diagnose if Tesseract is installed and printed on path.
    """
    try:
        import pytesseract
    except ImportError:
        return False
    
    # Check if configured in env
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    tesseract_cmd = os.getenv("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        
    try:
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR detected: version {version}")
        return True
    except Exception:
        print("⚠️ Warning: Tesseract command-line executable not found in PATH or config.")
        print("  - Scanned PDF pages cannot be processed with OCR.")
        print("  - To enable OCR, please install Tesseract on your system:")
        print("    On macOS: brew install tesseract")
        print("    On Windows: Install from UB-Mannheim installer and set TESSERACT_CMD in .env")
        print("  - Native text-based PDFs will still process successfully without Tesseract.\n")
        return False

def main():
    print("====================================================")
    print("⚖️ Starting Legal Document Risk Analyzer Setup Diagnostics")
    print("====================================================\n")
    
    # Check python version
    print(f"Python Version: {sys.version.split()[0]}")
    
    # Check packages
    deps_ok = check_dependencies()
    
    # Check tesseract
    tesseract_ok = check_tesseract()
    
    # Run Streamlit
    if deps_ok:
        print("🚀 Launching Streamlit dashboard...")
        try:
            subprocess.run(["streamlit", "run", "dashboard.py"], check=True)
        except KeyboardInterrupt:
            print("\n👋 App stopped by user.")
        except Exception as e:
            print(f"\n❌ Failed to launch Streamlit: {e}")
    else:
        print("❌ Cannot start. Please install missing dependencies and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
