app = FastAPI()

@app.get('/')
def root(request: Request):
    return {"status": "ok", "root": request.url.hostname}
