from backend import create_app
from backend.ingest import run_ingest

app = create_app()

if __name__ == "__main__":
    # Automatically check and create chunks on startup
    run_ingest()
    
    app.run(host="0.0.0.0", port=8090, debug=True)