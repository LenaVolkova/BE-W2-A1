from fastapi import FastAPI
import uvicorn

# Create an app
app = FastAPI()

# Configure root path - retutn API description
@app.get("/")
def read_root():
    return { "name": "Task API", "version": "1.0", "endpoints": ["/tasks"] }

#New endpoint to check that server is working
@app.get("/health")
def get_info():
    return { "status": "ok" }

# Launch server 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)