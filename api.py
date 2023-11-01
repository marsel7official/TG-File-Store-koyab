from fastapi import FastAPI, Request

app = FastAPI()

@app.get('/')
def health_check(request: Request):
    client_host = request.client.host
    server_host = request.url.hostname

    response_data = {
        "status": "ok",
        "client_host": client_host,
        "server_host": server_host,
        "message": "Service is running smoothly."
    }

    return response_data
