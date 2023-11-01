from fastapi import FastAPI, Request
app = FastAPI()

@app.get('/')
def root(request: Request):
    return {"status": "ok", "root": request.url.hostname}
