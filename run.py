"""
Ahlan AI - Cross-Platform Application Launcher
Runs the FastAPI backend and serves the interactive tutor interface.
"""
import sys
import os
import webbrowser
import time

def main():
    print("=" * 65)
    print(" 🌲 Ahlan AI (أهلاً) - Personal Levantine & Lebanese Arabic AI Tutor")
    print("=" * 65)
    print(" Starting server on http://localhost:8000 ...")
    print(" Press CTRL+C to stop.\n")

    # Add project root to sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        import uvicorn
    except ImportError:
        print("Error: uvicorn is not installed. Run: pip install -r requirements.txt")
        sys.exit(1)

    # Automatically open browser after 1 second
    def open_browser():
        time.sleep(1.2)
        try:
            webbrowser.open("http://localhost:8000")
        except Exception:
            pass

    import threading
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)

if __name__ == "__main__":
    main()
