from fastapi import FastAPI, UploadFile, File
from backend.validator import validate_csv, load_csv, clean_data
from fastapi.responses import StreamingResponse
import io

app = FastAPI(title="Dataset Quality Validator")

@app.post("/validate")
async def validate(file: UploadFile = File(...)):
    report = validate_csv(file.file)
    return report


@app.post("/clean")
async def clean(file: UploadFile = File(...)):
    # Load CSV file
    df = load_csv(file.file)

    # Clean file
    cleaned_df = clean_data(df)

    stream = io.StringIO()
    cleaned_df.to_csv(stream, index=False)
    stream.seek(0)  # important!

    # Return downloadable file
    return StreamingResponse(
        stream,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=cleaned.csv"}
    )