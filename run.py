import os
import uvicorn
import traceback

if __name__ == "__main__":
    try:
        import main
        uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    except Exception as e:
        error_text = traceback.format_exc()
        
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse
        app = FastAPI()
        
        @app.get("/{path:path}")
        def catch_all(path: str):
            return HTMLResponse(f"<h1>Crash on Startup</h1><pre>{error_text}</pre>", status_code=500)
            
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
