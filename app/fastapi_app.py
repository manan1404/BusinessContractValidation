# app/fastapi_app.py
from fastapi import FastAPI, UploadFile
from scripts.text_extraction import extract_text_from_pdf

app = FastAPI()

@app.post("/extract_text/")
async def extract_text(pdf: UploadFile):
    text = extract_text_from_pdf(pdf.file)
    return {"text": text}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
