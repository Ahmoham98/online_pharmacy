import uvicorn

#some random comments to test out if we are connected true

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)


