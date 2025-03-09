from fastapi import FastAPI
from fastapi.responses import Response

from model.parking import parking_pred
from model.tools.handle_pred import to_txt
from model.tools.parse import parse_lines

app = FastAPI()

app.post("/getParking")
def get_parking():
    return