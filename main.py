import zipfile
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io

## FastApi configuration
app = FastAPI()

## Route
@app.post("/zip/download")
@app.post("/zip/download/")
async def mock_download():
    zip_bytes_io = io.BytesIO()
    input_zip = zipfile.ZipFile("output.zip", 'r')
    files = [file for file in input_zip.namelist() if file.find('.jpg') != -1]  # Only reading jpg files
    with zipfile.ZipFile(zip_bytes_io, 'w', zipfile.ZIP_DEFLATED) as zipped:
        for file in files:
            zipped.writestr(file, input_zip.read(file))
    input_zip.close()

    response = StreamingResponse(
                iter([zip_bytes_io.getvalue()]),
                media_type="application/x-zip-compressed",
                headers = {"Content-Disposition":f"attachment;filename=output.zip",
                            "Content-Length": str(zip_bytes_io.getbuffer().nbytes)}
            )
    zip_bytes_io.close()
    return response
