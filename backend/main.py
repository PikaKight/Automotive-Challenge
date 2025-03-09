from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

app.post("/getParking")
def get_parking():
    return