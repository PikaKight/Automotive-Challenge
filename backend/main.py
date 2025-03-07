from fastapi import FastAPI

app = FastAPI()

app.post("/getParking")
def get_parking():
    return