import uvicorn

if __name__ == "__main__":
    uvicorn.run("sio_app:app", host="localhost", port=5000)