from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server import router as server_router
from Embedding import chromaDB_initialize
import uvicorn

# Import the FastAPI framework
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Include the server_router in the application's routers
app.include_router(server_router)

if __name__ == "__main__":
    # Define server configurations
    host = "0.0.0.0"
    port = int(5100)
    process_count = int(3)
    chromaDB_initialize()
    # Start the server with specified host, port, and process count
    print(
        f"Server is running on {host}:{port} and open {process_count} processes")
    uvicorn.run("main:app", host=host, port=port,
                reload=False, workers=process_count)
