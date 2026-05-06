from fastapi import FastAPI

app = FastAPI(title="KR4")


@app.get("/health")
def health_check():
    return {"status": "ok"}
