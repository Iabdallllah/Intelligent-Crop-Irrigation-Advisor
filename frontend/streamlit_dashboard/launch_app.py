#!/usr/bin/env python3
"""
Smart Crop Recommendation App Launcher
This script automatically starts the Streamlit app and opens the browser
"""

import subprocess
import webbrowser
import time
import os
import sys
import socket
from pathlib import Path

def find_free_port(start_port=8501, max_attempts=10):
    """Find a free port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def kill_streamlit_processes():
    """Kill any running Streamlit processes"""
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'streamlit.exe'], 
                         capture_output=True, text=True, check=False)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'streamlit'], 
                         capture_output=True, text=True, check=False)
        print("🧹 Cleaned up existing Streamlit processes")
        time.sleep(2)  # Wait for cleanup
    except (subprocess.SubprocessError, OSError) as e:
        print(f"⚠️  Could not clean up processes: {e}")

def main():
    print("🌾 Smart Crop Recommendation App Launcher")
    print("=" * 50)
    
    # Clean up any existing Streamlit processes
    kill_streamlit_processes()
    
    # Get the directory of this script
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if virtual environment exists
    venv_python = script_dir / ".venv" / "Scripts" / "python.exe"
    venv_streamlit = script_dir / ".venv" / "Scripts" / "streamlit.exe"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python -m venv .venv")
        return
    
    if not venv_streamlit.exists():
        print("❌ Streamlit not found in virtual environment!")
        print("Please run: pip install streamlit")
        return
    
    # Find a free port
    port = find_free_port(8501)
    if port is None:
        print("❌ Could not find a free port!")
        return
    
    url = f"http://localhost:{port}"
    
    print(f"🚀 Starting Streamlit app on port {port}...")
    print(f"🌐 App will be available at: {url}")
    
    # Start Streamlit app first
    process = None
    try:
        # Start Streamlit in background
        process = subprocess.Popen([
            str(venv_streamlit),
            "run",
            "app.py",
            f"--server.port={port}",
            "--server.headless=true"
        ])
        
        # Wait for Streamlit to start, then open browser
        print("⏳ Waiting for Streamlit to start...")
        time.sleep(4)  # Give Streamlit time to start
        
        print(f"🌐 Opening browser: {url}")
        webbrowser.open(url)
        
        # Wait for the process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")
        if process:
            process.terminate()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting app: {e}")
        print("💡 Try running the script again or manually stop other Streamlit processes")
    except (OSError, subprocess.SubprocessError) as e:
        print(f"❌ Unexpected error: {e}")
        if process:
            process.terminate()

if __name__ == "__main__":
    main()