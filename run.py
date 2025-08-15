#!/usr/bin/env python3
"""
Simple runner script for the Chat to Excel application.
This provides an alternative to running `streamlit run app.py` directly.
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    try:
        # Check if we're in the right directory
        if not os.path.exists('app.py'):
            print("Error: app.py not found. Please run this script from the project root directory.")
            sys.exit(1)
        
        # Run streamlit
        print("🚀 Starting Chat to Excel application...")
        print("📊 Opening browser at http://localhost:8501")
        print("👋 Press Ctrl+C to stop the application")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.headless", "false",
            "--server.port", "8501",
            "--browser.gatherUsageStats", "false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except FileNotFoundError:
        print("Error: Streamlit not found. Please install requirements with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 