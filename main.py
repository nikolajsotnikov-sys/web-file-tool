from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import pandas as pd
import uuid
import os

app = FastAPI()

@app.get("/")
def home():
    return HTMLResponse("""
    <h2>Upload Excel</h2>
    <form action="/process" method="post" enctype="multipart/form-data">
        <input type="file" name="file" />
        <button type="submit">Process</button>
    </form>
    """)

@app.post("/process")
async def process_excel(file: UploadFile = File(...)):
    input_filename = f"input_{uuid.uuid4()}.xlsx"
    with open(input_filename, "wb") as f:
        f.write(await file.read())

    df = pd.read_excel(input_filename)

    output_filename = f"output_{uuid.uuid4()}.xlsx"
    df.to_excel(output_filename, index=False)

    os.remove(input_filename)

    return FileResponse(output_filename, filename="processed.xlsx")
